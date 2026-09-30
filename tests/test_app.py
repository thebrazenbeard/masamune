import hashlib
import hmac
import json

from fastapi.testclient import TestClient

import masamune.app as app_module
from masamune.settings import Settings


def signature(secret: str, body: bytes) -> str:
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def test_webhook_rejects_invalid_signature(monkeypatch, tmp_path) -> None:
    settings = Settings(
        github_webhook_secret="secret",
        state_db_path=str(tmp_path / "state.sqlite3"),
        require_independence=False,
    )
    monkeypatch.setattr(app_module, "get_settings", lambda: settings)
    client = TestClient(app_module.app)
    response = client.post(
        "/webhook/github",
        content=b"{}",
        headers={
            "X-GitHub-Event": "ping",
            "X-GitHub-Delivery": "d1",
            "X-Hub-Signature-256": "sha256=wrong",
        },
    )
    assert response.status_code == 401


def test_webhook_claims_delivery_once(monkeypatch, tmp_path) -> None:
    settings = Settings(
        github_webhook_secret="secret",
        state_db_path=str(tmp_path / "state.sqlite3"),
        require_independence=False,
    )
    monkeypatch.setattr(app_module, "get_settings", lambda: settings)
    client = TestClient(app_module.app)
    body = json.dumps({"zen": "hello"}).encode()
    headers = {
        "X-GitHub-Event": "ping",
        "X-GitHub-Delivery": "d1",
        "X-Hub-Signature-256": signature("secret", body),
        "Content-Type": "application/json",
    }
    first = client.post("/webhook/github", content=body, headers=headers)
    second = client.post("/webhook/github", content=body, headers=headers)
    assert first.status_code == 200
    assert first.json()["status"] == "accepted"
    assert second.json()["status"] == "duplicate"
