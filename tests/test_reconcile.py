from masamune.models import (
    Challenge,
    Finding,
    FindingKind,
    LaneReport,
    Severity,
    Subject,
)
from masamune.reconcile import reconcile


def finding(identifier: str, confidence: float = 0.9) -> Finding:
    return Finding(
        id=identifier,
        title="Retry can duplicate the effect",
        kind=FindingKind.BUG,
        severity=Severity.HIGH,
        confidence=confidence,
        file="src/retry.py",
        evidence=["response loss path retries without idempotency key"],
        mechanism="A committed remote effect can be replayed after response loss.",
    )


def lanes() -> tuple[LaneReport, LaneReport]:
    masa = LaneReport(
        lane="MASA",
        provider_id="provider-a",
        model_id="model-a",
        findings=[finding("M-001")],
    )
    mune = LaneReport(
        lane="MUNE",
        provider_id="provider-b",
        model_id="model-b",
        findings=[],
    )
    return masa, mune


def subject() -> Subject:
    return Subject(
        repository="owner/repo",
        kind="PULL_REQUEST",
        number=7,
        head_sha="a" * 40,
        base_sha="b" * 40,
        title="Fix retry",
        url="https://github.com/owner/repo/pull/7",
    )


def test_confirm_requires_challenge_evidence() -> None:
    masa, mune = lanes()
    report = reconcile(
        subject(),
        masa,
        mune,
        [Challenge(
            finding_id="M-001",
            verdict="CONFIRM",
            rationale="Mechanism is reachable.",
            evidence=["call path reaches retry after ambiguous response"],
        )],
    )
    assert [item.id for item in report.confirmed] == ["M-001"]
    assert report.unresolved == []


def test_bare_agreement_is_not_confirmation() -> None:
    masa, mune = lanes()
    report = reconcile(
        subject(),
        masa,
        mune,
        [Challenge(
            finding_id="M-001",
            verdict="CONFIRM",
            rationale="I agree.",
            evidence=[],
        )],
    )
    assert report.confirmed == []
    assert [item.id for item in report.unresolved] == ["M-001"]


def test_rejection_is_preserved() -> None:
    masa, mune = lanes()
    report = reconcile(
        subject(),
        masa,
        mune,
        [Challenge(
            finding_id="M-001",
            verdict="REJECT",
            rationale="The caller supplies an idempotency key.",
            evidence=["src/caller.py passes request_id"],
        )],
    )
    assert report.rejected_ids == ["M-001"]
