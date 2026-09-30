import pytest

from masamune.policy import RepoPolicy, load_policy


def test_default_policy() -> None:
    assert load_policy(None) == RepoPolicy()


def test_nested_policy() -> None:
    policy = load_policy(
        """
masamune:
  allow_sweep: false
  max_files: 12
"""
    )
    assert policy.allow_sweep is False
    assert policy.max_files == 12


def test_unknown_policy_key_fails_closed() -> None:
    with pytest.raises(ValueError, match="unknown Masamune policy keys"):
        load_policy("masamune:\n  execute_arbitrary_code: true\n")


def test_policy_bounds_fail_closed() -> None:
    with pytest.raises(ValueError, match="max_files"):
        load_policy("masamune:\n  max_files: 0\n")
