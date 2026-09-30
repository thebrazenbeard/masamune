import pytest
from pydantic import ValidationError

from masamune.models import Finding, FindingKind, LaneReport, Severity


def test_lane_rejects_duplicate_finding_ids() -> None:
    finding = Finding(
        id="M-001",
        title="example",
        kind=FindingKind.BUG,
        severity=Severity.MEDIUM,
        confidence=0.7,
        evidence=["evidence"],
        mechanism="mechanism",
    )
    with pytest.raises(ValidationError, match="finding IDs must be unique"):
        LaneReport(
            lane="MASA",
            provider_id="provider",
            model_id="model",
            findings=[finding, finding.model_copy()],
        )
