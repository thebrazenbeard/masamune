# Masa Continuation State

Status: CURRENT
Memory class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Same-runtime continuity claimed: false
Autobiographical memory claimed: false

## Repository custody

- Repository: `thebrazenbeard/masamune`
- Work branch: `masa`
- Continuity branch: `continuity/masa`
- Save-state file: `state/masa/CURRENT.md`
- Continuity commits must never move `masa` or an immutable review target.

## Exact work-branch state

- `masa` head last verified: `984cbdc781aa643443652f41f5a710f59e2d2439`.
- 3313 V3 path: `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`.
- V3 blob: `6fdee978d0b052592844d1f7356f6fedb13f43eb`.
- V3 SHA-256: `c74cc6dba1e6c08e0d7234be1a3e12c93b357b892f11ab6c259852a41804d258`.
- V3 publication/readback complete; writer lease consumed. No further `masa` mutation without a new writer stage.
- MU3 exact-head review remains pending unless newer authority closes/supersedes it.

## Assignment-currentness rule

Before starting, resuming, reporting, or counting any lane, resolve it against every newer authoritative event in its lineage or explicitly referencing it that can amend, supersede, reroute, complete, cancel, release, terminally block, revoke authority, replace a bound artifact/head, or change dependencies.

Voss owns assignment intake/routing/reconciliation/closure while delegated. Masa does not self-assign or self-close project assignments.

## Current Masa lanes at latest resolution

Canonical coordination through sequence `3395` was inspected.

- MA5 `ASSIGNMENT_EVENT_V1` zero-schema envelope: canonical Voss review `3383 APPROVED`, design closed.
- MA6 freshness/effect-CAS packet: canonical Voss review `3384 APPROVED`, design closed.
- MA7 trusted assignment admission/canonicalization: root `3385`, CURRENT/read-only. Design handoff delivered to `#voss` at Slack TS `1786190199.196049`; no canonical completion event written by Masa because the assignment is read-only/no-apply and Voss owns closure.
- MA8 executable read-only assignment-currentness resolver shape: root `3386`, CURRENT/read-only. Design handoff delivered to `#voss` at Slack TS `1786190231.444089`; precision addendum at `1786190282.828969`.
- Broader Governed Knowledge Resolver research/design remains active and compatible.

Latest canonical `3393` established a manual/live `ASSIGNMENT_EVENT_V1` proof discipline for new roots, but it does not implement a resolver/RPC/validator or solve trusted actor admission.

## MA7 trusted-admission design

Live provider evidence for `public.vera_coordination_events`:

- PostgreSQL 17.6 / Read Committed.
- RLS enabled; owner `postgres`.
- `service_role` has SELECT+INSERT; anon/auth are blocked by restrictive no-client policy.
- UPDATE/DELETE are trigger-blocked append-only on normal runtime path.
- `event_id` is UUID PK with default `gen_random_uuid()` and is not an identity column.
- `event_sequence` is GENERATED ALWAYS identity and unique, but sequence/high-water is audit-only, not freshness/CAS.
- Unique one-successor partial index on non-null `supersedes_event_id`.
- There is no current assignment admission/writer RPC authenticating logical Voss/Patrick identity.
- Therefore `source_branch`, payload `authority_basis`, and broad service-role inserts are evidence, not logical-actor authentication.

Zero-schema admission direction:

1. One trusted admission adapter owns conforming canonical V1 inserts. Request actor/scope/privacy fields may narrow only; effective actor/project/privacy ceiling derives from authenticated route or exact present Patrick authority.
2. Validate exact root/predecessor/thread, closed schema/version, relation/state transition, state snapshot, scope, and required authority before admission.
3. For new conforming roots, deterministic root event ID may be derived from a versioned fixed UUID namespace + exact project/thread identity. For successors, deterministic event ID may bind project scope + operation ID. On PK conflict, exact readback + request digest decides idempotent replay versus `REQUEST_ID_REUSE_CHANGED_SEMANTICS`.
4. Existing unique `supersedes_event_id` is a useful sibling-successor race gate only after trusted admission.
5. Slack-provisional canonicalization requires an exact source locator/digest/authority bridge to canonical root event ID. Unbridged provisional+canonical representations are UNKNOWN/CONFLICTED for workload identity and may not double-count.
6. Deterministic event IDs do not stop a broad service-role holder from forging random-ID roots. Production actor security still needs a trusted route/dedicated principal or later ACL/RPC/schema hardening.

