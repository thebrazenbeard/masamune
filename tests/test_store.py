from masamune.store import DeliveryStore


def test_delivery_is_admitted_once(tmp_path) -> None:
    store = DeliveryStore(tmp_path / "state.sqlite3")
    first = store.claim("d1", "pull_request", "abc")
    second = store.claim("d1", "pull_request", "abc")
    assert first.accepted is True
    assert second.accepted is False
    assert second.state == "ACCEPTED"


def test_failed_delivery_can_be_retried(tmp_path) -> None:
    store = DeliveryStore(tmp_path / "state.sqlite3")
    store.claim("d1", "pull_request", "abc")
    store.mark("d1", "FAILED", "boom")
    retry = store.claim("d1", "pull_request", "abc")
    assert retry.accepted is True
    assert retry.state == "ACCEPTED"


def test_delivery_id_cannot_change_payload_identity(tmp_path) -> None:
    store = DeliveryStore(tmp_path / "state.sqlite3")
    store.claim("d1", "pull_request", "abc")
    conflict = store.claim("d1", "pull_request", "different")
    assert conflict.accepted is False
    assert conflict.state == "CONFLICT"
