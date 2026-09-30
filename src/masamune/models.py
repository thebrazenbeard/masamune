from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class EvidenceQuality(StrEnum):
    EXACT_FILE_LINE = "EXACT_FILE_LINE"
    EXACT_FILE = "EXACT_FILE"
    CONTEXT_ONLY = "CONTEXT_ONLY"
    MODEL_ASSERTION = "MODEL_ASSERTION"


class Severity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FindingKind(StrEnum):
    BUG = "BUG"
    REGRESSION_RISK = "REGRESSION_RISK"
    SECURITY = "SECURITY_CONCERN"
    DESIGN = "DESIGN_WEAKNESS"
    TESTING = "TESTING_GAP"
    PERFORMANCE = "PERFORMANCE_OPPORTUNITY"
    MAINTAINABILITY = "MAINTAINABILITY_IMPROVEMENT"
    SPECULATIVE = "SPECULATIVE_NEEDS_VALIDATION"


class Finding(BaseModel):
    id: str = Field(min_length=3, max_length=80)
    title: str = Field(min_length=3, max_length=180)
    kind: FindingKind
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    file: str | None = None
    line: int | None = Field(default=None, ge=1)
    evidence: list[str] = Field(default_factory=list, max_length=8)
    mechanism: str = Field(min_length=1, max_length=4000)
    suggestion: str | None = Field(default=None, max_length=4000)


class Challenge(BaseModel):
    finding_id: str
    verdict: Literal["CONFIRM", "REJECT", "NARROW", "UNRESOLVED"]
    rationale: str = Field(min_length=1, max_length=4000)
    evidence: list[str] = Field(default_factory=list, max_length=8)
    narrowed_title: str | None = Field(default=None, max_length=180)


class LaneReport(BaseModel):
    lane: Literal["MASA", "MUNE"]
    provider_id: str
    model_id: str
    findings: list[Finding] = Field(default_factory=list, max_length=30)
    challenges: list[Challenge] = Field(default_factory=list, max_length=30)
    notes: list[str] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def unique_finding_ids(self) -> LaneReport:
        identifiers = [finding.id for finding in self.findings]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("finding IDs must be unique within a lane report")
        return self


class Subject(BaseModel):
    repository: str
    kind: Literal["PULL_REQUEST", "ISSUE", "SWEEP"]
    number: int | None = None
    head_sha: str
    base_sha: str | None = None
    title: str
    url: str


class EvidenceReceipt(BaseModel):
    finding_id: str
    lane: str
    quality: EvidenceQuality
    file: str | None = None
    line: int | None = Field(default=None, ge=1)
    source_sha256: str | None = None
    context_sha256: str
    rationale: str


class ReviewReport(BaseModel):
    subject: Subject
    masa: LaneReport
    mune: LaneReport
    confirmed: list[Finding]
    narrowed: list[Finding]
    unresolved: list[Finding]
    rejected_ids: list[str]
    evidence_receipts: list[EvidenceReceipt] = Field(default_factory=list)
    skeptic_flags: list[str] = Field(default_factory=list, max_length=50)
    scope_note: str | None = None
