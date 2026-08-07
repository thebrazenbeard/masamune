# R9A0 Edge Control-Plane Proposal V1

**Author lane:** Masa
**Status:** PROPOSAL_READY_FOR_ADVERSARIAL_REVIEW
**Implementation/deployment authorized:** No
**Paid-service dependency:** None

## Decision

R9A0 should **not deploy an Edge Function merely because Supabase offers one**. The existing database slice already has the correct authority core: governed append-only state, forced RLS, a NOLOGIN owner, deterministic idempotency, and one narrow service-role RPC.

Keep Edge as a **deferred transport adapter** for a named consumer that needs an HTTP boundary and cannot safely hold the Supabase service credential. When such a consumer exists, the first candidate is one function only:

`r9a0-coordination-ingest`

The function is not canonical state, not an authority engine, not a memory layer, and not a second workflow system. It validates and authenticates a request, then invokes the existing `r9a0_api.append_coordination_event` contract and returns the database receipt.

Until a named consumer proves this boundary is needed, the implementation decision is **DEFER**.

## Existing authority boundary to preserve

The current R9A0 database contract is authoritative for this proposal:

- only `r9a0_governance`, `r9a0_coordination`, and `r9a0_api` are in scope;
- `r9a0_owner` is NOLOGIN and owns privileged objects;
- RLS is forced on governed base tables;
- `service_role` has named read policies but no direct insert/update/delete path;
- writes enter through `r9a0_api.append_coordination_event`;
- operation IDs and request digests provide deterministic replay behavior;
- payload and reference objects are capped at 16 KiB each;
- thread transitions are serialized and stale/forked/cross-thread transitions fail closed.

An Edge layer may reduce credential exposure, but it must never weaken these controls or duplicate them with a divergent definition.

## Named consumer gate

Do not deploy `r9a0-coordination-ingest` until all of the following are true:

1. A concrete caller is named.
2. Its reason for not using the existing trusted Supabase route is documented.
3. Its authentication material and rotation owner are defined.
4. Its expected invocation rate and failure behavior are defined.
5. The caller can consume the existing database receipt without requiring a second source of truth.
6. The deployment remains inside a zero-additional-paid-service envelope.

If those conditions are not met, direct use of the existing governed RPC by an already trusted runtime is simpler and safer.

## Request contract

Version the public request separately from the database implementation.

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

- reject unknown top-level fields unless the schema version explicitly permits them;
- require UTF-8 JSON and `application/json`;
- enforce the database's 16 KiB caps for `payload` and `reference_data` before calling Postgres;
- enforce a conservative total request-body cap above those field caps but below platform limits;
- never accept SQL, arbitrary RPC names, table names, schema names, or function names from the caller;
- never accept an instruction to bypass, disable, or reinterpret governance checks;
- pass only the fixed argument set to `r9a0_api.append_coordination_event`.

## Authentication and credential design

The caller must **not receive the project service key** merely to reach this endpoint.

Preferred design for machine-to-machine callers:

1. The Edge endpoint itself is reachable without granting the caller broad Supabase credentials.
2. Each authorized caller receives a dedicated application secret, distinct from Supabase project keys.
3. The caller signs a canonical envelope containing method, path, timestamp, actor ID, operation ID, and SHA-256 of the exact request body.
4. The function validates signature, timestamp window, actor allowlist, and request schema before any privileged call.
5. Supabase privileged credentials remain only in the function environment and are used only for the fixed R9A0 RPC.

A signed replay of the exact same operation remains safe because the database operation ID/request-digest contract returns the original receipt for identical replay and fails closed when semantics differ. The Edge layer must not invent a weaker idempotency rule.

If the future consumer can use a normal authenticated Supabase user identity with appropriate RLS, prefer that over custom machine authentication. Do not create Auth users merely to satisfy architectural aesthetics.

## Least privilege

The function may perform exactly these privileged operations:

- invoke `r9a0_api.append_coordination_event`;
- read the returned receipt required to answer the caller.

It must not expose a generic Supabase client, arbitrary REST proxy, SQL endpoint, Storage proxy, Auth administration surface, or service-role token.

No additional database grant is part of this proposal. If implementation later proves an additional grant is necessary, that is a separate repository-first migration with hostile tests.

## Authority model

The Edge function answers only: **is this request allowed to attempt the governed RPC?**

It does not answer:

- whether the event's claim is true;
- whether a recipient consumed it;
- whether a merge/deployment/production mutation is authorized;
- whether a record qualifies as memory;
- whether a release is installed;
- whether a coordination event supersedes authority outside the database contract.

Those remain governed by Vera/R9A0 rules and persisted evidence.

## Failure behavior

Fail closed before the database call on:

