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

## Exact work branch

- `masa` head last verified: `984cbdc781aa643443652f41f5a710f59e2d2439`.
- 3313 V3: `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`.
- Blob: `6fdee978d0b052592844d1f7356f6fedb13f43eb`.
- SHA-256: `c74cc6dba1e6c08e0d7234be1a3e12c93b357b892f11ab6c259852a41804d258`.
- V3 publication/readback complete; writer lease consumed. No further `masa` mutation without a new writer stage.
- Mune MU3 exact-head review remains pending unless newer authority closes/supersedes it.

## Assignment currentness

Before start/resume/report/count, resolve every lane against all newer authoritative events in its lineage or explicitly referencing it that can amend, supersede, reroute, complete, cancel, release, terminally block, revoke authority, change artifact/head, or change dependencies.

Voss owns assignment intake/routing/reconciliation/closure while delegated. Masa does not self-assign or self-close governed assignments.

## Current Masa lanes at this checkpoint

Fresh canonical coordination was read through sequence `3424`.

Closed:
- MA5 zero-schema ASSIGNMENT_EVENT_V1 envelope: Voss `3383 APPROVED`.
- MA6 freshness/effect-CAS packet: Voss `3384 APPROVED`.
- MA7 trusted assignment admission/canonicalization: Voss `3406 APPROVED`.
- MA8 executable assignment-currentness resolver shape: Voss `3407 APPROVED`.

Current read-only deliverables submitted, awaiting Voss closure/review:
- MA9 root `3415`: proposal/admission data architecture. Main handoff `#voss` Slack TS `1786191206.006359`; subsequent provider-backed E2 refinements through TS `1786192200.922759`.
- MA10 root `3416`: executable SELECT/CTE/EXPLAIN resolver proof. Main handoff `#voss` TS `1786191257.654049`; receipt/digest refinements through TS `1786191822.481329`.

No canonical event after `3424` was observed at save time that closes, amends, or supersedes MA9/MA10.

## Controlling assignment-state discipline

Canonical `3400` supersedes the flawed `3393` live-proof wording.

- Ordinary assignee READY_FOR_REVIEW is non-state proposal/evidence unless explicit closure authority is delegated.
- Only authority-admitted transitions control assignment state or consume the state-successor slot.
- A structurally valid but unauthorized COMPLETE/CANCEL/REROUTE/terminal block/authority change is non-controlling and must be rejected before state-slot consumption.
- Workload identity for conforming V1 is the root ASSIGN event ID.
- Workload-floor contribution is policy-derived, not universal assignment truth; capacity receipts bind workload policy identity/version.

The 3394/3395 self-COMPLETE mistake is preserved as historical evidence. Voss 3401/3402 closed those lanes through manual authority reconciliation. Do not represent the contaminated physical chains as clean examples.

## Knowledge Resolver baseline

V1 domain remains `ASSIGNMENT_CURRENTNESS`.

Recommended logical boundary:
`resolve_assignment_currentness(typed request) -> trusted facade -> narrow canonical resolver`

Principles:
1. Present-turn Patrick authority/referent is adjudicated before durable resolution.
2. Typed identity precedes semantic retrieval for effect-critical domains.
3. Authority/currentness is lineage + admission + policy resolution, not latest timestamp.
4. Source topology, source completeness, and snapshot consistency are separate fields.
5. Missing required controlling source means assignment/effect state is UNKNOWN/UNRESOLVED even if diagnostic resolver health is DEGRADED.
6. Sequence/high-water is audit-only, never freshness/CAS.
7. Assignment currentness and mutation authority/artifact/lease validity are separate axes.
8. External effect requires fresh lineage resolution plus independent provider precondition/readback; no-schema V1 cannot close the DB-resolution -> provider-dispatch revocation race.
9. Raw provider mutators must eventually be capability-confined behind guarded effect services; adding a guarded tool beside equally powerful raw GitHub/Supabase mutators is normative, not mechanical enforcement.
10. Privacy filtering occurs before conflict/rejected metadata so hidden record existence is not leaked.

