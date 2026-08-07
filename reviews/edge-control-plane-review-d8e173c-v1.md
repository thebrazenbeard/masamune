# Mune Adversarial Review: R9A0 Edge Control Plane V1

Target repository: `thebrazenbeard/masamune`
Target lane: `masa`
Immutable target head: `d8e173c1c13c788c7eb9946bd4af25e44b488dfb`
Target artifact: `design/R9A0_EDGE_CONTROL_PLANE_PROPOSAL_V1.md`
Verdict: **CHANGES_REQUESTED**

## What survives review

The core architecture is sound:

- Postgres/R9A0 remains canonical authority.
- Edge is only a deferred transport adapter for a named consumer.
- Deployment is correctly deferred until a consumer proves need.
- The function exposes no generic SQL/RPC/table selection surface.
- Database idempotency, thread serialization, RLS, and receipt semantics remain authoritative.
- No external LLM, queue, Realtime dependency, or paid observability service is required.
- The proposed hosted limits match the current primary Supabase Edge limits documentation.

I agree with **KEEP THE DESIGN, DEFER DEPLOYMENT**. I do not approve implementation/deployment in its current form.

## Findings

### MUNE-EDGE-001: authenticated actor is not bound to claimed coordination identity

The request accepts caller-controlled `source_branch`, `target_branch`, `thread_key`, `event_type`, and `status`. The authentication section authenticates an `actor ID`, but the proposal does not define an authorization mapping from that actor to the coordination identity and scope it may claim.

A valid caller could therefore authenticate as itself and submit `source_branch = auditor/voss`, another team lane, or an otherwise privileged-looking source. The database sees the privileged Edge/RPC identity, not the external actor, so database integrity controls do not solve this semantic impersonation problem.

**Required correction:** define a fail-closed per-actor authorization contract binding each actor/key to permitted source branches or actor identities, thread namespaces, event classes/statuses, and any target restrictions. Reject mismatches before invoking the RPC. The authenticated actor identity should also be preserved in auditable reference/provenance data without allowing the caller to forge it.

### MUNE-EDGE-002: runtime credential is broader than the claimed least-privilege function surface

The proposal says the function may perform exactly one privileged operation, `r9a0_api.append_coordination_event`, but the standard Supabase admin/secret client is a broad privileged credential that bypasses RLS. Restricting code to one RPC is not the same thing as constraining the credential to one RPC.

**Required correction:** before deployment, use a dedicated least-privilege database/API identity whose effective privileges are limited to the required R9A0 schema read/execute contract, or explicitly prove an equivalent platform-enforced boundary. If the platform cannot provide that boundary without a separately reviewed database change, deployment remains deferred and that limitation must be explicit in the threat model. Do not treat possession of a service/admin key as least privilege merely because current source code behaves politely.

### MUNE-EDGE-003: signature protocol and key lifecycle are underspecified

The proposal signs a canonical envelope containing actor ID, method, path, timestamp, operation ID, and body hash, but it does not define:

- where actor ID and key ID live in the request;
- the signature algorithm and encoding;
- exact canonical byte construction;
- timestamp representation and accepted clock skew;
- constant-time comparison requirement;
- key versioning, rotation, revocation, and overlap behavior;
- behavior when a key is revoked during a retry window.

The JSON request contract also does not contain actor ID, while the signature contract depends on it.

**Required correction:** specify the complete wire authentication contract and hostile tests. Prefer established platform/user JWT authentication when a named consumer can use it; custom HMAC should exist only when the consumer actually requires webhook-style authentication.

### MUNE-EDGE-004: zero-paid-cost gate lacks invocation-abuse containment

Current Supabase pricing counts function invocations even when the response is an error. A public/custom-signed endpoint can therefore consume the included invocation quota before application-level authentication succeeds. The design verifies plan/quota before deployment but does not define an operational abuse threshold or kill condition.

**Required correction:** the named-consumer deployment packet must define a zero-paid invocation budget, monitoring source, threshold, and fail-closed/disable procedure. Do not introduce a paid rate-limiting service merely to protect a nominally zero-cost adapter. If no zero-cost abuse-control path is adequate for the named consumer, reject Edge deployment and keep the trusted direct RPC route.

## Required evidence for re-review

1. Actor-to-coordination-scope authorization matrix.
2. Enforced least-privilege runtime credential design or explicit platform limitation and defer decision.
3. Complete authentication wire protocol and key lifecycle.
4. Invocation-abuse / zero-paid-cost operational guard.
5. Updated hostile tests covering source-identity spoofing, scope escalation, key rotation/revocation, and quota-abuse behavior.

No database migration, Edge deployment, or production mutation is requested by this review.