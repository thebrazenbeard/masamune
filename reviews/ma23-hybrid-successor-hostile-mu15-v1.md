# Mune MU15 — MA23 Hybrid Successor Hostile Review

**Assignment:** provisional `MU15 / MA23_HYBRID_SUCCESSOR_HOSTILE` from Voss Slack 2026-08-09 10:15 EDT  
**Review target:** Masa `MA23 FINAL READ-ONLY / HYBRID_COORDINATION_SUCCESSOR_FINAL`, Slack 2026-08-09 10:27 EDT, plus later MA25 provenance minimum where it materially repairs MA23  
**Class:** read-only coordination-cutover falsification  
**Disposition:** `CHANGES_REQUESTED_EXACT_ONCE_OPERATION_ID_AND_ROLLBACK_REAPPLY_SEMANTICS`  
**Mutation performed by MU15:** none on Vera/BT2/provider/producer

## Executive verdict

MA23 is close and gets the hard architectural choices right: orthogonal state/evidence relations, clean-break reissue of admitted CURRENT lineages only, explicit reviewed typing for the two hosted foundation rows, terminal/reopen generations, source-authority flip, and workload CAS/idempotency as separate machinery.

I still return **CHANGES_REQUESTED** for two mechanical gaps that can produce incorrect state even if every prose-level intention is followed:

1. MA23 derives reissue `operation_id` from the semantic-state digest, so changed semantics under the same cutover epoch can create a *different* operation ID and therefore a second root instead of an idempotency conflict.
2. MA23 says legacy becomes historical after source flip but does not close rollback/reapply semantics. A naive rollback can reactivate the old store after late rows exist, defeating the source-flip isolation it just established.

MA25 materially repairs the provenance/evidence-binding gap and should be incorporated into the final MA23 machine contract rather than left as optional commentary.

## 1. What MA23 gets right

### Orthogonal future model — APPROVED

The split is correct:

- immutable `events` envelope/provenance;
- consuming `state_transitions` as the sole state lineage;
- non-consuming many-to-many/cross-thread `evidence_links`;
- state transition may atomically carry zero-many evidence links;
- `thread_key` is routing metadata, never lineage identity.

This directly repairs the current 58a state/evidence collapse without bulk-importing the legacy ACK graph.

### Terminal / generation semantics — APPROVED

MA23 correctly makes COMPLETE/CANCEL/terminal-block absorbing, requires REOPEN/REACTIVATE to consume the exact terminal head, requires fresh authority and increments generation on the same server-derived lineage. ACK/REVIEW/EVIDENCE cannot reactivate or consume state.

That is the right semantic boundary.

### Two hosted foundation rows — APPROVED WITH EXACT MAPPING RECEIPT

Fresh hosted build-ground readback independently confirms there are exactly two foundation-era rows:

- seq2 `REVIEW / READY_FOR_REVIEW`, no supersedes/ack edge;
- seq3 `REVIEW / CHANGES_REQUESTED`, `acknowledges_event_id = seq2`.

Neither row is a modern typed assignment-state transition. MA23 correctly refuses heuristic typing and requires an explicit reviewed mapping artifact: seq2 historical envelope only; seq3 non-consuming REVIEW_OF/ACK evidence. If the mapping artifact is absent, preflight returns `UNRESOLVED_EXISTING_EVENTS`.

This is much safer than inventing a migration rule such as “ACK column means state predecessor,” which would faithfully preserve the old defect in a shinier schema.

### Workload allocation direction — APPROVED BUT NEEDS THE SAME OP-ID RULE BELOW

Separate append-only assignment-batch receipt + workload snapshot/CAS is correct. Raw `max(event_sequence)` is not currentness and must not become vacancy CAS.

The batch operation identity must obey the same rule as reissue operations: stable logical operation identity independent of mutable result fields, with a semantic request digest carrying the snapshot/currentness payload.

## 2. Exact counterexample A — semantic digest in reissue operation ID breaks exact-once

MA23 says deterministic reissue operation ID derives from:

`{cutover_epoch, legacy subject/root, semantic-state digest}`.

That looks content-addressed, but it is the wrong idempotency boundary.

### Hostile sequence

1. Cutover epoch `E` is opened.
2. Fenced snapshot `S1a` resolves legacy subject `L` current as semantic state digest `A`.
3. Reissue writes successor root `R1` with operation ID `op(E,L,A)`.
4. Readback/source flip does not complete, so cutover is retried/recovered.
5. The old writer fence was lost/re-established incorrectly or the operator recomputes a different final snapshot under the same epoch. Legacy subject `L` now resolves digest `B`.
6. Retry computes `op(E,L,B)`, which is a *different operation ID*.
7. Global operation-receipt idempotency therefore does not collide with `op(E,L,A)`. A second successor root can be created for the same `{epoch,legacy subject/root}`.

Result: exact-once lineage reissue fails while every individual operation ID is “valid.”

### Required correction

Reissue operation identity must be stable on the intended logical operation, for example:

`reissue_operation_id = H(cutover_epoch_id, legacy_subject_key, legacy_lineage_root_event_id)`

The **request digest** must bind:

`S1_snapshot_digest + semantic_state_digest + legacy_head + generation + resolver/admission/source policy digests + admission_dependency_set_digest + mapping version`.

Then:

- exact retry of same request => return original result/root;
- same operation ID with changed semantic request digest => `IDEMPOTENCY_CONFLICT / CUTOVER_EPOCH_CONFLICT`;
- a changed final S1 requires a **new cutover epoch**, not a different operation ID inside the old epoch.

Also require a unique mapping key/index or equivalent machine invariant on:

`{cutover_epoch_id, legacy_subject_key, legacy_lineage_root_event_id}`

so exact-once does not depend only on caller-computed operation IDs.

This is the same distinction current bug_ops already learned the expensive way: generated/result identity is not logical retry identity.

## 3. Exact counterexample B — post-flip rollback can reactivate late legacy state

MA23 correctly says that after source selection, legacy public coordination becomes `HISTORICAL_AUDIT_AFTER_EPOCH` and later old writes trigger split-brain reconciliation rather than silent import.

It does not define what “rollback” means once that flip has succeeded.

### Hostile sequence

1. Old writer fence succeeds; final S1 is frozen.
2. Reissue verifies and `SUCCESSOR_CANONICAL` source-selection readback succeeds.
3. Legacy store is now historical.
4. A broad/legacy writer later inserts old authority-shaped row `O` or an in-flight pre-fence transaction appears late and is classified as violation/anomaly.
5. A later recovery procedure encounters a successor problem and performs a naive “rollback to old source” by pointing currentness back at legacy coordination without a new fence/snapshot/reconciliation epoch.
6. Row `O`, which was explicitly non-authoritative after the original flip, is now visible to the reactivated old resolver and can become current.

Result: rollback silently reverses the source-authority boundary and can resurrect post-cutover state.

### Required correction

Cutover rollback/reapply semantics must be phase-specific:

- **before source flip:** old source remains canonical. Partial new roots are quarantined/recoverable by exact cutover epoch; retry uses the same stable operation IDs/request digests. No “rollback” source mutation is needed.
- **source-flip outcome ambiguous:** `CUTOVER_OUTCOME_UNKNOWN / RECOVERY_REQUIRED`. Reconcile the source-selection operation/receipt before any authority-bearing writes. Never guess old or new.
- **after verified successor source flip:** legacy source cannot be made canonical again merely by reversing a selector. Recovery is forward repair of successor state or a **new authority-bound cutover/recovery epoch** with a newly fenced and explicitly adjudicated source snapshot. Late old rows remain evidence/anomalies unless separately admitted through a new successor transition.

A real post-flip reversal, if ever product-required, is a new migration with new evidence, not “undo the pointer.”

## 4. MA25 provenance minimum should be normative MA23 input

MA23's base minimum says each reissued root binds an exact immutable legacy evidence locator. That is not sufficient by itself because the current legacy coordination table is not a cryptographic archive.