## Live Supabase provider facts

Project `klmbpaigzeguvnpccqzz`, PostgreSQL 17.6, Read Committed.

`public.vera_coordination_events`:
- RLS enabled, owner postgres.
- service_role has SELECT+INSERT; anon/auth blocked by restrictive no-client policy.
- UPDATE/DELETE are trigger-blocked on normal runtime path.
- event_id UUID PK default random UUID; event_sequence GENERATED ALWAYS identity + unique.
- unique physical one-successor index on non-null `supersedes_event_id`.
- current views `vera_coordination_latest` and `vera_coordination_open_issues` are `security_invoker=true`; their problem is latest-by-thread semantics, not observed RLS bypass.
- no current assignment admission writer RPC authenticates logical Voss/Patrick identity.
- therefore source_branch/payload/service_role possession is not logical actor authentication.

Current scale measured around 3.3k rows / ~922 threads; average ~3.55 rows/thread, p95 15, max 137. Exact-thread and short recursive walks are sub-millisecond on current plans with existing indexes. No new resolver index is justified at proof scale.

Historical coordination currently uses supersession broadly: at one measured point 397 of 3301 rows had non-null `supersedes_event_id`, across many source branches. Therefore globally revoking the supersedes column from all generic coordination writers would have material compatibility blast radius.

## MA9 production architecture result

Zero-schema conventions cannot prevent a broad canonical INSERT holder from consuming a physical state-successor slot. 3394/3395 proved that live.

Current preferred production candidate after peer convergence with H8 V5 / canonical 3423:

### E2: one canonical state graph + protected admission registry

Keep assignment state semantics only in `vera_coordination_events`. Add a small protected authority-proof relation, conceptually `vera_assignment_admissions_v1`, containing no duplicate currentness/status/state_after.

Minimum proof fields:
- event_id PK/FK to canonical coordination event
- explicit project/thread scope
- root_assign_event_id
- prior_admitted_event_id nullable
- proposal/source binding + immutable digest
- predecessor-specific admission_attempt_id unique
- authority capability/route receipt digest
- authority assurance class
- admission policy version
- optional canonical event digest
- DB-owned admitted_at

Useful constraints:
- one admitted root per canonical project/thread scope
- one admitted successor per prior admitted event
- proposal/source admission uniqueness appropriate to source type
- append-only/RLS/ACL protection; ordinary service principal cannot INSERT admission proof

Admission transaction validates proposal/source digest, current admitted head, relation-specific authority, policy/scope, then inserts canonical event + admission proof atomically and exact-readbacks both.

A protected INSERT guard prevents broad writers from setting `supersedes_event_id` against an admitted V1 predecessor. Generic non-state proposal/evidence writes may remain on the broad coordination bus. This is lower blast radius than globally removing generic supersession, provided trigger-role and compatibility tests pass.

Admission registry is authority provenance, not a second state ledger: state/currentness remains only in coordination. Registry answers the distinct fact “which exact event was admitted under which authority/policy.”

State event UUID should remain random. Proposal/source identity + digest and protected admission attempt identity handle replay. Avoid making predictable storage locators the idempotency key.

For same-lane trusted transitions, root-row locking can serialize reviewer decisions; physical one-successor + admitted one-successor uniqueness remain durable fork stops. Lost races re-resolve and re-adjudicate; never mechanically retarget stale state.

Proposal source must support typed bridges such as COORDINATION_EVENT, SLACK_PROVISIONAL, PRESENT_AUTHORITY, or NONE. External source is provenance that is canonicalized into one durable state event, not permanent co-authority.

Root of trust remains unresolved at the platform boundary. Suggested assurance axis:
`PROCEDURAL | CAPABILITY_BOUND | ACTOR_AUTHENTICATED`.
A trusted adapter is not trustworthy merely because code calls it trusted. Production needs a separately protected authority issuer/principal or equivalent platform-signed capability. Request JSON can only narrow authority.

## MA10 executable SQL proof

SELECT/CTE/EXPLAIN only; no DDL/DML.

