from masamune.models import LaneReport, ReviewReport, Subject
from masamune.render import render_report


def test_report_contains_idempotency_marker() -> None:
    subject = Subject(
        repository="owner/repo",
        kind="PULL_REQUEST",
        number=1,
        head_sha="a" * 40,
        base_sha="b" * 40,
        title="PR",
        url="https://github.com/owner/repo/pull/1",
    )
    report = ReviewReport(
        subject=subject,
        masa=LaneReport(
            lane="MASA", provider_id="a", model_id="x", findings=[]
        ),
        mune=LaneReport(
            lane="MUNE", provider_id="b", model_id="y", findings=[]
        ),
        confirmed=[],
        narrowed=[],
        unresolved=[],
        rejected_ids=[],
    )
    body = render_report(report, "review-123")
    assert "<!-- masamune-review:review-123 -->" in body
    assert "not" in body.lower()
    assert "defect-free" in body
