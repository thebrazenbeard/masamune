from __future__ import annotations

import re
from collections import defaultdict

_CODE_EXTENSIONS = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java",
    ".kt", ".kts", ".rb", ".php", ".cs", ".cpp", ".cc", ".c", ".h", ".hpp",
    ".sql", ".sh", ".ps1", ".yaml", ".yml", ".toml", ".json",
}
_RISK_WORDS = {
    "auth", "security", "permission", "payment", "billing", "retry", "queue",
    "cache", "state", "migration", "database", "db", "session", "token",
    "worker", "api", "webhook", "transaction", "lock", "concurrent", "config",
}


def is_code_path(path: str) -> bool:
    lower = path.lower()
    segments = set(lower.replace("\\", "/").split("/"))
    if segments & {"vendor", "node_modules", "dist", "build"}:
        return False
    return any(lower.endswith(ext) for ext in _CODE_EXTENSIONS)


def select_issue_paths(paths: list[str], issue_text: str, limit: int) -> list[str]:
    terms = {
        token for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", issue_text.lower())
        if len(token) >= 4
    }
    scored: list[tuple[int, str]] = []
    for path in paths:
        if not is_code_path(path):
            continue
        lower = path.lower()
        score = sum(3 for term in terms if term in lower)
        score += sum(1 for risk in _RISK_WORDS if risk in lower)
        scored.append((score, path))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return _diversify([path for _, path in scored], limit)


def select_sweep_paths(paths: list[str], limit: int) -> list[str]:
    scored: list[tuple[int, str]] = []
    for path in paths:
        if not is_code_path(path):
            continue
        lower = path.lower()
        score = sum(2 for risk in _RISK_WORDS if risk in lower)
        if "/test" not in lower and "spec" not in lower:
            score += 1
        scored.append((score, path))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return _diversify([path for _, path in scored], limit)


def _diversify(paths: list[str], limit: int) -> list[str]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        root = path.split("/", 1)[0]
        buckets[root].append(path)
    chosen: list[str] = []
    while len(chosen) < limit and buckets:
        for root in sorted(buckets):
            if buckets[root]:
                chosen.append(buckets[root].pop(0))
                if len(chosen) == limit:
                    break
            if not buckets[root]:
                del buckets[root]
    return chosen
