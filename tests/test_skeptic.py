from masamune.skeptic import skeptic_flags
from masamune.models import Challenge, EvidenceQuality, EvidenceReceipt, Finding, FindingKind, LaneReport, Severity


def make_finding(identifier: str = "M-001") -> Finding:
    return Finding(
        id=identifier,
        title="retry can duplicate effect",
        kind=FindingKind.BUG,
        severity=Severity.HIGH,
        confidence=0.9,
        file="src/retry.py",
        line=4,
        evidence=["remote effect can replay"],
        mechanism="response loss can trigger a second remote effect",
    )


def test_skeptic_flags_missing_challenge_and_evidence() -> None:
    masa = LaneReport(lane="MASA", provider_id="a", model_id="m1", findings=[make_finding()])
    mune = LaneReport(lane="MUNE", provider_id="b", model_id="m2", findings=[])
    flags = skeptic_flags(masa, mune, [], [])
    assert "CHALLENGE_COVERAGE_GAP:M-001" in flags
    assert "MISSING_EVIDENCE_RECEIPT:M-001" in flags


def test_skeptic_accepts_exact_evidence_and_complete_challenge() -> None:
    masa = LaneReport(lane="MASA", provider_id="a", model_id="m1", findings=[make_finding()])
    mune = LaneReport(lane="MUNE", provider_id="b", model_id="m2", findings=[])
    challenge = Challenge(
        finding_id="M-001",
        verdict="CONFIRM",
        rationale="reachable",
        evidence=["call path reaches retry"],
    )
    receipt = EvidenceReceipt(
        finding_id="M-001",
        lane="MASA",
        quality=EvidenceQuality.EXACT_FILE_LINE,
        file="src/retry.py",
        line=4,
        source_sha256="a" * 64,
        context_sha256="b" * 64,
        rationale="exact source anchor",
    )
    assert skeptic_flags(masa, mune, [challenge], [receipt]) == []