Fresh canonical trigger readback confirms `public.vera_coordination_events` currently has:

- insert-time record-time trigger;
- row UPDATE blocker;
- row DELETE blocker;
- **no BEFORE TRUNCATE guard**.

So successor audit cannot safely depend on a future live query of “whatever the old table says now,” even if row IDs are stable under ordinary updates.

MA25 provides the right repair and should be folded into the machine contract:

- every reissued root binds S1/cutover/store/schema identity;
- root/head/generation/semantic state;
- resolver/admission/source-completeness versions and implementation digests;
- `admission_dependency_set_digest` over exact snapshot-bound evidence descriptors;
- content/record digests for root/head and every admission-critical evidence descriptor;
- deterministic reissue mapping receipt;
- locator-only evidence is proven non-required by deletion/recompute negative control.

### Non-state evidence rule — APPROVED AS MA25 AMENDMENT

Use the dependency test:

`removing evidence from S1 changes admitted_current_state(subject) or lowers authority/source-completeness assurance below cutover threshold`.

If true, evidence is snapshot-bound. If false, it can remain locator-only HISTORICAL_AUDIT.

This handles real cases where REVIEW/DECISION/custody/source-completeness evidence affects admission without turning that evidence into state transitions.

Required evidence from mutable sources must have captured content/normalized-fact digest and immutable receipt. Bare Slack/Drive URLs are not enough.

## 5. Source-flip split-brain proof — APPROVED AFTER rollback correction

MA23's core source-flip rule is good:

- writer fence;
- final admitted S1;
- exact reissue;
- new-store readback reproduces S1;
- one source-selection record makes R9A0 canonical;
- later old writes are anomaly/reconciliation only.

Add two machine checks:

1. source-selection operation is idempotent and exact-readback bound to `{cutover_epoch,S1_digest,reissue_set_digest,old_source_id,new_source_id}`;
2. post-flip resolver has no compatibility/fallback path that consults legacy rows for currentness. Legacy lookup is audit/reconciliation only.

## 6. Rollback/reapply preservation requirements

The successor migration/cutover acceptance suite should prove:

### Pre-flip retry/reapply

- partial reissue + lost response -> exact replay returns same root IDs;
- same epoch + changed S1/request semantics -> conflict, no second root;
- complete verified reissue repeated -> exact same mapping set/cardinality;
- one legacy CURRENT subject maps to exactly one new root;
- terminal legacy lanes map to zero current roots unless final S1 contains a valid new generation/reactivation.

### Source flip

- exact source-selection replay returns same receipt;
- changed source/S1/reissue digest under same source-selection operation ID conflicts;
- ambiguous flip outcome blocks both stores from unreviewed authority-bearing continuation until reconciled.

### Post-flip

- late old row cannot affect successor currentness;
- naive old-source reactivation is mechanically forbidden;
- explicit recovery/new-cutover epoch is required for any source reversal;
- rollback/reapply does not duplicate successor roots or reset generation/owner/provenance.

## 7. Final MU15 disposition

`CHANGES_REQUESTED` on MA23 final as written.

Required amendments before byte-shaping approval:

1. remove `semantic_state_digest` from reissue **operation identity**; put it in the request digest and bind one immutable S1 digest per cutover epoch;
2. add machine uniqueness on `{cutover_epoch,legacy subject,legacy lineage root}`;
3. fold MA25 snapshot-bound provenance/evidence dependency rules into MA23 normative contract;
4. define phase-specific rollback/reapply semantics so a verified source flip can never be undone by simply reactivating the legacy store;
5. bind source-selection idempotency/readback and post-flip no-legacy-currentness fallback.

With those amendments, I would approve the hybrid direction. The architecture is sound; the remaining failures are operation-identity and recovery mechanics, exactly the sort of tiny fields humans omit before spending a weekend explaining duplicate roots to themselves.

No Vera/BT2 schema, provider config, canonical coordination state, producer branch, credential, deployment, installation, merge or protected effect was modified by MU15.