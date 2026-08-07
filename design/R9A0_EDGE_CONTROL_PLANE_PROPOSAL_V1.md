# R9A0 Edge Control-Plane Proposal V1.1

**Author lane:** Masa
**Status:** REVISED_AFTER_MUNE_REVIEW
**Mune findings addressed:** MUNE-EDGE-001, MUNE-EDGE-002, MUNE-EDGE-003, MUNE-EDGE-004
**Implementation/deployment authorized:** No
**Paid-service dependency:** None permitted

## Decision

R9A0 should **keep the narrow Edge transport-adapter design and defer deployment**.

The existing database slice remains the authority core: governed append-only state, forced RLS, a NOLOGIN owner, deterministic idempotency, and a narrow write contract. Edge is useful only when a named consumer needs an HTTP boundary and should not possess database credentials.

The first candidate remains one function:

`r9a0-coordination-ingest`

It is not canonical state, not an authority engine, not a memory layer, not a workflow system, and not a second coordination ledger. It authenticates a named actor, enforces that actor's predeclared scope, validates a fixed request contract, invokes one governed database write path, and returns the database receipt.

Until a named consumer and a zero-paid abuse boundary are both proven, the deployment decision is **DEFER**.

## Existing authority boundary to preserve

The current R9A0 database contract remains authoritative:

- only `r9a0_governance`, `r9a0_coordination`, and `r9a0_api` are in the database slice;
- `r9a0_owner` is NOLOGIN and owns privileged objects;
- RLS is forced on governed base tables;
- direct client mutation is denied;
- operation IDs and request digests provide deterministic replay behavior;
- payload and reference objects are capped at 16 KiB each;
- thread transitions are serialized and stale/forked/cross-thread transitions fail closed.

The Edge adapter may narrow credential exposure. It may not duplicate or weaken the database transition rules.

## Named-consumer gate

Do not implement or deploy the adapter until all of these are bound in a repository-first implementation packet:

1. concrete caller identity and owner;
2. reason the caller cannot safely use the existing trusted runtime path;
3. actor authorization scope;
4. authentication key lifecycle and rotation owner;
5. expected invocation rate and failure behavior;
6. no-cost pre-invocation abuse control or an explicit proof that the route is not exposed to an unbounded caller population;
7. exact database execution principal and privilege matrix;
8. repository/hosted provenance and rollback procedure;
9. current Supabase plan limits and included invocation budget;
10. hostile tests for the exact implementation candidate.

If any item is absent, direct use of the existing governed runtime path is simpler and safer.

## Actor authorization contract

Authentication alone is insufficient. A valid signature proves possession of a key; it does not authorize arbitrary semantic identity.

Every actor must have a repository-defined, default-deny authorization record conceptually equivalent to:

```json
{
  "actor_id": "masa",
  "key_ids": ["masa-2026-08-a"],
  "allowed_source_branches": ["debug/masamune/masa"],
  "allowed_thread_prefixes": ["vera-r9a0/assignments/masa/"],
  "allowed_event_types": ["STATUS", "REVIEW", "ISSUE", "RESOLUTION"],
  "allowed_target_prefixes": ["debug/masamune/", "auditor/voss", "vera-r9a0/program"],
  "enabled": true
}
```

The actual actor records may use another compact format, but these invariants are mandatory:

- caller-supplied `source_branch` must match the authenticated actor's allowed source scope;
- caller-supplied `thread_key`, `event_type`, and `target_branch` must fall inside the actor's configured scope;
- unknown actor, unknown key, disabled actor, or out-of-scope semantic identity fails before database execution;
- an actor cannot claim another actor's branch merely by signing the request with its own valid key;
- wildcard scopes are prohibited unless a specific actor's governing authority explicitly requires them and hostile tests cover the expansion;
- the Edge layer does not create new merge, deployment, production, memory, or writer-lease authority.

This closes semantic impersonation at the transport boundary while leaving the database as canonical state.

## Public request contract

Version the transport request independently from the database implementation.

```json
{
  "schema": "VERA_R9A0_COORDINATION_INGEST_V1",
  "operation_id": "uuid-or-canonical-operation-id",
  "thread_key": "string",
  "source_branch": "string",
  "target_branch": "string",
  "event_type": "string",
  "status": "string",
  "objective": "string",
  "summary": "string",
  "active_issue": "string|null",
  "requested_perspective": "string|null",
  "supersedes_event_id": "uuid|null",
  "acknowledges_event_id": "uuid|null",
  "payload": {},
  "reference_data": {}
}
```

Rules:

- reject unknown top-level fields unless that schema version explicitly permits them;
- require UTF-8 JSON and `application/json`;
- enforce the database's 16 KiB caps for `payload` and `reference_data` before calling Postgres;
- enforce a conservative total body cap below platform limits;
- never accept SQL, RPC names, table names, schema names, function names, role names, or privilege directives from the caller;
- never accept an instruction to bypass or reinterpret governance checks;
- authorize semantic scope before the database call;
- pass only the fixed argument set to the governed write path.

## Signature protocol

V1 uses a closed, explicit signature format. No algorithm negotiation is allowed.

