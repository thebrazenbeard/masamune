# Mune Review — R9A0 Edge Implementation Readiness

**Assignment:** Vera coordination 3311
**Reviewer lane:** Mune
**Reviewed exact head:** `3e5290a096a7069c9b194470ae6d0efa2830b41d`
**Reviewed artifact:** `design/R9A0_EDGE_IMPLEMENTATION_READINESS_SPEC_V1.md`
**Source design:** `design/R9A0_EDGE_CONTROL_PLANE_PROPOSAL_V2.md` at `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`
**Prior design verdict:** `APPROVED_DESIGN_KEEP_AND_DEFER`

## Verdict

`APPROVED`

This approval is for the implementation-readiness **specification** only. It does not mean the Edge adapter is ready to build or deploy.

## Findings

1. **KEEP_AND_DEFER is preserved.** The candidate requires a named consumer with a real credential-boundary problem and explicitly says that no consumer means no implementation.
2. **Least privilege is preserved.** Deployable Edge is forbidden from holding `service_role`; the future packet must use a dedicated narrow database principal with no ownership, broad role membership, table mutation rights, or unrelated RPC/schema capability. Failure to realize that principal cleanly requires rejecting Edge rather than widening privilege.
3. **Semantic actor authorization remains separate from authentication.** Actor records bind permitted source branches, thread prefixes, event types, target prefixes, key IDs, and enabled state under default deny.
4. **Transport identity and replay semantics are sufficiently specified.** The fixed HMAC-SHA-256 request identity, key lifecycle, exact raw-body binding, operation ID, and database-authoritative idempotency rules preserve the approved V2 boundary.
5. **Ambiguous commit handling is correct.** Receipt lookup by operation ID precedes any retry after an uncertain transport failure, preventing blind duplicate mutation.
6. **Zero-paid-cost posture fails closed.** The candidate correctly treats rejected invocations as potentially quota-consuming, requires current plan/quota/overage evidence and a pre-invocation or bounded-caller control, and forbids deployment when paid overage cannot be excluded.
7. **Hosted effects remain gated.** The repository-first packet, database principal creation, credentials, deployment, hosted migration/apply, and cost evidence are all future separately authorized effects.
8. **Hostile-test coverage is adequate for readiness.** The required suite covers actor impersonation, scope denial, key lifecycle, HMAC integrity, idempotency, narrow-principal privilege, stale/fork/cross-thread rejection, ambiguous commit, redaction, rollback, and zero-paid fail-closed behavior.

## Scope implications

- Assignment 3311 is satisfied at the review/specification level.
- `DESIGN_READY` may remain true.
- `IMPLEMENTATION_PACKET_READY_TO_BUILD` remains false until the named consumer, exact principal mechanism, exact budget/quota evidence, lifecycle owners, and other deployment-bound values are frozen.
- `HOSTED_DEPLOYMENT_READY` remains false.
- This verdict grants no merge, repository implementation write, migration/apply, deployment, credential, paid-service, or production authority.

## Independent-review boundary

Mune did not modify Masa's reviewed artifact or branch. This review is independent evidence only.
