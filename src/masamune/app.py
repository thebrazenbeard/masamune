from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import replace
from typing import Any

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request

from .commands import parse_command
from .context import (
    build_issue_context,
    build_pr_context,
    build_sweep_context,
    load_repo_policy,
)
from .github import GitHubAppClient
from .orchestrator import MasamuneOrchestrator, review_id_for
from .render import render_report
from .security import verify_github_signature
from .settings import Settings, get_settings
from .store import DeliveryStore

log = logging.getLogger("masamune")

app = FastAPI(
    title="Masamune Cloud",
    version="0.1.0",
    description="Adversarial debugging and continuous defect discovery for GitHub.",
)


def _store(settings: Settings) -> DeliveryStore:
    return DeliveryStore(settings.state_db_path)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "masamune"}


async def _publish_review(
    *,
    gh: GitHubAppClient,
    store: DeliveryStore,
    delivery_id: str,
    context: Any,
    anchor_issue: int,
    orchestrator: MasamuneOrchestrator,
) -> None:
    review_id = review_id_for(context)
    marker = f"<!-- masamune-review:{review_id} -->"

    # Fast idempotency path: do not pay for a repeated model review if the exact
    # subject has already been published on this discussion.
    if await gh.has_comment_marker(context.subject.repository, anchor_issue, marker):
        store.mark(delivery_id, "COMPLETED")
        return

    report = await orchestrator.review(context)
    body = render_report(
        report,
        review_id,
        include_unresolved=context.policy.post_unresolved,
    )
    store.save_review(
        review_id,
        delivery_id,
        context.subject.repository,
        context.subject.kind,
        context.subject.number,
        context.subject.head_sha,
        report.model_dump(mode="json"),
    )
    store.mark(delivery_id, "READY_TO_PUBLISH")

    # Re-read before the non-idempotent write. A previous attempt may have
    # succeeded while its response was lost.
    if not await gh.has_comment_marker(context.subject.repository, anchor_issue, marker):
        await gh.comment(context.subject.repository, anchor_issue, body)

    # Verify the effect instead of assuming POST success proves durable visibility.
    if not await gh.has_comment_marker(context.subject.repository, anchor_issue, marker):
        raise RuntimeError("Masamune comment write did not verify by readback")
    store.mark(delivery_id, "COMPLETED")


