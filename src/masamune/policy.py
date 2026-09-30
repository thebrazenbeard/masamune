from __future__ import annotations

import yaml
from pydantic import BaseModel, ConfigDict, Field


class RepoPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    enabled: bool = True
    review_pull_requests: bool = True
    allow_external_pull_requests: bool = False
    allow_issue_commands: bool = True
    allow_sweep: bool = True
    post_unresolved: bool = False
    max_files: int = Field(default=40, ge=1, le=200)
    max_file_bytes: int = Field(default=30_000, ge=2_000, le=200_000)
    max_context_bytes: int = Field(default=180_000, ge=10_000, le=1_000_000)


def load_policy(text: str | None) -> RepoPolicy:
    if not text:
        return RepoPolicy()
    raw = yaml.safe_load(text)
    if raw is None:
        return RepoPolicy()
    if not isinstance(raw, dict):
        raise TypeError(".masamune.yml must contain a mapping")
    cfg = raw.get("masamune", raw)
    if not isinstance(cfg, dict):
        raise TypeError("masamune policy must contain a mapping")
    unknown = set(cfg) - set(RepoPolicy.model_fields)
    if unknown:
        raise ValueError(f"unknown Masamune policy keys: {sorted(unknown)}")
    return RepoPolicy.model_validate(cfg)
