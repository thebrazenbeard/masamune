# R9A0 Edge Implementation Readiness Specification V1

**Author lane:** Masa
**Status:** NON_EXECUTING_READINESS_SPEC_READY_FOR_REVIEW
**Source candidate:** `design/R9A0_EDGE_CONTROL_PLANE_PROPOSAL_V2.md`
**Bound candidate head:** `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`
**Independent design verdict:** Mune `APPROVED_DESIGN_KEEP_AND_DEFER`
**Deployment authorized:** No
**Credential action authorized:** No
**Hosted database apply authorized:** No
**Paid-service action authorized:** No

## Purpose

This document converts the approved Edge V2 architecture into an implementation-readiness contract without performing the implementation.

The intended future component is one narrow transport adapter, `r9a0-coordination-ingest`, for a named consumer that needs an HTTP boundary and must not receive broad Supabase/database credentials.

The database remains canonical authority. The Edge layer may authenticate, authorize transport semantics, validate a fixed request, invoke one governed database path, and return the authoritative receipt. It may not become a second authority engine, workflow system, memory service, generic API gateway, or source of canonical state.

The readiness verdict is deliberately split:

- **DESIGN_READY:** yes, under the approved V2 contract.
- **IMPLEMENTATION_PACKET_READY_TO_BUILD:** only after the gates below have exact values and owners.
- **HOSTED_DEPLOYMENT_READY:** no.

## Gate 1: named consumer

No implementation should start merely to make Edge exist.

Before implementation, bind:

1. consumer name and owner;
2. caller population: one machine, bounded machines, or other closed set;
3. exact reason the existing trusted runtime/database path is unsuitable;
4. expected steady-state and burst request rates;
5. failure/retry behavior;
6. required response/receipt semantics;
7. whether caller network location can be restricted before Edge invocation;
8. lifecycle owner for actor scopes and signing keys.

If there is no named consumer with a real credential-boundary problem, the correct implementation remains **none**.

## Gate 2: repository-first implementation packet

A future implementation must be one immutable repository candidate containing all of these surfaces before any hosted effect:

```text
supabase/functions/r9a0-coordination-ingest/
  index.ts
  actor-policy.ts
  schema.ts
  auth.ts
  errors.ts
  README.md

supabase/migrations/<timestamp>_r9a0_edge_ingest_principal.sql
supabase/execution/<timestamp>_r9a0_edge_ingest_principal.sql
supabase/rollbacks/<timestamp>_r9a0_edge_ingest_principal.down.sql
supabase/tests/<timestamp>_r9a0_edge_ingest_principal.test.sql

tests/edge/r9a0-coordination-ingest.test.ts

docs/edge/R9A0_EDGE_PRIVILEGE_MATRIX.md
docs/edge/R9A0_EDGE_ACTOR_POLICY.md
docs/edge/R9A0_EDGE_FAILURE_AND_RETRY.md
docs/edge/R9A0_EDGE_ZERO_PAID_GATE.md
docs/edge/R9A0_EDGE_DEPLOYMENT_RECEIPT_TEMPLATE.json
```

Names may be adjusted by the implementation owner, but the evidence classes may not be omitted.

Execution SQL must be byte-identical to the repository migration unless the governing database process explicitly defines a stronger bound mechanism.

## Gate 3: dedicated database execution principal

The deployable Edge adapter must not hold the project-wide `service_role` credential.

The implementation candidate must create a dedicated database identity, conceptually `r9a0_edge_ingest`, satisfying all of these properties:

- LOGIN only if the selected connection mechanism actually requires LOGIN;
- not an owner of any schema/table/function;
- no membership in `service_role`, `postgres`, `r9a0_owner`, or another broad role;
- no `BYPASSRLS`;
- no `CREATEDB`, `CREATEROLE`, or replication capability;
- no direct table `INSERT`, `UPDATE`, `DELETE`, or `TRUNCATE`;
- no general table `SELECT` unless a separately reviewed receipt-read path proves it necessary;
- `USAGE` only on the minimum API schema required;
- `EXECUTE` only on one fixed governed append entry point and, if required, one fixed receipt-by-operation lookup;
- no Auth-admin, Storage-admin, Realtime, Vault, extension-management, or unrelated schema capability.

### Preferred database call shape

Prefer one of these, in order:

1. **Existing append RPC with a narrow caller check** extended repository-first to permit the dedicated database principal without weakening current callers.
2. **Thin security-definer Edge wrapper RPC** owned by `r9a0_owner`, with pinned `search_path`, that validates `session_user = 'r9a0_edge_ingest'` and delegates immediately to the existing authoritative append transition logic.

