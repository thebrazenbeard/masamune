import hashlib
import hmac

from masamune.security import verify_github_signature


def test_signature_verification() -> None:
    secret = "correct horse battery staple"
    body = b'{"hello":"world"}'
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_github_signature(secret, body, f"sha256={digest}")


def test_signature_rejects_bad_value() -> None:
    assert not verify_github_signature("secret", b"body", "sha256=deadbeef")
    assert not verify_github_signature("", b"body", "sha256=deadbeef")
    assert not verify_github_signature("secret", b"body", None)