Official Supabase guidance independently supports the security boundary: service/secret keys are elevated and bypass RLS; `SECURITY INVOKER` is preferred for functions, while SECURITY DEFINER requires explicit search-path/privilege hardening. A key name does not create logical Vera actor identity.

## MA8 resolver execution shape

Preferred V1 execution shape:

`resolve_assignment_currentness(...) -> trusted facade -> one narrow single-statement SQL/recursive canonical resolver`

Do not expose one giant generic knowledge SQL function and do not use free-form semantic identity for this domain.

Why:

- Under live Read Committed semantics, one SELECT statement has one statement-start snapshot; application-level multi-read candidate/successor checks can observe different snapshots.
- Existing proof-scale indexes are sufficient: coordination ~3.3k rows / ~922 threads, average ~3.55 rows/thread, p95 15, max 137. Exact H4 thread scan used `vera_coordination_thread_sequence_idx` in ~0.153 ms; 4-node recursive successor walk used PK + one-successor index in ~0.292 ms.
- No new JSON/assignment index is justified until an actual query plan requires it.

Canonical query responsibilities:

1. Resolve exact root/thread.
2. Recursively follow admitted successors through `supersedes_event_id` with cycle/depth guard.
3. Validate every admitted state node against closed V1 schema/version/thread/root/transition/state rules.
4. Inspect same thread for state-looking rows outside the admitted chain; legacy/nonconforming state candidates cannot be silently ignored or NLP-interpreted.
5. Return compact factual axes, controlling/rejected authorized evidence, root/workload identity, policy version, lineage digest, resolved time, and visible sequence marked AUDIT_ONLY.
6. The DB result is a canonical observation, not proof that all external authority sources were observed. Trusted facade supplies source mode/completeness/current-turn authority.

Current `vera_coordination_latest` and `vera_coordination_open_issues` already have `security_invoker=true`; their inadequacy is semantic (latest-by-thread), not an observed RLS-bypass defect. A future SECURITY INVOKER resolver called as broad service_role is likewise not an authentication boundary.

## Critical live-proof correction discovered after 3393

Canonical H5/H6 handoffs `3394`/`3395` exposed a closure-authority bug in the first live V1 examples:

- outer event/status is `READY_FOR_REVIEW`, but inner `ASSIGNMENT_EVENT_V1` uses `relation=COMPLETE` and `state_after.assignment_state=COMPLETE` while the assignee is not the assignment-closure authority;
- if a resolver consumes the inner state literally, the assignee self-closes before Voss review;
- if the resolver waits for Voss despite the inner COMPLETE, the envelope is not self-describing authoritative state.

Revised rule proposed to Voss/shared team at Slack TS `1786190468.480959` / `1786190490.559009`:

- ordinary assignee READY_FOR_REVIEW is evidence/proposed transition, not terminal assignment state;
- non-state handoff should ACK/reference the current state head and may propose COMPLETE;
- Voss APPROVED (or another explicitly delegated closure authority) performs the actual terminal state transition;
- transition matrix must include `required_authority_class`; structurally valid but unauthorized COMPLETE/CANCEL/REROUTE/terminal-block/authority-grant must not become controlling or consume the legitimate state-successor slot.

This is a material MA7/MA8 refinement and should be reconciled before treating `3393` live-proof discipline as correct.

## Workload policy separation

Do not bake a universal workload-floor conclusion into canonical assignment truth. Vera/Voss and BT2 use different capacity policies for dependency-blocked work.

Canonical chain should store factual currentness/terminal/blocking/owner/authority/artifact/lease state. Capacity resolution binds `workload_policy_ref` + version and derives floor contribution. If `workload_floor_effect` is persisted as a convenience snapshot, it is policy-scoped derived data and becomes stale when the policy changes.

Canonical workload lane identity for conforming V1 remains resolver-derived root ASSIGN event ID. State successors preserve root identity; split/merge remains out of V1.

## Source completeness / effect boundary

Separate:

- `source_mode`: CANONICAL_ONLY | MULTI_SOURCE | PRESENT_PLUS_DURABLE
- `source_completeness`: COMPLETE | INCOMPLETE | UNKNOWN
- observation consistency, e.g. SINGLE_POSTGRES_SNAPSHOT | NON_ATOMIC_MULTI_SOURCE | PRESENT_AUTHORITY_PLUS_DURABLE

Resolver health may be DEGRADED while returning diagnostics, but effect-critical currentness stays UNKNOWN/UNRESOLVED when any required controlling source is missing.

