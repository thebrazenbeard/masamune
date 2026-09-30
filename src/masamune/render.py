from __future__ import annotations

from .models import EvidenceQuality, Finding, ReviewReport


def _safe_md(text: str) -> str:
    # Model output is untrusted. Avoid emitting hidden comments or unsolicited
    # GitHub @mentions from generated findings.
    return text.replace("<!--", "&lt;!--").replace("@", "@\u200b")


def _finding_block(finding: Finding) -> str:
    where = ""
    if finding.file:
        path = _safe_md(finding.file).replace("`", "")
        where = f" — `{path}"
        if finding.line:
            where += f":{finding.line}"
        where += "`"
    evidence = "\n".join(
        f"- {_safe_md(item)}" for item in finding.evidence[:5]
    )
    suggestion = (
        f"\n**Suggestion:** {_safe_md(finding.suggestion)}\n"
        if finding.suggestion
        else ""
    )
    return (
        f"### {finding.severity} · {finding.kind}\n"
        f"**{_safe_md(finding.title)}**{where}\n\n"
        f"{_safe_md(finding.mechanism)}\n\n"
        f"**Evidence:**\n{evidence or '- No specific evidence supplied.'}\n"
        f"{suggestion}"
    )


def render_report(
    report: ReviewReport,
    review_id: str,
    *,
    include_unresolved: bool = True,
) -> str:
    subject = report.subject
    marker = f"<!-- masamune-review:{review_id} -->"
    receipt_counts = {quality.value: 0 for quality in EvidenceQuality}
    for receipt in report.evidence_receipts:
        receipt_counts[receipt.quality.value] += 1
    lines = [
        marker,
        "## ⚔️ Masamune adversarial review",
        "",
        f"**Exact subject:** `{subject.repository}@{subject.head_sha}`",
        f"**Mode:** {subject.kind}",
        f"**Masa:** `{report.masa.provider_id}/{report.masa.model_id}`",
        f"**Mune:** `{report.mune.provider_id}/{report.mune.model_id}`",
        f"**Evidence audit:** exact line {receipt_counts["EXACT_FILE_LINE"]}, exact file {receipt_counts["EXACT_FILE"]}, context-only {receipt_counts["CONTEXT_ONLY"]}, model-only {receipt_counts["MODEL_ASSERTION"]}",
        "",
    ]

    if report.skeptic_flags:
        lines += ["## Skeptic gate", ""]
        for flag in report.skeptic_flags:
            lines += [f"- `{_safe_md(flag)}`"]
        lines += [""]

    if report.confirmed:
        lines += ["## Confirmed by Mune", ""]
        for finding in report.confirmed:
            lines += [_finding_block(finding), ""]

    if report.narrowed:
        lines += ["## Survives, narrowed", ""]
        for finding in report.narrowed:
            lines += [_finding_block(finding), ""]

    if report.unresolved and include_unresolved:
        lines += ["## Unresolved / needs validation", ""]
        for finding in report.unresolved[:12]:
            lines += [_finding_block(finding), ""]
    elif report.unresolved:
        lines += [
            f"_Policy withheld {len(report.unresolved)} unresolved hypothesis/hypotheses._",
            "",
        ]

    if not report.confirmed and not report.narrowed and not report.unresolved:
        lines += [
            "No reportable finding survived this bounded review.",
            "",
            "That is **not** proof that the subject is defect-free.",
            "",
        ]

    if report.rejected_ids:
        lines += [
            "<details>",
            "<summary>Rejected Masa hypotheses</summary>",
            "",
            ", ".join(f"`{item}`" for item in report.rejected_ids),
            "",
            "</details>",
            "",
        ]

    lines += [
        "---",
        report.scope_note
        or "Masamune reviewed only the evidence included in this exact run. "
        "Model agreement is not independent factual evidence.",
    ]
    return "\n".join(lines)
