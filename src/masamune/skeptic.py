from __future__ import annotations

from .models import EvidenceQuality, EvidenceReceipt, LaneReport, Challenge


def skeptic_flags(
    masa: LaneReport,
    mune: LaneReport,
    challenges: list[Challenge],
    receipts: list[EvidenceReceipt],
) -> list[str]:
    flags: list[str] = []
    masa_ids = {finding.id for finding in masa.findings}
    mune_ids = {finding.id for finding in mune.findings}
    if masa_ids & mune_ids:
        flags.append("CROSS_LANE_FINDING_ID_COLLISION")

    challenged_ids = {challenge.finding_id for challenge in challenges}
    missing = sorted(masa_ids - challenged_ids)
    if missing:
        flags.append("CHALLENGE_COVERAGE_GAP:" + ",".join(missing[:10]))

    extra = sorted(challenged_ids - masa_ids)
    if extra:
        flags.append("CHALLENGE_FOR_UNKNOWN_FINDING:" + ",".join(extra[:10]))

    receipt_by_id = {receipt.finding_id: receipt for receipt in receipts}
    for finding in masa.findings:
        receipt = receipt_by_id.get(finding.id)
        if receipt is None:
            flags.append(f"MISSING_EVIDENCE_RECEIPT:{finding.id}")
        elif receipt.quality == EvidenceQuality.MODEL_ASSERTION:
            flags.append(f"MODEL_ONLY_EVIDENCE:{finding.id}")
        elif finding.severity.value in {"HIGH", "CRITICAL"} and receipt.quality == EvidenceQuality.CONTEXT_ONLY:
            flags.append(f"HIGH_SEVERITY_WEAK_ANCHOR:{finding.id}")

    if masa.provider_id == mune.provider_id:
        flags.append("SHARED_PROVIDER")
    if masa.model_id == mune.model_id:
        flags.append("SHARED_MODEL")

    return flags