Do not duplicate the coordination transition algorithm in a second function.

If neither path can be implemented without broad privileges or duplicated invariants, the implementation verdict is **REJECT EDGE**.

## Gate 4: receipt lookup after ambiguous transport failure

The caller must never blindly repeat a write after a timeout or connection reset that may have occurred after commit.

The implementation packet must provide a narrow operation-status path with these semantics:

```text
input: operation_id
output:
  NOT_FOUND
  or original governed receipt { event_id, event_sequence, request_digest, status, record_time }
```

The lookup must not expose arbitrary event search or unrelated coordination data.

After ambiguous failure:

1. query by the same `operation_id`;
2. if a receipt exists, return/reconcile that receipt and do not write again;
3. if not found, a retry may reuse the exact same operation ID and exact same request bytes;
4. changed semantics under the same operation ID must remain a hard failure at the database idempotency boundary.

## Gate 5: actor policy

Authentication and semantic authorization are separate.

Actor policy metadata is repository-visible and contains no secret material. Every actor record must bind:

```json
{
  "actor_id": "example",
  "key_ids": ["example-2026-08-a"],
  "allowed_source_branches": ["exact-or-reviewed-prefix"],
  "allowed_thread_prefixes": ["exact-or-reviewed-prefix"],
  "allowed_event_types": ["closed-enum-values"],
  "allowed_target_prefixes": ["exact-or-reviewed-prefix"],
  "enabled": true
}
```

Rules:

- default deny;
- no implicit actor creation;
- no actor may assert another actor's `source_branch` merely because its HMAC is valid;
- wildcard semantic scopes require explicit governing authority and a dedicated hostile test;
- actor policy cannot grant merge, deployment, production, memory, credential, or writer-lease authority;
- policy changes are repository changes and require the normal writer/reviewer discipline.

## Gate 6: signing-key lifecycle

Transport V1 remains HMAC-SHA-256 with no algorithm negotiation.

Required request identity:

- `X-Vera-Actor`;
- `X-Vera-Key-Id`;
- `X-Vera-Timestamp`;
- `X-Vera-Signature`;
- body `operation_id` matching the signed operation ID.

Canonical signed bytes are those defined by Edge V2: fixed version line, `POST`, fixed path, timestamp, actor, key ID, operation ID, and SHA-256 of exact raw body bytes.

### Secret placement

- secret bytes are stored only in the approved hosted secret/environment facility;
- repository stores only actor/key metadata and secret-variable names, never secret values;
- coordination events, deployment receipts, CI logs, application logs, and error responses never contain secret material;
- the database credential is a different secret from all actor HMAC secrets.

### Key states

Use closed states:

`ACTIVE | RETIRING | REVOKED`

Rules:

- one primary ACTIVE key per actor;
- rotation may temporarily allow one ACTIVE successor plus one RETIRING predecessor;
- overlap is bounded to 24 hours maximum;
- REVOKED fails immediately;
- a revoked `key_id` is never reused;
- a lost/suspected key goes directly to REVOKED;
- credential creation, rotation, and revocation are explicit credential actions and remain separately gated.

### Rotation sequence

1. create successor secret under authorized credential action;
2. deploy actor metadata recognizing successor key ID;
3. verify successor authentication in a non-mutating or disposable test path;
4. move old key to RETIRING;
5. update caller;
6. verify caller uses successor;
7. revoke old key before overlap deadline;
8. remove retired secret after verified revocation.

Do not rotate by overwriting the value behind an unchanged key ID because that destroys auditability of which credential signed a request.

## Gate 7: request validation

The function accepts only `POST` and `application/json` for the fixed versioned route.

Validation order must be deterministic:

1. platform/admin kill state;
2. method/content type;
3. conservative total body-size cap;
4. required auth headers and strict encoding;
5. timestamp/skew;
6. actor and key existence/state;
7. exact raw-body hash and constant-time HMAC verification;
8. JSON parse;
9. strict schema with unknown-field rejection;
10. operation ID/header-body consistency;
11. actor semantic scope;
12. payload/reference 16 KiB caps;
13. one fixed database call.

No caller-controlled SQL, schema, table, role, RPC, function, URL, or database identifier is accepted.

## Gate 8: stable failure classes

The implementation must distinguish rejection, infrastructure failure, and ambiguous commit.

Recommended public classes:

