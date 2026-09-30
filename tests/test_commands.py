from masamune.commands import parse_command


def test_investigate_explicit_issue() -> None:
    command = parse_command("/masamune investigate #417")
    assert command is not None
    assert command.kind == "INVESTIGATE"
    assert command.issue_number == 417


def test_investigate_current_issue() -> None:
    command = parse_command("hello\n/masamune investigate\n")
    assert command is not None
    assert command.kind == "INVESTIGATE"
    assert command.issue_number is None


def test_sweep() -> None:
    command = parse_command("/masamune sweep")
    assert command is not None
    assert command.kind == "SWEEP"


def test_random_text_is_not_command() -> None:
    assert parse_command("please investigate this") is None
