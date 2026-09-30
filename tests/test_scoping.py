from masamune.scoping import is_code_path, select_issue_paths, select_sweep_paths


def test_code_path_excludes_dependencies() -> None:
    assert is_code_path("src/auth/token.py")
    assert not is_code_path("node_modules/pkg/index.js")
    assert not is_code_path("docs/design.md")


def test_issue_selection_prefers_related_path() -> None:
    paths = [
        "src/payments/retry.py",
        "src/users/profile.py",
        "tests/test_retry.py",
    ]
    selected = select_issue_paths(paths, "duplicate payment on retry", 2)
    assert "src/payments/retry.py" in selected


def test_sweep_prioritizes_risk_surfaces() -> None:
    paths = ["src/ui/theme.py", "src/auth/token.py", "src/cache/state.py"]
    selected = select_sweep_paths(paths, 2)
    assert "src/auth/token.py" in selected or "src/cache/state.py" in selected