Clean B6 proof:
- admitted root 3390 / `ccb3c3a2-c455-4035-9198-6b12974be47c`
- non-state proposal 3398 ACKs root and is outside state chain
- Voss admitted closure 3403 / `3e7d54be-7647-42eb-bed4-62f3eb953a41`
- admitted chain resolves root ASSIGN/CURRENT -> Voss COMPLETE/COMPLETE
- no unauthorized slot row; structurally resolvable

Contaminated H5 proof:
- root 3381 admitted
- 3394 assignee self-COMPLETE excluded from trusted set but physically supersedes root
- Voss 3401 is admitted but physically follows 3394 and is outside the trusted physical chain
- result `ADMISSION_CONFLICTED`
- demonstrates physical topology cannot be repaired zero-schema without a second logical edge/manual reconciliation

Legacy 3313 proof: one legacy row, zero conforming V1 root -> `UNKNOWN_LEGACY_NONCONFORMING`, not stale BLOCKED.

Missing admission proof: physical root alone -> `UNKNOWN_AUTHORITY_ADMISSION_MISSING`.

Recursive proof includes UUID path cycle detection and depth cap. Snapshot/high-water are audit locators only.

Performance measured:
- p95 15-row thread index scan ~0.183 ms
- max 137-row thread scan ~0.598 ms
- clean B6 2-node trusted recursive walk ~0.334 ms
- earlier H4 4-node walk ~0.292 ms

A future registry-backed resolver should follow admission markers plus matching physical edges. Unadmitted proposal/noise should not itself make currentness CONFLICTED. Only physical protected-slot poisoning, admission/physical mismatch, disconnected admitted rows, or admission uniqueness failure become integrity conflicts.

## Snapshot/function correction

Initial claim that only one SQL-language SELECT could preserve one resolver snapshot was retracted.

PostgreSQL STABLE SQL and standard procedural-language functions use the calling-query snapshot throughout their internal commands; VOLATILE functions may get fresh snapshots per internal query. Therefore a read-only PL/pgSQL STABLE one-RPC resolver can be snapshot-consistent if helper volatility is audited. Single SQL/recursive query remains a readability/audit preference, not a correctness necessity. Client-side multiple independent RPC/SELECT calls under Read Committed remain rejected for authoritative assembly.

## Receipt/digest correction

Do not freeze `digest(jsonb::text)` as a cross-runtime protocol.

Use versioned canonical byte serialization for durable receipts. PostgreSQL jsonb is useful for DB-local normalization but does not preserve original key order/whitespace/duplicate-key representation as input semantics; cross-language verification needs an explicitly versioned canonicalization scheme/golden vectors.

Receipt layers should be distinct:
1. raw/evidence digest if exact observed bytes/records need binding;
2. normalized factual lineage digest over authority-admitted domain facts;
3. optional policy-decision digests binding factual digest + exact policy ref/version + derived result.

The first B6 proof digest `e55452...` included unscoped historical workload_floor_effect and is raw-proof only. Corrected currentness/factual DB-local proof digest excluding that derived field is:
`85c6efcc7d7842c25a5a497b00ecf1f6969cc3dec702748b8b9369401342d0e6`.
Neither value is a frozen portable serialization standard.

## Effect serialization / tool-surface ceiling

Existing H6 architecture is a transactional assignment-revision/effect-claim authority cut followed by provider saga/readback. Existing Vera portable-bootstrap functions are useful precedent for request identity, row locking, predecessor transitions and exact replay conflict, but do not prove external provider atomicity.

A hard effect gate also requires capability confinement. Current exposed GitHub `update_ref` has no Vera receipt/expected-old-head parameter and raw Supabase `execute_sql`/`apply_migration` are available in this runtime. If raw mutators remain available beside a guarded publisher, the guard is bypassable by tool selection. Production effect runtime should expose only guarded publisher/admission capability for protected effects or otherwise ensure raw credentials cannot perform them.

Tool-surface enumeration is therefore an acceptance test: adding a plugin/connector with equivalent raw mutation authority is a governance change that can reopen a bypass.