| Class | Meaning | Retry posture |
|---|---|---|
| `EDGE_DISABLED` | administrative kill/undeploy state | no automatic retry |
| `METHOD_NOT_ALLOWED` | wrong HTTP method | no retry |
| `UNSUPPORTED_MEDIA_TYPE` | wrong content type | no retry |
| `REQUEST_TOO_LARGE` | body/payload/reference cap exceeded | no retry |
| `AUTH_INVALID` | malformed/invalid signature | no retry |
| `AUTH_EXPIRED` | timestamp outside allowed skew | caller may re-sign same semantic request with same operation ID |
| `ACTOR_DISABLED` | actor/key revoked or disabled | no retry |
| `SCOPE_DENIED` | semantic actor scope failure | no retry |
| `SCHEMA_INVALID` | request shape invalid | no retry until corrected with a new operation ID if semantics change |
| `GOVERNANCE_REJECTED` | authoritative DB transition/idempotency rejection | follow database semantics, do not reinterpret |
| `DEPENDENCY_UNAVAILABLE_NO_COMMIT` | DB unavailable before attempted effect is known | bounded retry with same bytes/operation ID only |
| `AMBIGUOUS_COMMIT` | transport failed after DB effect may have committed | receipt lookup first; never blind retry |
| `INTERNAL_FAILURE` | bounded adapter defect | no mutation retry until commit state verified |

Do not expose raw SQL errors, stack traces, credentials, or private payload content.

## Gate 9: observability and redaction

V1 uses only already-included platform logging unless a separately authorized alternative is later approved.

Allowed structured fields:

- transport request ID;
- actor ID;
- key ID;
- operation ID;
- source commit/function version;
- outcome class;
- HTTP status;
- database receipt event ID/sequence when available;
- coarse latency bucket;
- deployment identifier.

Forbidden log content:

- authorization headers;
- HMAC values or secrets;
- database credentials;
- raw request body;
- raw `payload` or `reference_data` by default;
- arbitrary SQL/database errors;
- intimate/private content merely for debugging.

Logs are operational evidence only. The committed database receipt remains authoritative mutation evidence.

## Gate 10: zero-paid deployment proof

The function must not be deployed under the project's zero-added-cost constraint until current plan evidence proves the complete abuse envelope.

Required deployment-bound values:

```json
{
  "plan_locator": "current provider/organization evidence",
  "included_monthly_invocations": 0,
  "paid_overage_enabled": false,
  "named_caller_count": 0,
  "max_expected_requests_per_hour": 0,
  "edge_monthly_budget": 0,
  "edge_hourly_rejection_budget": 0,
  "kill_threshold_percent": 80,
  "pre_invocation_control": "verified mechanism or NONE",
  "worst_case_monthly_invocations": 0,
  "within_included_quota": false
}
```

The zeros above are placeholders, not claimed provider values.

A deployment is permitted only if one of these is proven from current evidence:

1. a no-additional-cost control rejects unauthorized/unbounded traffic before it consumes the relevant Edge invocation quota; or
2. a separately governed already-available upstream boundary limits the caller population and rate before Edge; or
3. the endpoint is reachable only by a demonstrably bounded caller set, worst-case invocation math stays below the included quota, and paid overage is disabled.

If the provider cannot disable paid overage, or rejected requests can produce unbounded billable usage beyond the included envelope, the zero-paid verdict is **DO NOT DEPLOY**.

### Administrative kill threshold

The 80% threshold is a policy threshold, not an in-function rate limiter.

A deployment packet must prove how usage is observed and how the endpoint is disabled at the platform/deployment boundary before the budget is exhausted. An action performed inside an invocation is not a pre-invocation cost control.

## Gate 11: hostile tests

The implementation candidate must have deterministic tests covering at least:

1. valid actor/in-scope request produces exactly one governed event;
2. exact replay produces no duplicate and returns original receipt;
3. reused operation ID with changed semantics fails;
4. another actor's source branch is denied;
5. out-of-scope thread/event/target is denied;
6. unknown actor denied;
7. unknown key denied;
8. RETIRING key accepted only inside configured overlap;
9. REVOKED key denied immediately;
10. modified raw body invalidates signature;
11. actor header/key mismatch denied;
12. timestamp just inside skew accepted and just outside rejected;
13. malformed signature hex rejected without timing-sensitive comparison path;
14. unknown JSON field rejected;
15. oversized total body rejected;
16. oversized payload rejected;
17. oversized reference data rejected;
18. SQL/RPC/schema/table/function injection fields have no route into execution;
19. dedicated DB principal cannot select unrelated tables;
20. dedicated DB principal cannot directly mutate coordination tables;
21. dedicated DB principal cannot invoke unrelated RPCs;
22. direct client/anon/authenticated behavior remains unchanged;
23. stale predecessor rejected by canonical DB contract;
24. fork attempt rejected;
25. cross-thread predecessor rejected;
26. timeout before DB attempt classified as no-commit;
27. forced connection drop after possible commit produces ambiguous state and receipt lookup prevents duplicate write;
28. kill state prevents the database call;
29. log capture contains no credentials/raw payloads;
30. rollback/disable leaves committed coordination history intact;
31. exact source/deployment identity appears in receipt metadata;
32. zero-paid budget fixture fails closed when plan evidence is absent;
33. zero-paid budget fixture fails when overage is enabled;
34. budget-threshold drill demonstrates administrative disable procedure.

