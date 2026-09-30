from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Command:
    kind: Literal["INVESTIGATE", "SWEEP"]
    issue_number: int | None = None


_INVESTIGATE = re.compile(
    r"(?im)^\s*/masamune\s+investigate(?:\s+#?(\d+))?\s*$"
)
_SWEEP = re.compile(r"(?im)^\s*/masamune\s+sweep\s*$")


def parse_command(text: str) -> Command | None:
    match = _INVESTIGATE.search(text)
    if match:
        issue = int(match.group(1)) if match.group(1) else None
        return Command("INVESTIGATE", issue)
    if _SWEEP.search(text):
        return Command("SWEEP")
    return None
