from __future__ import annotations

import asyncio
import hashlib

from .context import ReviewContext
from .llm import OpenAICompatibleModel
from .models import ReviewReport
from .reconcile import reconcile
from .settings import Settings


def review_id_for(context: ReviewContext) -> str:
    subject = context.subject
    raw = (
        f"{subject.repository}|{subject.kind}|{subject.number}|"
        f"{subject.base_sha}|{subject.head_sha}"
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


class MasamuneOrchestrator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.masa = OpenAICompatibleModel(
            base_url=settings.masa_base_url,
            api_key=settings.masa_api_key,
            provider_id=settings.masa_provider_id,
            model_id=settings.masa_model,
            timeout=settings.request_timeout_seconds,
            max_output_tokens=settings.model_max_output_tokens,
        )
        self.mune = OpenAICompatibleModel(
            base_url=settings.mune_base_url,
            api_key=settings.mune_api_key,
            provider_id=settings.mune_provider_id,
            model_id=settings.mune_model,
            timeout=settings.request_timeout_seconds,
            max_output_tokens=settings.model_max_output_tokens,
        )

    async def review(self, context: ReviewContext) -> ReviewReport:
        # Both first passes start from the same exact evidence and neither sees the
        # other's output. This is the independence boundary for the first pass.
        masa_report, mune_blind = await asyncio.gather(
            self.masa.masa_scan(context.text),
            self.mune.mune_blind_scan(context.text),
        )
        challenges = await self.mune.mune_challenge(
            context.text,
            mune_blind,
            masa_report,
        )
        scope_note = (
            f"Bounded review: at most {context.policy.max_files} selected files and "
            f"{context.policy.max_context_bytes} UTF-8 bytes of source/diff context. "
            "A missing finding is not evidence of absence."
        )
        return reconcile(
            context.subject,
            masa_report,
            mune_blind,
            challenges,
            scope_note=scope_note,
        )
