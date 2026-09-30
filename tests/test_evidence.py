from masamune.evidence import EvidenceQuality, audit_finding
from masamune.models import Finding, FindingKind, Severity


def make_finding(*, file: str | None, line: int | None, evidence: list[str]) -> Finding:
    return Finding(
        id="M-001",
        title="retry can duplicate effect",
        kind=FindingKind.BUG,
        severity=Severity.HIGH,
        confidence=0.9,
        file=file,
        line=line,
        evidence=evidence,
        mechanism="response loss can replay the remote effect",
    )


def test_exact_file_line_receipt() -> None:
    context = "=== HEAD SOURCE src/retry.py ===\nline one\nline two\n"
    receipt = audit_finding(
        make_finding(file="src/retry.py", line=2, evidence=[]),
        "MASA",
        context,
    )
    assert receipt.quality == EvidenceQuality.EXACT_FILE_LINE
    assert receipt.source_sha256
    assert receipt.context_sha256


def test_truncated_source_cannot_claim_exact_line() -> None:
    context = "=== HEAD SOURCE src/retry.py ===\nline one\n[MASAMUNE FILE/PATCH TRUNCATED]\n"
    receipt = audit_finding(
        make_finding(file="src/retry.py", line=2, evidence=[]),
        "MASA",
        context,
    )
    assert receipt.quality == EvidenceQuality.EXACT_FILE


def test_missing_file_is_model_assertion() -> None:
    context = "=== HEAD SOURCE src/other.py ===\nreturn safe\n"
    receipt = audit_finding(
        make_finding(file="src/retry.py", line=4, evidence=["retries without key"]),
        "MASA",
        context,
    )
    assert receipt.quality == EvidenceQuality.MODEL_ASSERTION


def test_context_only_evidence_is_distinguished() -> None:
    context = "=== SOURCE issue.txt ===\nretries without key\n"
    receipt = audit_finding(
        make_finding(file=None, line=None, evidence=["retries without key"]),
        "MASA",
        context,
    )
    assert receipt.quality == EvidenceQuality.CONTEXT_ONLY

def test_diff_line_is_not_source_line_evidence() -> None:
    context = "=== DIFF src/retry.py ===\n@@ -1 +1 @@\n+dangerous retry\n"
    receipt = audit_finding(
        make_finding(file="src/retry.py", line=1, evidence=[]),
        "MASA",
        context,
    )
    assert receipt.quality == EvidenceQuality.EXACT_FILE