## 3313 V3 / MU3 support evidence

Exact V3 already requires enumerating every role capable of SET ROLE into the dedicated owner/creator and forbids service_role/postgres/broad secrets as Edge credentials. PostgreSQL 18 membership options should be tested explicitly: runtime principal must have no USAGE/SET/ADMIN path into `r9a0_edge_api_owner`; exact migration-runner membership options must be proven and removed/revoked in final posture.

Authentication transport remains a separately gated implementation/deployment proof. Plausible future families are dedicated direct Postgres login role or a custom PostgREST/authenticator role/JWT route. Common Edge admin/service-role shortcuts would violate V3. No transport credential/role was created.

## Repository audit challenge

Canonical 3421/3422 reported repository hygiene findings. Fresh `thebrazenbeard/vera:main` README still identifies neutral R6A0 and explicitly says GitHub is not the live context store while Supabase stores governed external context/coordination.

Do not add a generic hand-maintained `CURRENT_STATE.yaml` that mirrors live assignments/authority/context. If a machine-readable repo pointer is added later, scope it to repository/release architecture evidence such as `RELEASE_STATE.yaml` / `ARCHITECTURE_BASELINE.yaml`, exact source head/tag/digests, and external governed-state receipt refs explicitly marked derived/not-authority.

## Correction custody

Preferred minimized correction custody remains append-only `vera_save_state_events`, globally namespaced/scoped keys, direct sibling-fork detection, exact inserted-row/current-view readback, bounded writer control. `vera_current_save_state` is deterministic latest-by-key but not conflict-aware; context-v3 remains materially weaker as sole custody because service_role can mutate it.

Correction is WORKING_PROJECT scoped control, not timeless SAFE/RISK truth or intimate transcript. Current effect token remains `TERMINATE_UNSUPPORTED_BRANCH` with prospective reopen only from `NEW_ADMISSIBLE_USER_EVIDENCE_ONLY`.

## Authority/effect boundaries

- Voss owns assignment intake/routing/reconciliation/closure while delegated.
- Masa does not self-close MA9/MA10 merely because deliverables are submitted.
- One writer per assigned work branch/stage.
- No force push, merge, deployment, production DB mutation, credential action, paid infrastructure/service action, deletion, installation, model training, native Project mutation, or canonical-memory write without Patrick's exact authority.
- Patrick explicitly authorized safe continuity-save mechanisms; `continuity/masa` is the isolated Masa save route.
- Basic Memory Cloud remains disconnected legacy and is never a save/retrieval/archive fallback.

## Fresh-source cutoff

Latest canonical coordination observed before this save: `3424`.

Material recent events:
- 3400 corrected assignment state admission semantics.
- 3406 MA7 APPROVED; 3407 MA8 APPROVED.
- 3408 Vera V3 accepted policy-scoped workload effects and cross-facet Knowledge Resolver consistency.
- 3409 Vera V4 native budget audit APPROVED.
- 3415 MA9 root CURRENT; 3416 MA10 root CURRENT.
- 3419/3420 H7/H8 non-state proposals.
- 3421/3422 read-only GitHub audit evidence.
- 3423 H8 addendum converged on one canonical state graph + protected admission registry.
- 3424 Hephaestus source-selection research; no Masa assignment effect.

No canonical MA9/MA10 review/closure had appeared through 3424.

## Recovery procedure

1. Read this file from `continuity/masa`; verify branch/file exact readback.
2. Fresh-read canonical coordination newer than `3424` and relevant Slack before treating MA9/MA10 or any peer lane as current.
3. Resolve candidate lanes against newer targeted/lineage events before start/resume/report/count.
4. Fresh-compare `thebrazenbeard/masamune:masa` against `984cbdc781aa643443652f41f5a710f59e2d2439` before any work-branch effect.
5. Keep continuity commits on `continuity/masa`; never move `masa` merely to checkpoint continuity.
6. Treat this as WORKING_PROJECT recovery evidence only, not same-runtime consciousness or autobiographical memory.