async def _process_delivery(
    delivery_id: str,
    event_name: str,
    payload: dict[str, Any],
    settings: Settings,
) -> None:
    store = _store(settings)
    try:
        installation = payload.get("installation") or {}
        installation_id = installation.get("id")
        repository = (payload.get("repository") or {}).get("full_name")
        if not installation_id or not repository:
            store.mark(delivery_id, "IGNORED")
            return

        sender = payload.get("sender") or {}
        if sender.get("type") == "Bot":
            store.mark(delivery_id, "IGNORED")
            return

        gh = GitHubAppClient(settings, int(installation_id))
        repository_meta = await gh.repo(repository)
        if repository_meta.get("private") and not settings.allow_private_repositories:
            store.mark(delivery_id, "IGNORED")
            return

        default_ref = (payload.get("repository") or {}).get("default_branch") or "main"
        policy = await load_repo_policy(gh, repository, default_ref)
        policy = replace(
            policy,
            max_files=min(policy.max_files, settings.max_files),
            max_file_bytes=min(policy.max_file_bytes, settings.max_file_bytes),
            max_context_bytes=min(
                policy.max_context_bytes,
                settings.max_context_bytes,
            ),
        )
        if not policy.enabled:
            store.mark(delivery_id, "IGNORED")
            return

        orchestrator = MasamuneOrchestrator(settings)

        if event_name == "pull_request":
            action = payload.get("action")
            if action not in {"opened", "reopened", "synchronize", "ready_for_review"}:
                store.mark(delivery_id, "IGNORED")
                return
            if not policy.review_pull_requests:
                store.mark(delivery_id, "IGNORED")
                return
            pr = payload.get("pull_request") or {}
            if pr.get("draft") and action != "ready_for_review":
                store.mark(delivery_id, "IGNORED")
                return
            trusted_associations = {"OWNER", "MEMBER", "COLLABORATOR"}
            if (
                not policy.allow_external_pull_requests
                and pr.get("author_association") not in trusted_associations
            ):
                store.mark(delivery_id, "IGNORED")
                return
            number = int(payload["number"])
            context = await build_pr_context(gh, repository, number, policy)
            await _publish_review(
                gh=gh,
                store=store,
                delivery_id=delivery_id,
                context=context,
                anchor_issue=number,
                orchestrator=orchestrator,
            )
            return

        if event_name == "issue_comment" and payload.get("action") == "created":
            if not policy.allow_issue_commands:
                store.mark(delivery_id, "IGNORED")
                return
            comment = payload.get("comment") or {}
            command = parse_command(comment.get("body") or "")
            if command is None:
                store.mark(delivery_id, "IGNORED")
                return
            username = sender.get("login")
            if not username:
                store.mark(delivery_id, "IGNORED")
                return
            permission = await gh.collaborator_permission(repository, username)
            if permission not in {"write", "maintain", "admin"}:
                store.mark(delivery_id, "IGNORED")
                return
            anchor_issue = int((payload.get("issue") or {})["number"])

            if command.kind == "INVESTIGATE":
                target = command.issue_number or anchor_issue
                context = await build_issue_context(gh, repository, target, policy)
            else:
                if not policy.allow_sweep:
                    store.mark(delivery_id, "IGNORED")
                    return
                context = await build_sweep_context(gh, repository, policy)

            await _publish_review(
                gh=gh,
                store=store,
                delivery_id=delivery_id,
                context=context,
                anchor_issue=anchor_issue,
                orchestrator=orchestrator,
            )
            return

        if event_name == "issues" and payload.get("action") == "labeled":
            label = (payload.get("label") or {}).get("name", "").lower()
            if label != "masamune" or not policy.allow_issue_commands:
                store.mark(delivery_id, "IGNORED")
                return
            username = sender.get("login")
            if not username:
                store.mark(delivery_id, "IGNORED")
                return
            permission = await gh.collaborator_permission(repository, username)
            if permission not in {"write", "maintain", "admin"}:
                store.mark(delivery_id, "IGNORED")
                return
            number = int((payload.get("issue") or {})["number"])
            context = await build_issue_context(gh, repository, number, policy)
            await _publish_review(
                gh=gh,
                store=store,
                delivery_id=delivery_id,
                context=context,
                anchor_issue=number,
                orchestrator=orchestrator,
            )
            return

        store.mark(delivery_id, "IGNORED")
    except Exception as exc:
        log.exception("Masamune delivery %s failed", delivery_id)
        store.mark(delivery_id, "FAILED", f"{type(exc).__name__}: {exc}"[:2000])


@app.post("/webhook/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str | None = Header(default=None),
    x_github_delivery: str | None = Header(default=None),
    x_hub_signature_256: str | None = Header(default=None),
) -> dict[str, str]:
    settings = get_settings()
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.max_webhook_bytes:
        raise HTTPException(status_code=413, detail="webhook payload too large")

    body = await request.body()
    if len(body) > settings.max_webhook_bytes:
        raise HTTPException(status_code=413, detail="webhook payload too large")

    if not verify_github_signature(
        settings.github_webhook_secret,
        body,
        x_hub_signature_256,
    ):
        raise HTTPException(status_code=401, detail="invalid webhook signature")

    if not x_github_event or not x_github_delivery:
        raise HTTPException(status_code=400, detail="missing GitHub webhook headers")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="invalid JSON payload") from exc

    digest = hashlib.sha256(body).hexdigest()
    store = _store(settings)
    claim = store.claim(x_github_delivery, x_github_event, digest)
    if not claim.accepted:
        return {"status": "duplicate", "state": claim.state}

    store.mark(x_github_delivery, "PROCESSING")
    background_tasks.add_task(
        _process_delivery,
        x_github_delivery,
        x_github_event,
        payload,
        settings,
    )
    return {"status": "accepted", "delivery": x_github_delivery}
