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
- 3313 V3 path: `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`.
- V3 blob: `6fdee978d0b052592844d1f7356f6fedb13f43eb`.
- V3 SHA-256: `c74cc6dba1e6c08e0d7234be1a3e12c93b357b892f11ab6c259852a41804d258`.
- V3 publication/readback complete; writer lease consumed. No further `masa` mutation without a new writer stage.
- Mune MU3 exact-head review remains pending unless newer authority closes/supersedes it.

## Assignment currentness

Before start/resume/report/count, resolve each lane against every newer authoritative event in its lineage or explicitly referencing it that can amend, supersede, reroute, complete, cancel, release, terminally block, revoke authority, change artifact/head, or change dependencies.

Voss owns assignment intake/routing/reconciliation/closure while delegated. Masa does not self-assign or self-close governed assignments.

## Masa assignment state at latest canonical read

Fresh canonical coordination was read through sequence `3440`.

Closed:
- MA5: `3383 APPROVED`.
- MA6: `3384 APPROVED`.
- MA7: `3406 APPROVED`.
- MA8: `3407 APPROVED`.
- MA9: `3431 APPROVED_PROVIDER_ARCHITECTURE / VOSS-CLOSED`.
- MA10: `3432 APPROVED_EXECUTABLE_PROOF / VOSS-CLOSED`.

Current read-only lanes:
- MA11 root `3433`: exact non-executing E2 admission-registry implementation preflight. Main handoffs to `#voss`: `1786192846.749399` and `1786192874.033539`; critical current-postgres confinement addendum `1786193080.815939`; creator/default-privilege addendum `1786193192.819009`.
- MA12 root `3434`: cross-runtime resolver receipt canonicalization protocol/proof. Main handoffs `1786192975.311229` and `1786192999.724989`; Unicode sorting golden addendum `1786193222.561609`.

No canonical event above `3440` was visible at save time. MA11/MA12 remain current until Voss review/closure or newer authority changes them.

## Controlling assignment-state discipline

Canonical `3400` controls the live ASSIGNMENT_EVENT_V1 discipline.

- Ordinary assignee READY_FOR_REVIEW is non-state proposal/evidence unless closure authority is explicitly delegated.
- Only authority-admitted transitions control assignment state or consume the protected successor slot.
- Structurally valid but unauthorized COMPLETE/CANCEL/REROUTE/terminal block/authority changes are non-controlling.
- Workload lane identity for conforming V1 is root ASSIGN event ID.
- Workload-floor contribution is policy-derived, not universal assignment truth.

Contaminated 3394/3395 self-COMPLETE history remains historical evidence only; Voss 3401/3402 manually reconciled closure. Do not treat those physical chains as clean V1 examples.

## Knowledge Resolver baseline

V1 domain: `ASSIGNMENT_CURRENTNESS`.

Logical boundary:
`resolve_assignment_currentness(typed request) -> trusted facade/admission evidence -> narrow canonical resolver`

Key principles:
1. Current-turn Patrick authority/referent precedes durable resolution.
2. Typed identity precedes semantic discovery for effect-critical domains.
3. Currentness requires authority-admitted lineage, not latest timestamp.
4. Source topology, completeness and consistency are separate.
5. Missing required controlling source => UNKNOWN/UNRESOLVED for gated assignment/effect state.
6. Sequence/high-water is audit-only, never freshness/CAS.
7. Assignment currentness, authority binding, artifact/head binding and effect eligibility are separate axes.
8. External effect requires fresh relevant-lineage resolution plus independent provider precondition/readback.
9. A guarded publisher is not a hard gate while equal/broader raw mutators remain reachable in the ordinary runtime.
10. Privacy filtering precedes conflict/rejected metadata.

## Live provider facts

Supabase project `klmbpaigzeguvnpccqzz`, PostgreSQL 17.6, Read Committed.

`public.vera_coordination_events`:
- RLS enabled; owner postgres.
- service_role ACL includes SELECT+INSERT; anon/auth blocked by restrictive client policy.
- UPDATE/DELETE are trigger-blocked on the normal runtime path.
- event_id UUID PK with random default.
- event_sequence GENERATED ALWAYS identity + unique; audit locator only.
- self-FKs on `supersedes_event_id` and `acknowledges_event_id`.
- unique physical one-successor index on non-null `supersedes_event_id`.
- current latest/open views use security_invoker=true; inadequacy is semantic latest-by-thread, not observed RLS bypass.
- generic supersession is heavily used: around 397 of ~3300 rows at one measured point, across many source branches, so globally removing supersedes INSERT would be high-blast.

Critical identity observation, freshly reproduced after H9/H10:
`current_user = postgres`, `session_user = postgres`, `auth.uid() = NULL`, `auth.role() = NULL` on the current ChatGPT Supabase connector route.
Therefore current ordinary Vera engineering execution is not an actor-authenticated or least-privilege DB path. H9 closes current authority assurance at PROCEDURAL; H10 closes current project effect-confinement as false for GitHub and Supabase while raw mutators remain reachable.