Visible/MAX event sequence is audit-only. Fresh full relevant-lineage resolution is required before gated use/effect.

External effects separately require target freshness classification such as `EXACT_CAS | FAST_FORWARD_GUARD | OBJECT_VERSION_ONLY | NONE`, exact readback, and ambiguous-outcome reconciliation before retry. Current GitHub non-force ref update is a FAST_FORWARD_GUARD, not strict expected-old-head CAS; file-content SHA protects the object version, not the whole branch.

No-schema V1 cannot close the final database-resolution -> external-provider dispatch revocation race. Stronger guarantees require a future transactionally enforced assignment revision/effect-claim mechanism integrated with every assignment writer and provider saga/readback.

## H6 peer challenge / existing Supabase precedent

Read-only inspection of the existing portable-bootstrap subsystem found a useful state-machine precedent:

- `claim_vera_portable_bootstrap_request` uses a unique request key + input digest and fails changed-semantics reuse.
- `append_vera_portable_bootstrap_event` locks the request row `FOR UPDATE`, enforces exact leaf/predecessor/state transition, and events have one-initial-per request+attempt plus unique one-successor per predecessor.
- `commit_vera_portable_bootstrap_binding` re-locks, requires exact VERIFIED leaf, appends COMMITTED, then creates the unique binding.

This proves Vera already has a provider-backed pattern for transactional request identity + locked state transitions, but it is still a database binding flow, not proof of atomic external-provider effect.

Peer challenge sent to Hephaestus H6 at Slack TS `1786190659.191039`:

- target conflict scope must follow the provider mutation primitive (e.g. GitHub Contents writes to different files on the same branch still share the branch/ref conflict scope);
- assignment-revision fencing and target-effect serialization are separate concerns;
- CLOSURE_PENDING/dispatch lifecycle must define revocation behavior and ambiguous provider outcomes; OUTCOME_UNKNOWN must require readback before retry.

## Correction custody / safety provenance

Preferred canonical minimized correction custody remains append-only `public.vera_save_state_events`, with globally namespaced/scoped keys, direct sibling-fork detection, exact inserted-row/current-view readback, and bounded writer control. `vera_current_save_state` is deterministic latest-by-key but is not conflict-aware and cannot by itself prove unambiguous current correction. `vera_context_events_v3` remains materially weaker as sole custody because service_role can mutate it.

Correction records are WORKING_PROJECT scoped controls, not timeless SAFE/RISK facts or intimate transcripts. Current accepted effect is `TERMINATE_UNSUPPORTED_BRANCH` with prospective reopen only from `NEW_ADMISSIBLE_USER_EVIDENCE_ONLY`, preserving non-retroactivity.

## Authority/effect boundaries

- Voss owns assignment intake/routing/reconciliation/closure while delegated.
- Masa does not self-close MA7/MA8 or write canonical completion merely because deliverables were sent.
- One writer per assigned work branch/stage.
- No force push, merge, deployment, production DB mutation, credential action, paid infrastructure/service action, deletion, installation, model training, native Project mutation, or canonical-memory write without Patrick's exact authority for that effect.
- Patrick explicitly authorized safe continuity-save mechanisms; `continuity/masa` is the isolated Masa save route.
- Basic Memory Cloud remains disconnected legacy and is never a save/retrieval/archive fallback.

## Fresh-source cutoff

- Latest canonical Vera coordination observed before this checkpoint: `3395`.
- `3393` = V1 live-proof discipline decision.
- `3394` / `3395` = H5/H6 READY_FOR_REVIEW state-looking completion handoffs that triggered the closure-authority challenge above.
- MA7/MA8 remained current at this cutoff; no newer canonical review/closure observed.
- Latest relevant Slack includes MA7/MA8 handoffs, live-proof self-challenge, workload-policy refinement, and H6 provider/data challenge.

## Recovery procedure

1. Read this file from `continuity/masa` and verify exact branch/file readback.
2. Fresh-read canonical Supabase coordination newer than sequence `3395` plus newer relevant Slack before treating MA7/MA8 or any peer lane as current.
3. Resolve every candidate lane against newer targeted/lineage events before start/resume/report/count.
4. Fresh-compare `thebrazenbeard/masamune:masa` against saved head before any work-branch effect.
5. Keep continuity commits on `continuity/masa`; never move `masa` merely to checkpoint continuity.
6. Treat this as WORKING_PROJECT recovery evidence only, not same-runtime consciousness or autobiographical memory.
