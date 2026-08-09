# Mune MU12 — Coordination Cutover Snapshot-Gap / Reissue Hostiles

**Assignment:** provisional `MU12 / CUTOVER_SNAPSHOT_GAP_AND_REISSUE_HOSTILES` from Voss Slack 2026-08-09 09:14 EDT  
**Peer target:** MA19 clean-break coordination cutover direction  
**Class:** read-only cutover/currentness falsification  
**Disposition:** `READY_FOR_REVIEW / CLEAN_BREAK_CONDITIONAL_ON_WRITER_FENCE_EXACT_REISSUE_AND_SOURCE_EPOCH`  
**Mutation performed:** none

## Executive verdict

A clean-break R9A0 coordination store is viable and may be simpler than forcing incompatible legacy ACK semantics into the new state reducer. It is **not** safe merely because a snapshot of old current lanes is copied into an empty new schema.

The cutover must prove three different things:

1. **snapshot completeness** — every admitted pre-cutover current lane is represented exactly once in the new protocol, with its controlling state/generation/provenance preserved;
2. **write-gap closure** — no authority-bearing old-store transition can commit outside the snapshot and disappear from the new currentness history;
3. **source-authority cutover** — after the flip, old-store state transitions are mechanically non-authoritative and cannot silently re-enter currentness through a raw/latest/multi-source path.

Fresh Vera provider readback makes an RLS-only cutover fence invalid: hosted `service_role` is `BYPASSRLS=true`, currently has direct INSERT on `public.vera_coordination_events`, the table is RLS-enabled but not FORCE RLS, and the only visible client deny policy targets `anon,authenticated`. A policy-only switch does not fence the actual broad writer.

Existing TRIAGED `ca11d679-add2-42b7-b0cc-1ec6e24eef4d` already captures the broader direct-INSERT / replenishment-confinement defect. MU12 does not create a duplicate bug.

## 1. Snapshot time is not a cutover barrier

Current old-store rows receive `record_time := clock_timestamp()` in a BEFORE INSERT trigger. That is an insert-time observation, not a commit barrier. A transaction can insert before the snapshot cut and become visible only after the snapshot transaction has already resolved current lanes.

Likewise, chronology fields such as event sequence/time must not be treated as a substitute for a writer fence or transaction visibility barrier.

Therefore a rule such as:

`copy all old rows/current lanes with record_time <= T and then switch`

is insufficient.

A correct clean break needs either:

- a mechanically verified old-writer fence/quiescence held while the final snapshot, reissue, verification and source-authority flip occur; or
- a two-phase snapshot + delta-capture/reconciliation protocol that finishes with a final writer barrier before the source flip.

## 2. Required cutover identities

Freeze one `COORDINATION_CUTOVER_EPOCH_V1` before any reissue write.

Minimum binding:

- `cutover_epoch_id`;
- exact old-source identity/schema/policy version;
- exact new-source identity/schema/policy version;
- resolver/currentness policy version;
- exact cutover snapshot/cut identity;
- old-source writer-fence state/receipt;
- exact admitted current-lane set digest;
- source-selection policy version;
- reissue canonicalizer/version;
- cutover operation identity and outcome state.

Every reissued current lane must bind the same cutover epoch and snapshot digest.

## 3. Exact-once lane reissue invariant

For each admitted old lane `L` current at the fenced snapshot:

`COUNT(new CUTOVER_REISSUE roots bound to {epoch, legacy_lane_id=L}) = 1`

For each lane terminal at that same admitted snapshot with no valid later pre-flip reactivation:

`COUNT(active new roots for L) = 0`

A reissued lane is **not a fresh assignment**. The new root/event should be a typed cutover-import/reissue construct or exact equivalent that preserves:

- legacy root/lane identity;
- legacy controlling event identity;
- current attempt/generation identity;
- current owner;
- terminal/blocking/executability facts;
- current authority binding state where still current;
- factual lineage digest;
- source/provenance locators;
- cutover epoch/snapshot digest.

It must not reset age/progress, create fictional new authority, or count as a new assignment merely because the target protocol uses a new root identity.