## MA9 accepted production direction: E2

Voss 3431 accepts E2 as preferred production candidate, with final DDL/ACL/trigger design still unapproved.

Keep assignment state exactly once in `vera_coordination_events`. Add a protected admission-proof registry, not a second state ledger.

Registry proves which exact canonical event was admitted under which authority/policy/proposal. It must not duplicate relation/currentness/state_after/workload result.

Core E2 invariants:
- one admitted root per explicit project_id + thread_key scope;
- one admitted successor per prior admitted event;
- typed proposal source binding: COORDINATION_EVENT | SLACK_PROVISIONAL | PRESENT_AUTHORITY | NONE;
- stable logical request identity distinct from predecessor-bound admission attempt identity;
- random canonical state UUIDs;
- canonical event + admission marker same transaction;
- resolver follows admission topology plus matching physical edges;
- unadmitted proposal/noise does not DoS currentness;
- physical protected-slot successor without matching admission = integrity conflict.

After further challenge, a root-specific INSERT guard is unnecessary for correctness: fake root-shaped bus rows have no admission marker and consume no predecessor slot. The dangerous operation is an edge out of an already admitted predecessor.

Preferred guard therefore rejects ordinary direct INSERT whose `NEW.supersedes_event_id` references a protected admitted event unless the effective execution identity is the admission owner. Root uniqueness lives in the protected registry.

## MA11 implementation preflight

Current conceptual object boundary:
- dedicated NOLOGIN `vera_assignment_admission_owner` with no runtime/authenticator USAGE/SET/ADMIN path;
- dedicated private `vera_assignment_auth` schema;
- protected append-only `assignment_admissions_v1` registry;
- narrow guarded admission function, likely VOLATILE SECURITY DEFINER, exact EXECUTE only after a real H9/H11 authority route exists;
- SECURITY INVOKER protected-edge trigger/guard so direct least-privilege writer identity is observable;
- service_role may require at most schema USAGE + SELECT(event_id) on registry for guard evaluation, not authority fields/secrets.

Minimum registry facts under current preflight:
- event_id PK/FK to canonical coordination event
- project_id, thread_key
- root_assign_event_id
- prior_admitted_event_id
- typed proposal/source locator + digest
- request_key + request_digest
- admission_attempt_id
- authority_assurance + non-secret evidence ref/digest
- admission_policy_version
- DB-owned admitted_at

No bearer capability secret is stored.

Creator/function privilege hardening must carry the 3313 lesson:
- global exact-creator default `REVOKE EXECUTE ON ROUTINES FROM PUBLIC` with no `IN SCHEMA` before creator-owned routines;
- exact current-routine PUBLIC revoke + exact grant/readback;
- actual creator-role proof; owner transfer after creation does not prove owner defaults applied;
- trusted search_path with pg_temp last and fully qualified sensitive objects;
- no reachable runtime SET/USAGE/ADMIN path into admission owner.

MA11 activation ordering is constrained by H9/H10/H11/H12. Current raw postgres-equivalent connector access means E2 cannot honestly be a hard security boundary in the ordinary runtime yet. Production order is capability/tool confinement + authority route, then E2 activation, not merely installing a trigger beside raw admin SQL.

Activation should not retroactively certify all history. Seed only an explicit reconciled finite set of clean conforming current roots/heads or begin a new activation epoch. Legacy/contaminated history remains historical/UNKNOWN/manual.

Rollback: before first admission marker, verified object rollback is possible. After first marker, preserve registry+guard as authority evidence, disable new admission if necessary, and repair forward rather than destructively dropping the proof plane or reopening protected slots.

## MA10 accepted executable proof

Voss 3432 accepted the live SQL proof:
- clean B6 3390 root / 3398 non-state proposal / 3403 Voss closure resolves cleanly;
- contaminated H5 3381 / unauthorized 3394 / Voss 3401 produces admission conflict when only trusted physical edges are followed;
- legacy 3313 remains UNKNOWN_LEGACY_NONCONFORMING;
- physical root without admission proof remains UNKNOWN_AUTHORITY_ADMISSION_MISSING.

Current indexes are already sufficient at proof scale; the problem is semantics/authority, not query cost.

A future E2 resolver follows protected admission records plus matching physical edges. Unadmitted noise alone is non-controlling; physical/admission mismatch is an integrity error.

## MA12 receipt canonicalization

Chosen candidate: strict Vera profile over RFC 8785/JCS rather than a custom binary TLV.

