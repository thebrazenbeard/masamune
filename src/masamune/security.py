from __future__ import annotations

import hashlib
import hmac


def verify_github_signature(secret: str, body: bytes, signature: str | None) -> bool:
    if not secret or not signature or not signature.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    supplied = signature.removeprefix("sha256=")
    return hmac.compare_digest(expected, supplied)
