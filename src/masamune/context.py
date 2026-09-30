from __future__ import annotations

import re
from dataclasses import dataclass

from .github import GitHubAppClient
from .models import Subject
from .policy import RepoPolicy
from .scoping import is_code_path, select_issue_paths, select_sweep_paths


@dataclass(frozen=True)
class ReviewContext:
    subject: Subject
    text: str
    policy: RepoPolicy


_INVISIBLE_CONTROLS = re.compile("[\\u200b-\\u200f\\u202a-\\u202e\\u2060-\\u2064\\ufeff]")


_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"(?i)\b(api[_-]?key|access[_-]?token|secret|password)\b"
        r"(\s*[:=]\s*)[\"']?[A-Za-z0-9_./+=-]{12,}[\"']?"
    ),
]


def _redact(text: str) -> str:
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub("[REDACTED_POTENTIAL_SECRET]", text)
    return _INVISIBLE_CONTROLS.sub(
        lambda match: f"[MASAMUNE INVISIBLE U+{ord(match.group()):04X}]",
        text,
    )


def _bounded(text: str, max_bytes: int) -> str:
    text = _redact(text)
    raw = text.encode("utf-8")
    if len(raw) <= max_bytes:
        return text
    return (
        raw[:max_bytes].decode("utf-8", errors="ignore")
        + "\n[MASAMUNE FILE/PATCH TRUNCATED]"
    )


def _trim(parts: list[str], max_bytes: int) -> str:
    out: list[str] = []
    used = 0
    for part in parts:
        part = _redact(part)
        encoded = part.encode("utf-8")
        if used + len(encoded) > max_bytes:
            remaining = max_bytes - used
            if remaining <= 0:
                break
            out.append(encoded[:remaining].decode("utf-8", errors="ignore"))
            out.append("\n[MASAMUNE CONTEXT TRUNCATED AT POLICY BYTE LIMIT]")
            break
        out.append(part)
        used += len(encoded)
    return "\n".join(out)


async def load_repo_policy(
    gh: GitHubAppClient,
    repository: str,
    default_ref: str,
) -> RepoPolicy:
    from .policy import load_policy

    text = await gh.file_text(repository, ".masamune.yml", default_ref)
    return load_policy(text)


async def build_pr_context(
    gh: GitHubAppClient,
    repository: str,
    number: int,
    policy: RepoPolicy,
) -> ReviewContext:
    pr = await gh.pull(repository, number)
    head_sha = pr["head"]["sha"]
    base_sha = pr["base"]["sha"]
    subject = Subject(
        repository=repository,
        kind="PULL_REQUEST",
        number=number,
        head_sha=head_sha,
        base_sha=base_sha,
        title=pr.get("title") or f"PR #{number}",
        url=pr["html_url"],
    )
    files = await gh.pull_files(repository, number)
    parts = [
        f"SUBJECT: pull request #{number}",
        f"REPOSITORY: {repository}",
        f"BASE_SHA: {base_sha}",
        f"HEAD_SHA: {head_sha}",
        f"TITLE: {pr.get('title', '')}",
        f"BODY:\n{pr.get('body') or ''}",
        "\nCHANGED FILES:",
    ]
    candidates = [item for item in files if is_code_path(item["filename"])]
    candidates.sort(key=lambda item: (-int(item.get("changes", 0)), item["filename"]))
    for item in candidates[: policy.max_files]:
        path = item["filename"]
        patch = _bounded(
            item.get("patch") or "[patch unavailable]",
            policy.max_file_bytes,
        )
        parts.append(
            f"\n=== DIFF {path} ===\n"
            f"status={item.get('status')} additions={item.get('additions')} "
            f"deletions={item.get('deletions')}\n{patch}"
        )
        source = await gh.file_text(repository, path, head_sha)
        if source is not None:
            parts.append(
                f"\n=== HEAD SOURCE {path} ===\n"
                f"{_bounded(source, policy.max_file_bytes)}"
            )
    return ReviewContext(subject, _trim(parts, policy.max_context_bytes), policy)


async def build_issue_context(
    gh: GitHubAppClient,
    repository: str,
    number: int,
    policy: RepoPolicy,
) -> ReviewContext:
    issue = await gh.issue(repository, number)
    head_sha, tree_sha = await gh.default_head(repository)
    body = issue.get("body") or ""
    subject = Subject(
        repository=repository,
        kind="ISSUE",
        number=number,
        head_sha=head_sha,
        title=issue.get("title") or f"Issue #{number}",
        url=issue["html_url"],
    )
    paths = await gh.tree_paths(repository, tree_sha)
    chosen = select_issue_paths(
        paths,
        issue.get("title", "") + "\n" + body,
        policy.max_files,
    )
    parts = [
        f"SUBJECT: issue #{number}",
        f"REPOSITORY: {repository}",
        f"HEAD_SHA: {head_sha}",
        f"TITLE: {issue.get('title', '')}",
        f"ISSUE BODY:\n{body}",
        "\nSELECTED REPOSITORY CONTEXT:",
    ]
    for path in chosen:
        source = await gh.file_text(repository, path, head_sha)
        if source is not None:
            parts.append(
                f"\n=== SOURCE {path} ===\n"
                f"{_bounded(source, policy.max_file_bytes)}"
            )
    return ReviewContext(subject, _trim(parts, policy.max_context_bytes), policy)


async def build_sweep_context(
    gh: GitHubAppClient,
    repository: str,
    policy: RepoPolicy,
) -> ReviewContext:
    head_sha, tree_sha = await gh.default_head(repository)
    subject = Subject(
        repository=repository,
        kind="SWEEP",
        head_sha=head_sha,
        title="Repository defect discovery sweep",
        url=f"https://github.com/{repository}",
    )
    paths = await gh.tree_paths(repository, tree_sha)
    chosen = select_sweep_paths(paths, policy.max_files)
    parts = [
        "SUBJECT: repository-wide bounded defect discovery sweep",
        f"REPOSITORY: {repository}",
        f"HEAD_SHA: {head_sha}",
        (
            "Only selected files below are in scope. Absence of a finding is not proof "
            "that the repository is defect-free."
        ),
    ]
    for path in chosen:
        source = await gh.file_text(repository, path, head_sha)
        if source is not None:
            parts.append(
                f"\n=== SOURCE {path} ===\n"
                f"{_bounded(source, policy.max_file_bytes)}"
            )
    return ReviewContext(subject, _trim(parts, policy.max_context_bytes), policy)