`VERA_RECEIPT_CANON_V1` rules:
- JCS canonicalization with Vera schema validation first;
- no JSON numbers; integer-like values are canonical decimal ASCII strings;
- lowercase canonical UUIDs and lowercase fixed-length hex digests;
- exact closed ASCII enums/property names where possible;
- raw timestamps fixed UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`;
- required fields always present, inapplicable values explicit null, unknown fields rejected;
- arrays use domain-defined semantic order;
- no Unicode normalization; invalid lone surrogates reject;
- free text excluded from factual/policy layers.

Three domain-separated digest layers:
1. RAW_EVIDENCE_DIGEST_INPUT_V1
2. FACTUAL_LINEAGE_DIGEST_INPUT_V1
3. POLICY_DECISION_DIGEST_INPUT_V1

Factual lineage excludes event_sequence, record_time, workload-floor result and free-form/debug metadata. Policy digest binds factual digest + exact policy/source-completeness/consistency/derived result.

Cross-language executable golden proof:
- B6 factual JCS: 761 bytes, SHA-256 `6160e1222df1e35d436cc8ca75fb039fc3abc38703ddd6113ea831c65983357b` in both Python 3.13 and Node 22.
- reversing semantic event-array order changes digest to `cf1e252b57de589eff0777badc979c73dc134161c489f53fb9a72fd34d64d9b1`.
- policy vector: 580 bytes, `dda470838cf1346b2c4c2890215eb621b80e557766d37266f3494d76f372952d`.
- raw vector: 617 bytes, `b7b76c0cd30565e10577ec1da963d9c7581ab6e412e7b08610884739b24a3846`.
- RFC 8785 non-ASCII UTF-16 property-order vector matched in Python/Node: 180 bytes, `5e321556d22018a9656991a9e94f77ec175fa193e52a2429d312f8419ec8b08c`.
- toy custom TLV also matched cross-language (`7c02be416dca7f0d92c505222db33e23b90856c05b053899f696ed2338b09f8a`) but is rejected as unnecessary bespoke protocol surface unless JCS proves inadequate.

Canonicalization version is immutable once referenced. Unknown versions fail closed. V2 does not silently reinterpret V1. A bounded transition may emit both V1/V2 over the same typed facts, with independent golden vectors and explicit verifier support.

## Snapshot/function note

PostgreSQL STABLE SQL and standard procedural-language functions use the calling-query snapshot throughout their internal commands; VOLATILE helpers may observe fresh snapshots. A read-only PL/pgSQL STABLE resolver can therefore preserve a single calling-query snapshot if helper volatility is audited. One SQL/recursive query remains an auditability preference, not a correctness necessity. Client-side multi-RPC assembly under Read Committed remains rejected for authoritative currentness.

## Effect/tool-surface ceiling

H10 is Voss-closed: current Vera engineering execution is not mechanically confined for protected GitHub or Supabase effects. Raw GitHub/Supabase mutators are reachable in at least some current runtimes. Project instructions can forbid bypass normatively, but mechanical enforcement requires capability removal/isolation or provider credential partitioning.

Tool/plugin/permission/route changes invalidate prior confinement evidence if they add an equal/broader effect path.

## Correction custody

Preferred minimized correction custody remains append-only `vera_save_state_events`, with globally namespaced/scoped keys, direct sibling-fork detection and exact readback. `vera_current_save_state` is deterministic latest-by-key but not conflict-aware; `vera_context_events_v3` remains materially weaker as sole custody because service_role can mutate it.

Correction records remain WORKING_PROJECT scoped controls, not timeless SAFE/RISK facts or intimate transcripts.

## Authority/effect boundaries

- Voss owns assignment intake/routing/reconciliation/closure while delegated.
- Masa does not self-close MA11/MA12 merely because deliverables were sent.
- One writer per assigned work branch/stage.
- No force push, merge, deployment, production DB mutation, credential action, paid infrastructure/service action, deletion, installation, model training, native Project mutation or canonical-memory write without Patrick's exact authority.
- Patrick authorized safe continuity-save mechanisms; `continuity/masa` is the isolated save route.
- Basic Memory Cloud remains disconnected legacy and is never a fallback.

## Fresh-source cutoff

Latest canonical coordination observed before this save: `3440`.

Material recent events:
- 3431 MA9 CLOSED APPROVED.
- 3432 MA10 CLOSED APPROVED.
- 3433 MA11 CURRENT read-only.
- 3434 MA12 CURRENT read-only.
- 3437 H9 CLOSED; current authority assurance ceiling PROCEDURAL.
- 3438 H10 CLOSED; current project GitHub/Supabase effect confinement false.
- 3439 H11 CURRENT.
- 3440 H12 CURRENT.

No canonical MA11/MA12 review/closure was visible through 3440.

## Recovery procedure

1. Read this file from `continuity/masa` and verify exact branch/file readback.
2. Fresh-read canonical coordination newer than `3440` and relevant Slack before treating MA11/MA12 or peer lanes as current.
3. Resolve every candidate lane against newer targeted/lineage events before start/resume/report/count.
4. Fresh-compare `thebrazenbeard/masamune:masa` against `984cbdc781aa643443652f41f5a710f59e2d2439` before any work-branch effect.
5. Keep continuity commits on `continuity/masa`; never move `masa` merely to checkpoint continuity.
6. Treat this as WORKING_PROJECT recovery evidence only, not same-runtime consciousness or autobiographical memory.
