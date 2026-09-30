# Masamune Product Roadmap

This roadmap is direction, not current capability.

## V0 — evidence-bound GitHub review

Implemented in the current feature branch:

- GitHub App webhook backend;
- exact-subject PR review;
- issue investigation;
- bounded defect sweep;
- Masa blind scan;
- Mune blind scan + challenge;
- deterministic reconciliation;
- durable delivery/review receipts;
- idempotent/readback-verified comments;
- repository policy;
- Python local/self-hosted backend;
- Supabase Edge + Postgres zero-cost hosted path;
- hard daily free-tier budget admission;
- singleton expiring model-execution lease;
- Groq Masa + Gemini Mune free-tier defaults;
- local tests/CI/container packaging.

## V0.2 — production execution substrate

Next engineering targets:

- durable queue with per-job leases, fencing, retry budget, and stuck-work
  recovery beyond the current singleton execution lease;
- structured observability and per-review token/cost accounting;
- rate-limit handling and backpressure;
- installation/repository entitlement registry;
- provider timeout/failure isolation;
- schema-constrained model output retries;
- encrypted secret custody;
- operator replay/reconciliation tools.

## V0.3 — stronger code understanding

- symbol-aware repository indexing;
- dependency/call-graph context expansion;
- issue/PR/history retrieval;
- test-to-code mapping;
- duplicate finding suppression;
- repository-specific invariants;
- historical defect and regression graph.

## V0.4 — sandboxed verification

- isolated ephemeral checkout workers;
- no GitHub credentials inside untrusted execution;
- repository-defined test allowlists;
- build/test receipts bound to exact commit/environment;
- negative/regression test synthesis;
- strict timeout/network/resource policy.

A test pass remains execution evidence, not semantic proof.

## V0.5 — repair workflow

- explicit opt-in repair permission;
- candidate repair branch;
- Masa repair proposal;
- Mune adversarial attack;
- sandbox qualification;
- draft PR only after surviving policy;
- human merge remains default.

## V1 — hosted product

- account/organization onboarding;
- repository selection;
- plans/entitlements;
- usage metering;
- billing;
- GitHub Marketplace packaging where appropriate;
- team dashboard;
- scheduled sweeps;
- retention/privacy controls;
- customer-controlled model/provider options;
- enterprise dedicated/self-hosted deployment path.

## Product metric

The primary quality metric should not be comment volume.

Masamune should optimize for **confirmed useful findings per unit of developer
attention**, with false-positive rate, finding survival after human review, time
to root cause, prevented recurrence, and review cost tracked separately.
