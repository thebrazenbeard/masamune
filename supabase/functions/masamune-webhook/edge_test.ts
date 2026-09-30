import { sha256Hex, verifyGithubSignature } from "./crypto.ts";
import { auditFinding } from "./evidence.ts";
import { skepticFlags } from "./skeptic.ts";
import { loadPolicy } from "./policy.ts";
import { reconcile } from "./reconcile.ts";
import { type LaneReport, parseCommand, type Subject } from "./types.ts";

function assert(
  condition: unknown,
  message = "assertion failed",
): asserts condition {
  if (!condition) throw new Error(message);
}

Deno.test("command parsing", () => {
  const command = parseCommand("/masamune investigate #417");
  assert(command?.kind === "INVESTIGATE");
  assert(command.issueNumber === 417);
  assert(parseCommand("/masamune sweep")?.kind === "SWEEP");
  assert(parseCommand("please investigate") === null);
});

Deno.test("policy is strict and bounded", () => {
  const policy = loadPolicy(
    "masamune:\n  allow_sweep: false\n  max_files: 5\n",
  );
  assert(policy.allow_sweep === false);
  assert(policy.max_files === 5);

  let threw = false;
  try {
    loadPolicy('masamune:\n  enabled: "false"\n');
  } catch {
    threw = true;
  }
  assert(threw, "string boolean must fail closed");
});

Deno.test("sha256 known vector", async () => {
  const digest = await sha256Hex(new TextEncoder().encode("abc"));
  assert(
    digest ===
      "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
  );
});

Deno.test("GitHub webhook HMAC verifies", async () => {
  const secret = "secret";
  const body = new TextEncoder().encode('{"hello":"world"}');
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = new Uint8Array(
    await crypto.subtle.sign("HMAC", key, body),
  );
  const hex = Array.from(sig, (b) => b.toString(16).padStart(2, "0")).join("");
  assert(await verifyGithubSignature(secret, body, "sha256=" + hex));
  assert(!(await verifyGithubSignature(secret, body, "sha256=deadbeef")));
});

Deno.test("reconciliation requires verification evidence", () => {
  const subject: Subject = {
    repository: "owner/repo",
    kind: "PULL_REQUEST",
    number: 1,
    head_sha: "a".repeat(40),
    base_sha: "b".repeat(40),
    title: "test",
    url: "https://github.com/owner/repo/pull/1",
  };
  const masa: LaneReport = {
    lane: "MASA",
    provider_id: "groq",
    model_id: "model-a",
    findings: [{
      id: "M-001",
      title: "duplicate effect",
      kind: "BUG",
      severity: "HIGH",
      confidence: 0.9,
      evidence: ["retry path"],
      mechanism: "response loss can replay the effect",
    }],
    challenges: [],
    notes: [],
  };
  const mune: LaneReport = {
    lane: "MUNE",
    provider_id: "google",
    model_id: "model-b",
    findings: [],
    challenges: [],
    notes: [],
  };

  const withoutEvidence = reconcile(subject, masa, mune, [{
    finding_id: "M-001",
    verdict: "CONFIRM",
    rationale: "agree",
    evidence: [],
  }]);
  assert(withoutEvidence.confirmed.length === 0);
  assert(withoutEvidence.unresolved.length === 1);

  const withEvidence = reconcile(subject, masa, mune, [{
    finding_id: "M-001",
    verdict: "CONFIRM",
    rationale: "reachable",
    evidence: ["caller retries after ambiguous response"],
  }]);
  assert(withEvidence.confirmed.length === 1);
});

Deno.test("evidence audit distinguishes exact and weak anchors", async () => {
  const exact = await auditFinding(
    {
      id: "M-001",
      title: "retry can duplicate effect",
      kind: "BUG",
      severity: "HIGH",
      confidence: 0.9,
      file: "src/retry.ts",
      line: 2,
      evidence: [],
      mechanism: "response loss can replay the effect",
    },
    "MASA",
    "=== HEAD SOURCE src/retry.ts ===\nline one\nline two\n",
  );
  assert(exact.quality === "EXACT_FILE_LINE");

  const truncated = await auditFinding(
    {
      id: "M-002",
      title: "unknown",
      kind: "BUG",
      severity: "MEDIUM",
      confidence: 0.9,
      file: "src/retry.ts",
      line: 2,
      evidence: [],
      mechanism: "unknown",
    },
    "MASA",
    "=== HEAD SOURCE src/retry.ts ===\nline one\n[MASAMUNE FILE/PATCH TRUNCATED]\n",
  );
  assert(truncated.quality === "EXACT_FILE");

  const assertion = await auditFinding(
    {
      id: "M-003",
      title: "unknown",
      kind: "BUG",
      severity: "MEDIUM",
      confidence: 0.9,
      file: "src/missing.ts",
      line: 2,
      evidence: ["not present"],
      mechanism: "unknown",
    },
    "MASA",
    "=== HEAD SOURCE src/retry.ts ===\nline one\n",
  );
  assert(assertion.quality === "MODEL_ASSERTION");
});

Deno.test("skeptic gate catches incomplete challenge coverage", () => {
  const masa = {
    lane: "MASA" as const,
    provider_id: "groq",
    model_id: "masa-model",
    findings: [{
      id: "M-001",
      title: "retry defect",
      kind: "BUG" as const,
      severity: "HIGH" as const,
      confidence: 0.9,
      file: "src/retry.ts",
      line: 4,
      evidence: ["evidence"],
      mechanism: "replay",
    }],
    challenges: [],
    notes: [],
  };
  const mune = {
    lane: "MUNE" as const,
    provider_id: "google",
    model_id: "mune-model",
    findings: [],
    challenges: [],
    notes: [],
  };
  const flags = skepticFlags(masa, mune, [], []);
  assert(flags.includes("CHALLENGE_COVERAGE_GAP:M-001"));
  assert(flags.includes("MISSING_EVIDENCE_RECEIPT:M-001"));
});

Deno.test("skeptic gate accepts exact evidence and complete challenge", () => {
  const masa = {
    lane: "MASA" as const,
    provider_id: "groq",
    model_id: "masa-model",
    findings: [{
      id: "M-001",
      title: "retry defect",
      kind: "BUG" as const,
      severity: "HIGH" as const,
      confidence: 0.9,
      file: "src/retry.ts",
      line: 4,
      evidence: ["evidence"],
      mechanism: "replay",
    }],
    challenges: [],
    notes: [],
  };
  const mune = {
    lane: "MUNE" as const,
    provider_id: "google",
    model_id: "mune-model",
    findings: [],
    challenges: [],
    notes: [],
  };
  const flags = skepticFlags(
    masa,
    mune,
    [{
      finding_id: "M-001",
      verdict: "CONFIRM" as const,
      rationale: "reachable",
      evidence: ["call path reaches retry"],
      narrowed_title: null,
    }],
    [{
      finding_id: "M-001",
      lane: "MASA" as const,
      quality: "EXACT_FILE_LINE" as const,
      file: "src/retry.ts",
      line: 4,
      source_sha256: "a".repeat(64),
      context_sha256: "b".repeat(64),
      rationale: "exact source anchor",
    }],
  );
  assert(flags.length === 0);
});