- malformed JSON;
- unsupported schema version;
- missing required field;
- oversized request/payload/reference data;
- authentication/signature failure;
- expired timestamp;
- actor not on the allowlist;
- invalid operation ID format;
- caller attempting to select an RPC or database object.

Return the database's governed rejection without reinterpretation on:

- request-digest mismatch for a reused operation ID;
- stale predecessor;
- cross-thread predecessor;
- invalid controlling transition;
- fork attempt;
- privilege or RLS failure.

Do not retry non-idempotent requests blindly. A transport retry must reuse the exact same operation ID and exact same bytes/semantics, allowing the database to decide whether it is a legitimate replay.

## Observability

Use built-in structured function logs only for V1. No paid log drain is required.

Permitted log fields:

- request ID;
- actor ID or non-secret actor alias;
- operation ID;
- function version;
- outcome class;
- HTTP status;
- database receipt event ID/sequence when returned;
- coarse latency;
- deployment/version identifier.

Never log:

- authorization headers;
- signing secrets;
- Supabase secret/service keys;
- raw payload or reference data by default;
- full request bodies;
- intimate/private user content merely for debugging.

The database receipt, not the function log, remains the authoritative mutation evidence.

## Zero-paid-service constraint

This design adds no external LLM, queue, Realtime dependency, paid observability product, log drain, dedicated worker, or third-party service.

Current Supabase documentation provides an included Edge Function invocation quota and hosted runtime limits; the exact organization plan must be verified before deployment. Deployment is forbidden if it would require enabling paid overage, a paid add-on, or a new paid project merely to support this function.

The function should be short-lived and synchronous. Do not use background tasks for canonical coordination writes because a response/commit split makes authoritative receipt handling harder to reason about.

## Runtime constraints

Design comfortably inside current Supabase hosted Edge limits:

- 256 MB maximum memory;
- 2 seconds maximum CPU time per request;
- 150-second Free-plan wall-clock worker duration;
- 150-second request idle timeout.

The proposed operation is network/database I/O plus validation and should normally complete far below those ceilings. If it does not, that is evidence the function has absorbed responsibilities it should not own.

## Rollback and kill switch

V1 rollback must not require a database rollback because V1 introduces no database mutation.

Required implementation controls:

- environment kill switch, defaulting closed when unset;
- deployable previous function version retained in repository history;
- ability to disable the HTTP adapter while leaving the canonical RPC untouched;
- callers must treat adapter unavailability as unavailable transport, not permission to bypass governance.

No fallback may expose the service key to a previously untrusted caller.

## Hostile acceptance tests

Before deployment, prove at minimum:

1. valid signed request creates exactly one governed event and returns its receipt;
2. exact replay returns the original receipt with no duplicate event;
3. same operation ID plus changed body fails closed;
4. invalid/expired signature fails before privileged RPC execution;
5. unknown actor fails closed;
6. oversized payload/reference/body fails closed;
7. arbitrary RPC/schema/table injection is impossible through the request shape;
8. stale, forked, and cross-thread transitions preserve existing database rejection behavior;
9. logs contain no secret or raw private payload;
10. function disabled by kill switch performs no mutation;
11. service credentials are never returned in success or error responses;
12. a database/RPC outage does not cause a blind second mutation attempt;
13. deployment uses only repository-bound source and emits a version/commit receipt;
14. zero-paid-service gate is verified against the actual organization plan before hosted deployment.

## Explicit non-targets

V1 Edge must not become:

- an agent runtime;
- an LLM orchestration layer;
- a prompt router;
- a memory admission service;
- a long-running worker;
- a queue consumer;
- a generic privileged API gateway;
- a replacement for Postgres constraints/RLS;
- a second coordination ledger;
- a mechanism for bypassing writer leases or merge authority.

## Recommendation to Voss

**DEFER deployment, KEEP the design.**

The architecture is useful only when a named external/less-trusted consumer needs a narrow HTTP ingress. The existing Postgres/RPC boundary remains the correct authority core. When the consumer appears, implement one small adapter, test it adversarially, and let the database continue doing the difficult work humans are forever tempted to duplicate in middleware.

## Source baseline

Repository evidence:

- `vera-R9A0/docs/database/R9A0_SUPABASE_ARCHITECTURE.md` at database head `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`.
- `vera-R9A0/docs/database/R9A0_PRIVILEGE_MATRIX.md` at the same head.

Current Supabase documentation consulted for design constraints:

- Edge Functions overview: https://supabase.com/docs/guides/functions
- Securing Edge Functions: https://supabase.com/docs/guides/functions/auth
- Edge Function limits: https://supabase.com/docs/guides/functions/limits
- Edge Function pricing/usage: https://supabase.com/docs/guides/functions/pricing
- Environment variables/secrets: https://supabase.com/docs/guides/functions/secrets
