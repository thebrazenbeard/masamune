"""Opt-in, read-only Masamune Supabase Edge readiness probe.

This checks the deployed health contract, not source/deployment equivalence,
webhook delivery, GitHub permissions, or reviewer/model execution.
"""

import argparse
import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


ENDPOINT = (
    "https://fawkirqroyniueeqspif.supabase.co/functions/v1/masamune-webhook"
)
PROJECT_REF = "fawkirqroyniueeqspif"
MAX_RESPONSE_BYTES = 8192
CONFIG_NAMES = frozenset({
    "MASAMUNE_GITHUB_APP_ID",
    "MASAMUNE_GITHUB_PRIVATE_KEY",
    "MASAMUNE_GITHUB_WEBHOOK_SECRET",
    "MASAMUNE_MASA_API_KEY",
    "MASAMUNE_MUNE_API_KEY",
})
READY_KEYS = frozenset({"status", "service", "runtime", "billing_mode"})
NOT_READY_KEYS = READY_KEYS | {"missing"}


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


@dataclass(frozen=True)
class ProbeResult:
    qualified: bool
    kind: str
    detail: str


def unique_object_pairs(pairs):
    """Reject duplicate JSON keys at every nesting depth.

    The deployed Edge v10 GET success body has *no* ``missing`` key; its
    not-ready body carries a nonempty ``missing`` array. Do not infer that
    absent, false, empty object, and empty list mean equivalent things.
    """
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key")
        obj[key] = value
    return obj


def classify(status: int, headers, body: bytes, effective_url: str) -> ProbeResult:
    """Fail closed on unexpected status, origin, provider, or payload."""
    if effective_url != ENDPOINT:
        return ProbeResult(False, "UNVERIFIED", "response URL differs from pinned endpoint")
    if headers.get("sb-project-ref") != PROJECT_REF:
        return ProbeResult(False, "UNVERIFIED", "provider project header mismatch")
    if len(body) > MAX_RESPONSE_BYTES:
        return ProbeResult(False, "UNVERIFIED", "response exceeded maximum size")
    try:
        payload = json.loads(body, object_pairs_hook=unique_object_pairs)
    except (ValueError, UnicodeDecodeError):
        return ProbeResult(False, "UNVERIFIED", "invalid JSON response")
    if not isinstance(payload, dict) or payload.get("service") != "masamune" or payload.get("runtime") != "supabase-edge":
        return ProbeResult(False, "UNVERIFIED", "wrong service or runtime")
    if payload.get("billing_mode") != "zero-cost-enforced":
        return ProbeResult(False, "UNVERIFIED", "zero-cost enforcement not asserted")

    if status == 200 and payload.get("status") == "ok" and payload.keys() == READY_KEYS:
        return ProbeResult(True, "READINESS_HTTP_PASS", "deployed GET contract reports ready")

    if status == 503 and payload.get("status") == "not_ready":
        if payload.keys() != NOT_READY_KEYS:
            return ProbeResult(False, "UNVERIFIED", "unexpected not-ready response schema")
        missing = payload.get("missing")
        if not isinstance(missing, list) or not missing or not all(isinstance(n, str) and n in CONFIG_NAMES for n in missing) or len(missing) != len(set(missing)):
            return ProbeResult(False, "UNVERIFIED", "unexpected readiness diagnostic")
        return ProbeResult(False, "NOT_READY", "missing configured inputs: " + ", ".join(sorted(set(missing))))

    return ProbeResult(False, "UNVERIFIED", "unexpected HTTP status or health state")


def probe(*, opener=None, timeout: float = 8.0) -> ProbeResult:
    if opener is None:
        opener = build_opener(NoRedirects())
    req = Request(ENDPOINT, headers={"Accept": "application/json"}, method="GET")
    try:
        response = opener.open(req, timeout=timeout)
    except HTTPError as exc:
        response = exc
    except (URLError, TimeoutError, OSError) as exc:
        return ProbeResult(False, "UNREACHABLE", type(exc).__name__)

    with response:
        if 300 <= response.status <= 399:
            return ProbeResult(False, "UNVERIFIED", "redirect refused")
        data = response.read(MAX_RESPONSE_BYTES + 1)
        return classify(response.status, response.headers, data, response.geturl())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="perform one bounded HTTPS GET (default makes no network calls)")
    args = parser.parse_args(argv)
    if not args.live:
        print("NOT_EXECUTED: add --live for one read-only GET")
        return 2
    result = probe()
    print(f"{result.kind}: {result.detail}")
    return 0 if result.qualified else 2


if __name__ == "__main__":
    raise SystemExit(main())
