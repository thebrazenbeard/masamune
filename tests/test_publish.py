from __future__ import annotations

from masamune.app import _publish_review
from masamune.context import ReviewContext
from masamune.models import LaneReport, ReviewReport, Subject
from masamune.policy import RepoPolicy
from masamune.store import DeliveryStore


class FakeGitHub:
    def __init__(self) -> None:
        self.comments: list[str] = []

    async def has_comment_marker(
        self, repository: str, issue_number: int, marker: str
    ) -> bool:
        return any(marker in body for body in self.comments)

    async def comment(
        self, repository: str, issue_number: int, body: str
    ) -> dict[str, int]:
        self.comments.append(body)
        return {"id": len(self.comments)}


class FakeOrchestrator:
    def __init__(self, report: ReviewReport) -> None:
        self.report = report
        self.calls = 0

    async def review(self, context: ReviewContext) -> ReviewReport:
        self.calls += 1
        return self.report


def make_context() -> ReviewContext:
    subject = Subject(
        repository="owner/repo",
        kind="PULL_REQUEST",
        number=7,
        head_sha="a" * 40,
        base_sha="b" * 40,
        title="Test",
        url="https://github.com/owner/repo/pull/7",
    )
    return ReviewContext(subject, "bounded exact context", RepoPolicy())


def make_report(context: ReviewContext) -> ReviewReport:
    return ReviewReport(
        subject=context.subject,
        masa=LaneReport(
            lane="MASA", provider_id="a", model_id="m1", findings=[]
        ),
        mune=LaneReport(
            lane="MUNE", provider_id="b", model_id="m2", findings=[]
        ),
        confirmed=[],
        narrowed=[],
        unresolved=[],
        rejected_ids=[],
    )


async def test_publish_is_readback_verified_and_idempotent(tmp_path) -> None:
    context = make_context()
    report = make_report(context)
    gh = FakeGitHub()
    orchestrator = FakeOrchestrator(report)
    store = DeliveryStore(tmp_path / "state.sqlite3")
    store.claim("d1", "pull_request", "hash")
    store.mark("d1", "PROCESSING")

    await _publish_review(
        gh=gh,
        store=store,
        delivery_id="d1",
        context=context,
        anchor_issue=7,
        orchestrator=orchestrator,
    )
    assert len(gh.comments) == 1
    assert orchestrator.calls == 1

    # A new delivery for the same exact subject should see the deterministic
    # marker before model execution and avoid both spend and duplicate effects.
    store.claim("d2", "pull_request", "hash2")
    store.mark("d2", "PROCESSING")
    await _publish_review(
        gh=gh,
        store=store,
        delivery_id="d2",
        context=context,
        anchor_issue=7,
        orchestrator=orchestrator,
    )
    assert len(gh.comments) == 1
    assert orchestrator.calls == 1
