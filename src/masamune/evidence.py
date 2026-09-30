from __future__ import annotations

import hashlib
import re
from enum import StrEnum

from pydantic import BaseModel, Field

from .models import EvidenceQuality, EvidenceReceipt, Finding, LaneReport


_CONTEXT_HEADER = re.compile(r"^=== (?:HEAD SOURCE|SOURCE|DIFF) (.+?) ===$", re.MULTILINE)


def _normal(path: str) -> str:
    return path.replace("\\", "/").strip()


def _sections(context: str) -> dict[str, str]:
    matches = list(_CONTEXT_HEADER.finditer(context))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        path = _normal(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(context)
        result[path] = context[start:end].strip()
    return result


def audit_finding(finding: Finding, lane: str, context: str) -> EvidenceReceipt:
    context_hash = hashlib.sha256(context.encode("utf-8")).hexdigest()
    sections = _sections(context)
    path = _normal(finding.file) if finding.file else None

    if path and path in sections:
        section = sections[path]
        source_hash = hashlib.sha256(section.encode("utf-8")).hexdigest()
        truncated = "[MASAMUNE FILE/PATCH TRUNCATED]" in section or "[MASAMUNE CONTEXT TRUNCATED" in section
        if finding.line and not truncated:
            lines = section.splitlines()
            if 1 <= finding.line <= len(lines):
                return EvidenceReceipt(
                    finding_id=finding.id,
                    lane=lane,
                    quality=EvidenceQuality.EXACT_FILE_LINE,
                    file=path,
                    line=finding.line,
                    source_sha256=source_hash,
                    context_sha256=context_hash,
                    rationale="Cited file and line are present in an untruncated bounded context section.",
                )
        return EvidenceReceipt(
            finding_id=finding.id,
            lane=lane,
            quality=EvidenceQuality.EXACT_FILE,
            file=path,
            line=finding.line,
            source_sha256=source_hash,
            context_sha256=context_hash,
            rationale="Cited file is present in the bounded context, but the exact line cannot be established from the supplied section.",
        )

    for evidence in finding.evidence:
        if evidence and evidence in context:
            return EvidenceReceipt(
                finding_id=finding.id,
                lane=lane,
                quality=EvidenceQuality.CONTEXT_ONLY,
                file=path,
                line=finding.line,
                source_sha256=None,
                context_sha256=context_hash,
                rationale="Evidence text occurs directly in the bounded context without an exact file anchor.",
            )

    return EvidenceReceipt(
        finding_id=finding.id,
        lane=lane,
        quality=EvidenceQuality.MODEL_ASSERTION,
        file=path,
        line=finding.line,
        source_sha256=None,
        context_sha256=context_hash,
        rationale="No deterministic source anchor or exact context evidence was established.",
    )


def audit_reports(
    masa: LaneReport,
    mune: LaneReport,
    context: str,
) -> list[EvidenceReceipt]:
    receipts = [audit_finding(item, "MASA", context) for item in masa.findings]
    receipts.extend(audit_finding(item, "MUNE", context) for item in mune.findings)
    return receipts