Required headers:

- `X-Vera-Actor`: configured actor ID;
- `X-Vera-Key-Id`: active key ID assigned only to that actor;
- `X-Vera-Timestamp`: Unix epoch seconds in base-10 ASCII;
- `X-Vera-Signature`: lowercase hexadecimal HMAC-SHA-256 digest.

The caller signs the exact canonical byte string:

```text
VERA-R9A0-INGEST-V1\n
POST\n
/functions/v1/r9a0-coordination-ingest\n
<timestamp>\n
<actor_id>\n
<key_id>\n
<operation_id>\n
<lowercase_hex_sha256_of_exact_raw_request_body>
```

Canonicalization rules:

1. HTTP method is exactly uppercase `POST`.
2. Path is exactly `/functions/v1/r9a0-coordination-ingest` with no query-string contribution.
3. Header values are UTF-8 without leading/trailing whitespace after transport parsing.
4. Timestamp is canonical base-10 seconds with no sign, decimal, or padding.
5. Actor ID, key ID, and operation ID must match the values validated from headers/body exactly.
6. Body hash is SHA-256 of the exact raw bytes received, before JSON reserialization.
7. Signature algorithm is fixed to HMAC-SHA-256 for V1.
8. Verification uses a constant-time byte comparison after strict hexadecimal decoding.
9. Timestamp acceptance window is ±300 seconds; values outside the window fail closed.
10. Reusing an operation ID with changed body semantics still fails at the authoritative database idempotency contract.

No JSON canonicalization scheme is required because the signature covers the exact received body bytes.

## Key lifecycle

Keys are per actor, never shared across actors.

- Every key has `actor_id`, `key_id`, state, creation time, and optional retirement time.
- Only `ACTIVE` keys authenticate new requests.
- Rotation may temporarily expose one `ACTIVE` and one explicitly `RETIRING` key for a bounded overlap window no longer than 24 hours.
- `REVOKED` keys fail immediately and cannot be reactivated under the same key ID.
- Key material never appears in repository files, coordination payloads, logs, receipts, or error bodies.
- Rotation and credential creation are separate credential actions requiring the authority applicable at implementation time.

## Database credential boundary

**The Edge Function must not hold the project-wide Supabase `service_role` credential.** That key is broader than this adapter's purpose and can bypass RLS across unrelated surfaces.

A deployable implementation therefore requires a separate repository-first database privilege repair before Edge deployment:

1. Create a dedicated login execution principal such as `r9a0_edge_ingest` with no ownership, no membership in broad platform roles, and no general table privileges.
2. Grant only database connect as necessary, `USAGE` on `r9a0_api`, and `EXECUTE` on the one governed append function or a fixed edge wrapper that delegates to the same authoritative transition logic.
3. If the existing append function currently authorizes only service-role JWT execution, amend its authorization boundary or add a thin fixed wrapper so the dedicated `session_user` is accepted without duplicating transition logic.
4. Grant no direct `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, Storage, Auth-admin, Realtime, or unrelated schema access to the Edge principal.
5. Store only the dedicated principal's connection secret in the function environment.
6. Prove through hostile-role tests that the credential cannot access unrelated tables or invoke arbitrary RPCs.

The role credential itself is not created by this design document. Credential creation, hosted migration, and deployment remain separately gated actions.

If this least-privilege database principal cannot be implemented cleanly, **reject Edge deployment** rather than falling back to the broad service-role key.

## Authority model

The adapter answers only two transport questions:

1. Is this authenticated actor allowed to submit this exact semantic request shape?
2. Can the fixed governed database write path be attempted?

It does not decide whether:

- an event's claim is true;
- a recipient consumed it;
- a merge, deployment, or production mutation is authorized;
- a record qualifies as memory;
- a release is installed;
- a coordination event supersedes authority outside the database contract.

Those remain governed elsewhere.

## Failure behavior

Fail closed before database execution on:

- malformed JSON;
- unsupported schema;
- unknown field;
- missing field;
- oversized request/payload/reference data;
- signature or key failure;
- timestamp outside ±300 seconds;
- actor disabled or unknown;
- semantic scope mismatch;
- invalid operation ID;
- arbitrary database-object selection attempt.

Return the database's governed rejection without reinterpretation on:

- request-digest mismatch;
- stale predecessor;
- cross-thread predecessor;
- invalid controlling transition;
- fork attempt;
- database privilege failure.

A transport retry must reuse the same operation ID and exact body bytes. After ambiguous network failure, the caller must verify commit state through the governed receipt/read path before deciding whether another transport attempt is appropriate.

## Observability

Use only built-in structured function logs for the first candidate. No paid log drain is required.

Permitted fields:

- transport request ID;
- actor ID;
- key ID, never key material;
- operation ID;
- function version/commit;
- outcome class;
- HTTP status;
- database receipt event ID/sequence when returned;
- coarse latency;
- deployment identifier.

Never log authorization headers, HMAC secrets, database credentials, raw request bodies, raw payload/reference objects, or private user content merely for debugging.

The database receipt remains authoritative mutation evidence. Logs are operational evidence only.

## Zero-paid invocation-abuse boundary

Mune correctly identified a limit that cannot be hand-waved away: **a rejected Edge invocation can still consume Edge invocation quota**. Function-internal authentication or rate limiting therefore does not itself guarantee zero cost under volumetric abuse.

V1 deployment is forbidden until the implementation packet proves one of these conditions:

1. the platform provides a no-additional-cost pre-invocation restriction/rate limit that bounds requests before they count against the relevant quota; or
2. the endpoint is reachable only through a separately governed, already-available no-cost upstream boundary that limits the caller population and request rate; or
3. current included quota plus a documented worst-case caller model proves the endpoint cannot trigger paid overage, with paid overage disabled.

If none can be proven, the correct zero-paid-cost verdict is **DO NOT DEPLOY EDGE**.

The deployment receipt must bind these values from the actual current plan rather than hard-code folklore into architecture:

```json
{
  "included_monthly_invocations": "verified-current-number",
  "paid_overage_enabled": false,
  "edge_monthly_budget": "bounded-number-below-included-quota",
  "edge_hourly_rejection_budget": "bounded-number",
  "kill_threshold_percent_of_edge_budget": 80,
  "pre_invocation_abuse_control": "verified mechanism",
  "verification_locator": "plan/config evidence"
}
```

Crossing the configured 80% Edge budget or the hourly rejection budget requires the adapter to be administratively disabled at the platform/deployment layer, not merely return a different response inside an already-counted invocation. Re-enabling it requires fresh plan/budget verification.

This design does not claim an automatic no-cost kill mechanism exists today. That mechanism must be demonstrated before deployment.

## Runtime constraints

The adapter remains short-lived and synchronous. It should perform bounded parsing, signature verification, scope authorization, one governed database call, and receipt serialization.

It must not absorb background jobs, long-running orchestration, agent loops, vector work, model inference, or queue consumption.

Any implementation must re-verify then-current Supabase Edge runtime limits before deployment rather than rely on old numeric limits in this design document.

## Rollback and kill switch

Because the Edge adapter is not canonical state, rollback is transport removal rather than database-history rewriting.

Required controls:

- environment/config enable flag defaulting closed;
- repository-bound previous function version;
- tested administrative disable/undeploy procedure;
- independent ability to disable the adapter while leaving the canonical database contract intact;
- no fallback path that exposes a broad credential to a previously untrusted caller.

The dedicated database principal and any supporting grant must have a repository-first rollback/forward-repair migration if they are ever implemented.

## Hostile acceptance tests

Before deployment, prove at minimum:

1. valid actor, valid key, and in-scope semantic identity creates exactly one governed event;
2. valid actor attempting another actor's `source_branch` fails before database execution;
3. valid actor with out-of-scope thread/event/target fails closed;
4. exact replay returns the original receipt without duplication;
5. same operation ID plus changed body fails closed;
6. signature with modified raw body bytes fails;
7. signature with actor/key mismatch fails;
8. expired/future timestamp outside ±300 seconds fails;
9. revoked key fails immediately;
10. signature comparison and malformed hex handling do not leak key information;
11. oversized body/payload/reference fails closed;
12. arbitrary RPC/schema/table injection is impossible;
13. stale, forked, and cross-thread transitions preserve database rejection behavior;
14. Edge database credential cannot read or mutate unrelated tables or invoke unrelated RPCs;
15. logs contain no secrets or raw private payloads;
16. adapter disable/undeploy performs no database rollback and canonical RPC state remains valid;
17. ambiguous database/network failure does not cause blind duplicate mutation;
18. exact source commit/deployment identity is present in the operational receipt;
19. zero-paid plan/budget evidence is current and paid overage is disabled;
20. abuse test reaches the configured budget threshold and demonstrates the documented platform-level kill procedure.

## Explicit non-targets

The Edge adapter must not become:

- an agent runtime;
- an LLM orchestration layer;
- a prompt router;
- a memory service;
- a long-running worker;
- a queue consumer;
- a generic privileged API gateway;
- a replacement for Postgres constraints or RLS;
- a second coordination ledger;
- a route around writer leases, merge authority, or hosted-apply gates.

## Recommendation to Voss

**KEEP the architecture, DEFER deployment.**

Mune's review strengthens the defer decision. A real implementation is acceptable only if it has actor-bound semantic authorization, a dedicated least-privilege database principal instead of `service_role`, a fixed signature/key lifecycle, and a proven zero-paid abuse boundary. If those conditions cannot all be demonstrated, the right implementation is no Edge Function at all.

## Source baseline

Repository evidence:

- `vera-R9A0/docs/database/R9A0_SUPABASE_ARCHITECTURE.md` at database head `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`.
- `vera-R9A0/docs/database/R9A0_PRIVILEGE_MATRIX.md` at the same head.
- Mune adversarial review sequence `3263`, review commit `fbb1560fcdafb2cf368e6306577f9b88a6e1980e`.

Current Supabase documentation must be re-verified at implementation time for Edge authentication, limits, pricing, secrets, and any available pre-invocation protection.