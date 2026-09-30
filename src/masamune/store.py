from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DeliveryClaim:
    accepted: bool
    state: str


class DeliveryStore:
    """Small durable webhook ledger.

    A GitHub delivery ID is admitted exactly once. Processing state is explicit so a
    crash is observable instead of silently causing the same external effect twice.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=30000")
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS webhook_delivery (
                    delivery_id TEXT PRIMARY KEY,
                    event_name TEXT NOT NULL,
                    state TEXT NOT NULL,
                    received_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    payload_sha256 TEXT NOT NULL,
                    error TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS review_receipt (
                    review_id TEXT PRIMARY KEY,
                    delivery_id TEXT NOT NULL,
                    repository TEXT NOT NULL,
                    subject_kind TEXT NOT NULL,
                    subject_number INTEGER,
                    head_sha TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(delivery_id) REFERENCES webhook_delivery(delivery_id)
                )
                """
            )

    def claim(self, delivery_id: str, event_name: str, payload_sha256: str) -> DeliveryClaim:
        now = datetime.now(UTC).isoformat()
        with self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO webhook_delivery
                    (delivery_id, event_name, state, received_at, updated_at, payload_sha256)
                    VALUES (?, ?, 'ACCEPTED', ?, ?, ?)
                    """,
                    (delivery_id, event_name, now, now, payload_sha256),
                )
                return DeliveryClaim(True, "ACCEPTED")
            except sqlite3.IntegrityError:
                row = conn.execute(
                    """
                    SELECT state, updated_at, event_name, payload_sha256
                    FROM webhook_delivery
                    WHERE delivery_id = ?
                    """,
                    (delivery_id,),
                ).fetchone()
                state = row["state"] if row else "UNKNOWN"
                if row and (
                    row["event_name"] != event_name
                    or row["payload_sha256"] != payload_sha256
                ):
                    return DeliveryClaim(False, "CONFLICT")
                stale_processing = False
                if row and state == "PROCESSING":
                    updated = datetime.fromisoformat(row["updated_at"])
                    stale_processing = (
                        datetime.now(UTC) - updated
                    ).total_seconds() >= 900
                if state in {"FAILED", "READY_TO_PUBLISH"} or stale_processing:
                    conn.execute(
                        """
                        UPDATE webhook_delivery
                        SET state = 'ACCEPTED', updated_at = ?, error = NULL
                        WHERE delivery_id = ?
                        """,
                        (now, delivery_id),
                    )
                    return DeliveryClaim(True, "ACCEPTED")
                return DeliveryClaim(False, state)

    def mark(self, delivery_id: str, state: str, error: str | None = None) -> None:
        now = datetime.now(UTC).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE webhook_delivery
                SET state = ?, updated_at = ?, error = ?
                WHERE delivery_id = ?
                """,
                (state, now, error, delivery_id),
            )

    def save_review(
        self,
        review_id: str,
        delivery_id: str,
        repository: str,
        subject_kind: str,
        subject_number: int | None,
        head_sha: str,
        result: dict[str, Any],
    ) -> None:
        now = datetime.now(UTC).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO review_receipt
                (review_id, delivery_id, repository, subject_kind, subject_number,
                 head_sha, result_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    review_id,
                    delivery_id,
                    repository,
                    subject_kind,
                    subject_number,
                    head_sha,
                    json.dumps(result, sort_keys=True, separators=(",", ":")),
                    now,
                ),
            )
