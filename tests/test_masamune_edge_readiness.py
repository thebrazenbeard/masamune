"""Offline tests for opt-in provider readiness probe; no network calls."""

import importlib.util
import json
from pathlib import Path
from email.message import Message
from unittest import TestCase
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / "tools" / "masamune_edge_readiness.py"
spec = importlib.util.spec_from_file_location("masamune_edge_readiness", SOURCE)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def headers(ref=module.PROJECT_REF):
    m = Message()
    m["sb-project-ref"] = ref
    return m


def payload(status="ok", missing=None, billing="zero-cost-enforced"):
    return json.dumps({
        "status": status,
        "service": "masamune",
        "runtime": "supabase-edge",
        "billing_mode": billing,
        **({"missing": missing} if missing is not None else {}),
    }).encode()


class EdgeReadinessTests(TestCase):
    def classify(self, http=200, data=None, ref=module.PROJECT_REF, url=module.ENDPOINT):
        return module.classify(http, headers(ref), payload() if data is None else data, url)

    def test_ready_exact_provider(self):
        self.assertTrue(self.classify().qualified)

    def test_missing_config_is_explicit_nonready(self):
        result = self.classify(503, payload("not_ready", ["MASAMUNE_GITHUB_APP_ID"]))
        self.assertEqual(result.kind, "NOT_READY")
        self.assertFalse(result.qualified)

    def test_no_foreign_provider_or_url(self):
        self.assertEqual(self.classify(ref="other").kind, "UNVERIFIED")
        self.assertEqual(self.classify(url="https://elsewhere.example/").kind, "UNVERIFIED")

    def test_refuse_unexpected_billing_mode(self):
        self.assertEqual(self.classify(data=payload(billing="operator-configured")).kind, "UNVERIFIED")

    def test_refuse_forged_status_or_config_name(self):
        self.assertEqual(self.classify(503, payload("not_ready", ["SECRET_VALUE"])).kind, "UNVERIFIED")
        self.assertEqual(self.classify(503, payload("ok")).kind, "UNVERIFIED")

    def test_bounded_and_strict_json(self):
        self.assertEqual(self.classify(data=b"x" * (module.MAX_RESPONSE_BYTES + 1)).kind, "UNVERIFIED")
        self.assertEqual(self.classify(data=b"<html></html>").kind, "UNVERIFIED")

    def test_default_does_not_contact_network(self):
        with patch.object(module, "probe", side_effect=AssertionError("network called")):
            self.assertEqual(module.main([]), 2)

    def test_redirect_handler_refuses_follow(self):
        self.assertIsNone(module.NoRedirects().redirect_request(None, None, 302, "move", {}, "https://elsewhere.example"))


if __name__ == "__main__":
    import unittest
    unittest.main()
