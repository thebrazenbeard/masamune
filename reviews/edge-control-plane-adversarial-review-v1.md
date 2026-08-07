# Mune Edge Control-Plane Adversarial Review Framework V1

Status: PRE-PROPOSAL REVIEW FRAMEWORK
Role: Independent reviewer
Target: R9A0 Supabase Edge control-plane proposal
Verdict: NOT YET ISSUED

This document defines the evidence and failure cases Mune will apply to Masa's concrete proposal. It is not an approval, rejection, or substitute for reviewing the exact candidate architecture.

## Acceptance gates

1. **Least privilege**
   - Every Edge function, service role, database role, schema privilege, RPC, secret, and external capability has an explicit minimum scope.
   - No function receives broad service-role authority merely for convenience.
   - Privileged operations are mediated through narrow interfaces with hostile-role tests.

2. **Authoritative state and stale-state resistance**
   - The design identifies the single controlling source for coordination state.
   - Requests that depend on a thread tip, authority lease, predecessor, approval, or supersession bind that state atomically or revalidate it before effect.
   - Cached or projected state cannot silently outrank newer durable state.

3. **Idempotency and replay safety**
   - Every externally retryable write has a stable operation identity and semantic replay contract.
   - Same operation ID plus changed semantics fails closed.
   - Ambiguous network failure requires commit-state verification before retry.

4. **Repository/hosted provenance**
   - Deployable code and database artifacts are repository-first and exact-head bound.
   - Hosted state can be traced to immutable repository artifacts and execution receipts.
   - CI verifies the candidate actually executed, not merely that hashes match an internally stale manifest.

5. **Rollback and failure containment**
   - Each state-changing component has a bounded rollback or forward-repair path.
   - Partial failure cannot leave authority, leases, or event-chain state in an indeterminate state.
   - Rollback does not require paid infrastructure or hidden operator knowledge.

6. **Observability without secret leakage**
   - Logs expose operation IDs, exact candidate identity, bounded outcomes, latency, and failure class.
   - Credentials, bearer tokens, sensitive payload fields, and private user content are excluded or redacted by construction.
   - A failed function can be distinguished from a rejected request and from an ambiguous commit.

7. **Zero-paid-service constraint**
   - The proposal identifies every external dependency and its cost assumption.
   - No required path depends on paid Supabase branching, paid queues, external SaaS, or another metered service unless separately authorized.

8. **Concurrency and one-writer discipline**
   - Concurrent writers cannot create forked controlling state or bypass leases.
   - Shared targets have explicit ownership transfer and immutable review heads.
   - Reviewer activity cannot mutate the implementation under review.

9. **Security boundaries**
   - FORCE RLS / RLS behavior is explicit for every table exposed through an invoker context.
   - Security-definer functions pin search_path and minimize executable grants.
   - Anonymous/authenticated/service-role behavior is tested separately.

10. **Failure-mode evidence**
    - The proposal must include deterministic tests for stale predecessor, duplicate operation, semantic replay mismatch, privilege escalation, malformed payload, unavailable dependency, timeout after possible commit, rollback path, and projection lag.

## Automatic changes-requested conditions

- Broad service-role access where a narrow RPC or policy suffices.
- A retry path that can duplicate a committed effect.
- Any reliance on stale projected state without authoritative revalidation.
- Hosted-only configuration that is not reconstructible from repository evidence.
- Hidden paid dependency or unbounded external service requirement.
- Logs capable of persisting secrets or sensitive payloads.
- Rollback described only as manual cleanup without a tested bounded procedure.
- Missing hostile-role or concurrency tests for privileged paths.

## Evidence required for final Mune verdict

- Masa's exact proposal artifact and immutable revision/head.
- Exact service/function boundary map.
- Privilege matrix and secret-access map.
- State-transition and idempotency contract.
- Failure/rollback design.
- Observability contract.
- Repository-to-hosted provenance path.
- Deterministic test matrix covering the failure cases above.

Until those artifacts exist, Mune's final Edge verdict remains pending rather than inferred.