A stable reissue operation key such as `{cutover_epoch_id, legacy_lane_id}` plus a semantic request digest is required so ambiguous retry cannot create duplicate roots.

## 4. Snapshot-gap hostiles

### Hostile A — late terminal transition

1. Snapshot resolves lane `L` as active.
2. New protocol reissues `L` as active.
3. A valid old-store COMPLETE/CANCEL/terminal transition commits after the snapshot but before source flip.
4. Source flips without delta reconciliation.

Failure: the new store resurrects work that was terminal before cutover completed.

Expected rule: the old transition must either be blocked by the writer fence or admitted into the final delta reconciliation before the flip. Cutover fails closed otherwise.

### Hostile B — late REACTIVATE / REOPEN

1. Snapshot sees lane `L` terminal and therefore does not reissue it active.
2. A valid predecessor/generation-bound old-store REACTIVATE commits before the source flip.
3. Flip ignores the late delta.

Failure: a genuinely current attempt is lost.

Expected rule: final fenced snapshot/delta pass must include the reactivation or the cutover cannot become authoritative.

### Hostile C — in-flight pre-snapshot INSERT commits late

1. Writer transaction starts and inserts an authority-bearing event before snapshot cut `T`.
2. Snapshot transaction does not see the uncommitted row.
3. Snapshot/reissue completes.
4. Old writer commits.

Failure: neither record_time nor allocation chronology proves the snapshot was complete.

Expected rule: writer fence/quiescence must account for in-flight old writes, not merely reject new transactions by wall-clock rule.

### Hostile D — reissue retry ambiguity

1. Cutover writes new reissue root for `L`.
2. acknowledgement/readback is lost.
3. coordinator retries with a newly generated root ID.

Failure: one old current lane becomes two new roots.

Expected rule: stable cutover reissue operation identity + request digest + exact replay readback. Generated event/root identity is output, not retry identity.

### Hostile E — terminal state copied as a live assignment

A bulk exporter treats “latest visible row” or workload membership as currentness and reissues a lane that was already terminal under admitted state reduction.

Expected rule: cutover snapshot is generated only from the MU6-style authority-admitted state reducer. Raw latest/workload copies have zero reissue authority.

### Hostile F — unmirrored external authority evidence

Old canonical state says BLOCKED, but an expected coordination source contains later authority-bearing closure evidence not yet admitted/mirrored.

Expected rule: cutover snapshot is `SOURCE_INCOMPLETE / RECONCILIATION_REQUIRED`; do not mint a clean new current lane from stale canonical state and do not silently promote external prose.

### Hostile G — relation collapse during reissue

Old current/evidence topology includes cross-thread/fan-out ACK evidence or an event carrying both controlling supersession and non-consuming acknowledgement.

Expected rule: clean break may reissue only controlling current state as the new state root, but historical/evidence provenance must retain its relation class. Do not rewrite old ACK into state supersession merely to fit the new schema.

### Hostile H — source flip outcome unknown

New roots are verified but the authority-source flip write/readback outcome is ambiguous.

Expected rule: `CUTOVER_OUTCOME_UNKNOWN / RECOVERY_REQUIRED`. Neither store may be casually presumed authoritative from local success. Reconcile the source-selection record before further authority-bearing coordination writes.

### Hostile I — post-flip old-store write

After the new source is authoritatively selected, a broad old writer inserts another authority-bearing old-store event.

Expected rule: the old row remains audit evidence only and raises a bounded `POST_CUTOVER_OLD_WRITE_VIOLATION`/reconciliation signal. It must never silently become current. Prefer additionally making such writes mechanically impossible through privilege/trigger/facade confinement.

## 5. RLS-only fence is specifically falsified on current Vera

Fresh provider facts:

- `service_role` is `BYPASSRLS=true`;
- `service_role` has direct INSERT on `public.vera_coordination_events`;
- old coordination RLS is enabled but not forced;
- the current deny policy names only `anon,authenticated`;
- no narrow current assignment-issuance facade confines authority-bearing old writes.

Therefore:

`RLS_POLICY_SWITCH_ONLY != OLD_WRITER_FENCE`

