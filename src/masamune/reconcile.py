from __future__ import annotations

from copy import deepcopy

from .models import Challenge, Finding, LaneReport, ReviewReport, Subject


def reconcile(
    subject: Subject,
    masa: LaneReport,
    mune: LaneReport,
    challenges: list[Challenge],
    *,
    scope_note: str | None = None,
) -> ReviewReport:
    by_id: dict[str, Challenge] = {}
    for challenge in challenges:
        by_id.setdefault(challenge.finding_id, challenge)

    confirmed: list[Finding] = []
    narrowed: list[Finding] = []
    unresolved: list[Finding] = []
    rejected: list[str] = []

    masa_ids = {finding.id for finding in masa.findings}
    for finding in masa.findings:
        challenge = by_id.get(finding.id)
        if challenge is None:
            unresolved.append(finding)
            continue

        if challenge.verdict == "REJECT":
            rejected.append(finding.id)
            continue

        if challenge.verdict == "CONFIRM":
            if finding.confidence >= 0.65 and challenge.evidence:
                confirmed_finding = deepcopy(finding)
                confirmed_finding.evidence.extend(
                    f"Mune verification: {item}" for item in challenge.evidence
                )
                confirmed.append(confirmed_finding)
            else:
                unresolved.append(finding)
            continue

        if challenge.verdict == "NARROW":
            narrowed_finding = deepcopy(finding)
            if challenge.narrowed_title:
                narrowed_finding.title = challenge.narrowed_title
            narrowed_finding.confidence = min(narrowed_finding.confidence, 0.85)
            narrowed_finding.evidence.extend(
                f"Mune verification: {item}" for item in challenge.evidence
            )
            narrowed.append(narrowed_finding)
            continue

        unresolved.append(finding)

    # Mune's blind-only findings are useful, but they have not survived a second
    # independent challenge. Preserve them as unresolved rather than promoting them.
    for finding in mune.findings:
        if finding.id not in masa_ids and finding.confidence >= 0.60:
            unresolved.append(finding)

    return ReviewReport(
        subject=subject,
        masa=masa,
        mune=mune.model_copy(update={"challenges": challenges}),
        confirmed=confirmed,
        narrowed=narrowed,
        unresolved=unresolved,
        rejected_ids=rejected,
        scope_note=scope_note,
    )
