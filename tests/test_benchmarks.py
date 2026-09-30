import json
from pathlib import Path


def test_benchmark_manifest_is_self_consistent() -> None:
    root = Path(__file__).parents[1]
    manifest = json.loads((root / "benchmarks/cases.json").read_text())
    assert manifest["version"] == "0.1"
    assert manifest["cases"]
    for case in manifest["cases"]:
        fixture = root / case["path"]
        assert fixture.is_file(), case["id"]
        expected = case["expected"]
        assert expected["kind"]
        assert expected["anchor"] in fixture.read_text()
        assert expected["mechanism_contains"]