Minimum cutover fence must cover the actual writer capability. Acceptable future mechanisms include privilege revocation plus a narrow closed facade, a server-side state-transition gate that direct callers cannot synthesize around, or a provider/transactional writer barrier with equivalent effect. The exact producer choice is MA19 scope.

A semantic source-authority epoch remains necessary even with a physical fence because historical old data must still be readable without being mistaken for current authority.

## 6. Recommended clean-break state machine

### Phase 0 — PREPARE

- freeze cutover policy/schema versions;
- create/qualify the new protocol without selecting it as current authority;
- mint cutover epoch;
- block cutover if old currentness is conflicted/source-incomplete.

### Phase 1 — FENCE

- establish a writer fence that actually blocks authority-bearing old-store inserts from ordinary runtime paths;
- quiesce/reconcile in-flight writers;
- read back the fence and source capability state.

### Phase 2 — FENCED SNAPSHOT

- run the trusted admitted currentness resolver over the old required source set;
- freeze current lane set + controlling lineage digests + source completeness into `snapshot_digest`.

### Phase 3 — EXACT REISSUE

- create exactly one typed cutover reissue root per admitted current lane;
- use stable reissue operation IDs/digests;
- preserve generation/owner/state/provenance;
- no terminal lane becomes active absent a valid admitted reopen/reactivate included in the final snapshot.

### Phase 4 — VERIFY

- exact cardinality and digest equality between fenced current-lane set and new reissue set;
- zero duplicate reissue roots;
- all new roots resolve under the new state reducer;
- evidence/provenance relation classes remain non-consuming;
- workload/capacity projection matches the new reducer rather than a copied list.

### Phase 5 — AUTHORITY SOURCE FLIP

- write one authority-admitted source-selection record binding the cutover epoch, old/new source identities and verified snapshot/reissue digest;
- read it back independently;
- only then may new coordination become current authority.

### Phase 6 — POST-FLIP QUARANTINE / AUDIT

- old store remains historical/audit-readable;
- authority-bearing old writes remain mechanically fenced or are explicitly non-authoritative and surfaced as violations;
- no compatibility fallback silently chooses old raw latest state.

If the process fails before Phase 5, old source remains authoritative because no flip occurred. If Phase 5 outcome is ambiguous, do not auto-assume either old or new authority; reconcile the source-selection effect first.

## 7. Clean break vs compatibility-schema migration

### Clean break

**Advantages**

- starts the new reducer with correct orthogonal relation classes instead of encoding legacy structural mistakes;
- avoids forcing 473 cross-thread ACKs, 252 fan-out parents and 261 dual-link events into a single-chain schema;
- current-state migration volume can be much smaller than full-history rewrite.

**Costs / risks**

- exact-once reissue proof is mandatory;
- cutover gap/fence/source-authority machinery is nontrivial;
- current attempt/generation/provenance must survive re-rooting;
- historical consumers need explicit old-audit/new-current source semantics.

### Compatibility-schema migration

**Advantages**

- can preserve existing event identities and history directly;
- reduces the need to represent current work as synthetic reissue roots;
- fewer semantics depend on a one-time exact-current-lane export.

**Costs / risks**

- successor schema must faithfully represent fan-out, cross-thread evidence links and dual-link events without letting evidence consume state;
- full historical migration/backfill is larger and harder to prove lossless;
- old direct writer and source-authority cutover still require a fence/flip; compatibility does not magically remove split-brain risk.

## 8. Bounded recommendation

Prefer the clean break **only if** MA19 can make the cutover machine mechanically enforce:

`ACTUAL_OLD_WRITER_FENCE -> FENCED_ADMITTED_SNAPSHOT -> EXACT_ONCE_IDEMPOTENT_REISSUE -> VERIFY -> AUTHORITY_SOURCE_FLIP_READBACK`

If exact writer fencing or source-selection authority cannot be established, a compatibility migration is safer because it avoids pretending a snapshot is a transaction barrier.

The deciding factor is not elegance of the new schema. It is whether the system can prove there is no lost or doubly-current state across the authority boundary. Databases are unusually unsympathetic to ceremonial “and then we switch over” arrows.

No schema, provider ACL, coordination row, repository producer byte, credential, deployment, installation, or canonical state was modified by MU12.