Tests 19 through 22 require a disposable database environment. Hosted production evidence is not a substitute.

## Gate 12: rollback and forward repair

Edge rollback is transport removal, not coordination-history deletion.

Required procedures:

### Function rollback

- disable/undeploy the adapter;
- retain repository history of the deployed version;
- callers fail closed and do not fall back to a broad database credential;
- canonical Postgres coordination state remains untouched.

### Database privilege rollback

The future migration packet must include a rollback that:

- revokes the dedicated principal's function/schema privileges;
- disables or drops only the Edge-specific execution role/wrapper if safe under the database migration policy;
- does not modify or delete coordination events;
- does not revoke privileges required by existing non-Edge R9A0 paths.

If dropping the login would destroy needed audit attribution, prefer `NOLOGIN`/revocation as forward repair rather than destructive cleanup. The exact choice must be tested in the disposable database.

### Secret rollback

- revoke actor keys when compromise is suspected;
- revoke/rotate the dedicated DB credential separately;
- never restore operation by exposing `service_role` to the caller.

## Gate 13: exact deployment receipt

A future deployment receipt must bind at least:

```json
{
  "schema": "VERA_R9A0_EDGE_DEPLOYMENT_RECEIPT_V1",
  "source_commit": "immutable sha",
  "function_source_digest": "sha256",
  "database_migration_digest": "sha256",
  "database_test_receipt": "locator",
  "actor_policy_digest": "sha256",
  "function_name": "r9a0-coordination-ingest",
  "function_version": "bound deployment id",
  "database_principal": "r9a0_edge_ingest",
  "secret_ids": ["names/versions only, never values"],
  "plan_evidence_locator": "current evidence",
  "paid_overage_enabled": false,
  "budget_gate_passed": true,
  "hostile_test_receipt": "locator",
  "rollback_test_receipt": "locator",
  "deployed_at": "timestamp"
}
```

The receipt does not itself prove the underlying evidence. Every locator must be independently retrievable.

## Gate 14: separation from other R9A0 systems

The implementation must contain no dependency on:

- Anticipatory Pragmatics;
- shared-knowledge/vector search;
- canonical memory admission;
- voice runtime inference;
- model orchestration;
- Realtime;
- queues;
- Cron;
- Storage for request payloads;
- paid branching;
- external SaaS observability.

Those systems may evolve independently without changing this transport boundary.

## Required review sequence before any hosted effect

1. Masa or assigned implementer prepares one repository-first immutable implementation candidate.
2. Disposable CI applies the exact privilege migration and executes the hostile DB/Edge test suite.
3. Mune reviews one immutable head and its receipts without patching it.
4. Voss reconciles the candidate against current R9A0 authority, plan/cost, and release state.
5. Exact user authority is obtained for any credential creation, hosted migration, deployment, or paid-risk action.
6. Only then may hosted implementation occur.

A design approval is not deployment authority.

## Current readiness verdict

`DESIGN_APPROVED_IMPLEMENTATION_NOT_YET_JUSTIFIED`

The architecture is implementable in principle, but no named consumer, dedicated database credential, actor keys, current plan/abuse proof, or hosted deployment authority is established by this document.

Until those inputs exist, leaving Edge undeployed is not unfinished work. It is the correct state of the approved KEEP_AND_DEFER design.

## Evidence baseline

- Masa Edge V2 candidate: `thebrazenbeard/masamune` head `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`.
- Mune independent review artifact: `reviews/edge-control-plane-v2-review-d65bcb2-v1.md`, verdict `APPROVED_DESIGN_KEEP_AND_DEFER`.
- Voss replacement assignment: Vera coordination sequence `3279`.
- R9A0 database authority baseline remains the accepted current-base candidate at `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`; this readiness spec makes no modification to that branch.
