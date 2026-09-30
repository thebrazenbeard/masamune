from masamune.context import _bounded


def test_obvious_github_token_is_redacted() -> None:
    token = "ghp_" + "A" * 36
    result = _bounded(f"token={token}", 30_000)
    assert token not in result
    assert "[REDACTED_POTENTIAL_SECRET]" in result


def test_private_key_block_is_redacted() -> None:
    value = (
        "-----BEGIN PRIVATE KEY-----\n"
        "abc123\n"
        "-----END PRIVATE KEY-----"
    )
    result = _bounded(value, 30_000)
    assert "abc123" not in result
    assert "[REDACTED_POTENTIAL_SECRET]" in result


def test_file_is_bounded() -> None:
    result = _bounded("x" * 100, 20)
    assert len(result) < 100
    assert "TRUNCATED" in result


def test_invisible_unicode_is_made_visible() -> None:
    result = _bounded("safe\u202Ehidden", 30_000)
    assert "\u202e" not in result
    assert "[MASAMUNE INVISIBLE U+202E]" in result
