from __future__ import annotations

from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class RepoPolicy:
    enabled: bool = True
    review_pull_requests: bool = True
    allow_external_pull_requests: bool = False
    allow_issue_commands: bool = True
    allow_sweep: bool = True
    post_unresolved: bool = False
    max_files: int = 40
    max_file_bytes: int = 30_000
    max_context_bytes: int = 180_000

    def __post_init__(self) -> None:
        if not 1 <= self.max_files <= 200:
            raise ValueError("max_files must be between 1 and 200")
        if not 2_000 <= self.max_file_bytes <= 200_000:
            raise ValueError("max_file_bytes must be between 2000 and 200000")
        if not 10_000 <= self.max_context_bytes <= 1_000_000:
            raise ValueError(
                "max_context_bytes must be between 10000 and 1000000"
            )


def load_policy(text: str | None) -> RepoPolicy:
    if not text:
        return RepoPolicy()
    raw = yaml.safe_load(text) or {}
    cfg = raw.get("masamune", raw)
    if not isinstance(cfg, dict):
        raise TypeError(".masamune.yml must contain a mapping")
    allowed = {field for field in RepoPolicy.__dataclass_fields__}
    unknown = set(cfg) - allowed
    if unknown:
        raise ValueError(f"unknown Masamune policy keys: {sorted(unknown)}")
    return RepoPolicy(**cfg)
