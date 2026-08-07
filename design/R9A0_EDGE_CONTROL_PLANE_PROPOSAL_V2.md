# R9A0 Edge Control-Plane Proposal V2

**Author lane:** Masa
**Status:** CORRECTION_CANDIDATE_READY_FOR_MUNE_REREVIEW
**Supersedes as review target:** `design/R9A0_EDGE_CONTROL_PLANE_PROPOSAL_V1.md` V1/V1.1
**Core verdict:** KEEP narrow transport-adapter architecture; DEFER deployment
**Deployment authorized:** No
**Paid-service dependency permitted:** No

## Normative composition

This V2 candidate consists of this file plus the fully revised V1.1 design at the same immutable `masa` head. This file is the controlling V2 delta and acceptance contract. If wording conflicts, V2 controls.

## Mune findings disposition

### MUNE-EDGE-001: semantic actor impersonation

**Resolved in design.** Authentication and semantic authorization are separate gates.

Every actor has a default-deny record binding:

- `actor_id`;
- permitted `key_id` values;
- permitted `source_branch` values;
- permitted `thread_key` prefixes;
- permitted event types;
- permitted target prefixes;
- enabled/disabled state.

A correctly signed request still fails before database execution if the caller tries to claim another actor's branch, thread scope, event class, or target scope. Wildcard scope requires explicit governing authority and hostile tests.

### MUNE-EDGE-002: broad Edge admin/service credential

**Resolved by rejecting `service_role` as the deployable Edge credential.**

A future implementation requires a repository-first database privilege package that creates a dedicated execution principal such as `r9a0_edge_ingest` with no ownership, no broad platform-role membership, and no general table privileges.

Permitted database capability is limited to:

- connect as necessary;
- `USAGE` on `r9a0_api`;
- `EXECUTE` on exactly one fixed governed append path or a thin wrapper that delegates to the existing authoritative transition logic.

No direct table mutation, generic read access, Auth administration, Storage administration, Realtime administration, arbitrary RPC, or unrelated-schema access is allowed.

If the existing append function's caller check accepts only a service-role JWT, a future repository-first migration must add a dedicated `session_user` authorization path or a thin wrapper without duplicating state-transition semantics.

The Edge environment holds only the dedicated principal credential. If that narrow principal cannot be implemented cleanly, **Edge deployment is rejected** rather than falling back to `service_role`.

Credential creation itself remains a separately authorized future action and is not performed by this proposal.

### MUNE-EDGE-003: underspecified signature and key lifecycle

**Resolved with one fixed V1 transport signature scheme.**

Required headers:

- `X-Vera-Actor`
- `X-Vera-Key-Id`
- `X-Vera-Timestamp`
- `X-Vera-Signature`

Algorithm: HMAC-SHA-256 only. No algorithm negotiation.

Canonical signed bytes are:

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

Rules:

1. method is exactly uppercase `POST`;
2. path is exactly `/functions/v1/r9a0-coordination-ingest`;
3. timestamp is unsigned base-10 epoch seconds with no padding/decimal;
4. actor/key/operation IDs must match parsed request values exactly;
5. body hash covers exact received raw bytes before JSON reserialization;
6. signature is strict lowercase hex HMAC-SHA-256;
7. comparison is constant-time after strict decoding;
8. accepted clock skew is ±300 seconds;
9. keys are actor-specific and never shared;
10. only ACTIVE keys authenticate new requests;
11. rotation may temporarily expose one ACTIVE and one RETIRING key for at most 24 hours;
12. REVOKED key IDs fail immediately and cannot be reactivated under the same ID;
13. key material never enters repository, logs, coordination payloads, receipts, or errors.

Database operation-ID/request-digest logic remains the authoritative semantic replay rule.

### MUNE-EDGE-004: zero-paid invocation abuse

**Resolved by making the limitation an explicit deployment gate rather than pretending in-function rejection is free.**

Rejected Edge requests can still consume invocation quota. Therefore function-internal auth/rate limiting cannot prove zero paid cost under volumetric abuse.

Deployment is forbidden unless the implementation packet proves at least one of:

1. no-additional-cost pre-invocation platform restriction/rate limiting that bounds counted calls; or
2. an already-available, separately governed, no-cost upstream boundary that limits caller population and rate before Edge invocation; or
3. verified included quota plus worst-case caller model proves paid overage cannot occur and paid overage is disabled.

The deployment receipt must bind current values for included invocation quota, an Edge-specific monthly budget, hourly rejection budget, paid-overage disabled state, the pre-invocation control, and its evidence locator.

The administrative kill threshold is **80% of the Edge-specific budget or the separately bound hourly rejection budget, whichever triggers first**. Crossing it requires disabling/undeploying the adapter at the platform layer. Merely returning 429/503 from inside the function is not considered a quota kill because that invocation has already occurred.

If no zero-paid pre-invocation control can be proven, V2's deployment verdict is **DO NOT DEPLOY**.

## Authority and state boundary

PostgreSQL remains canonical authority. The Edge adapter may only:

1. authenticate caller;
2. authorize actor semantic scope;
3. validate bounded request shape;
4. call one fixed governed database path;
5. return the database receipt.

It may not decide truth, merge/deployment authority, memory admission, release installation, writer leases, or supersession outside the database contract.

## Required hostile tests

A future implementation must prove at minimum:

- actor cannot claim another `source_branch`;
- out-of-scope thread/event/target is rejected before DB execution;
- modified raw body invalidates signature;
- actor/key mismatch fails;
- timestamp outside ±300 seconds fails;
- revoked key fails;
- malformed hex does not leak comparison information;
- exact replay is idempotent;
- same operation ID with changed semantics fails;
- dedicated Edge DB principal cannot access unrelated tables/RPCs;
- no broad service credential is present in the function environment;
- stale/fork/cross-thread DB rejection remains unchanged;
- secrets/raw private payloads are absent from logs;
- ambiguous network failure does not trigger blind duplicate mutation;
- current zero-paid budget evidence is verified;
- budget-threshold exercise demonstrates the documented platform-level disable procedure.

## Current implementation decision

**No Edge implementation or deployment is currently justified.**

The design is retained because it provides a defensible future boundary if a named less-trusted consumer appears. Until then, existing trusted runtime access to the governed database contract is simpler and has less attack surface.

## Provenance

- Source Masa candidate head: `d8e173c1c13c788c7eb9946bd4af25e44b488dfb`
- Mune review sequence: `3263`
- Mune review commit: `fbb1560fcdafb2cf368e6306577f9b88a6e1980e`
- Revised V1.1 commit: `b1dd8ddb96ee39fed858b2b821fd8ca42efef639`
- Voss correction assignment: `3267`
