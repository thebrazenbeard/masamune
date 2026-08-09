# Mune MU6 — Correction / Currentness Resolver Final V2

**Assignment:** `VOSS-20260808-MU6` / canonical root `3464`, amendment `3665`  
**Class:** read-only resolver proof  
**Disposition:** `FINAL_READY_FOR_REVIEW`  
**Provider/schema mutation:** none

## Final verdict

`PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT_AND_PRIVACY_ORDER_CORRECTION`

The append-only evidence substrate can support deterministic currentness only if six concerns remain mechanically distinct:

1. raw source observation and provenance;
2. source completeness/reconciliation;
3. trusted exact-scope graph construction;
4. admission and typed state semantics;
5. current-state reduction;
6. caller privacy projection.

A seventh concern is deliberately outside the resolver: **mutation admission / assignment issuance concurrency**. Correctly resolving a vacancy does not itself authorize or serialize the write that fills it.

Raw “latest” chronology views are observation aids only. They are not assignment/currentness reducers.

## 1. Full governed graph precedes privacy projection

The original V1 proof filtered caller-visible rows before graph construction. Read-only synthetic hostiles reproduced the defect:

- visible root `r` + hidden successor `h` -> full graph leaf `h`, visible-only leaf `r`;
- visible node + hidden sibling successor -> full graph fork, visible-only graph falsely clean;
- hidden controlling leaf -> visible-only subset falsely promotes an older record.

Correct invariant:

`TRUSTED_FULL_GOVERNED_GRAPH -> ADMISSION/STATE_REDUCTION -> CALLER_VISIBILITY_PROJECTION -> PRIVACY_MINIMIZED_RESULT`

Privacy may suppress identifiers/details or force a generic unavailable/unresolved result. It may never remove governing nodes in a way that changes which node controls state.

Existing bug: `1be2c5ab-2eee-4916-ad07-8d5a7ca84455`.

## 2. Raw chronology is not assignment state

Fresh live Vera readback proves `public.vera_coordination_latest` is a raw sequence projection:

`DISTINCT ON (thread_key) ... ORDER BY thread_key, event_sequence DESC`

Concrete witness:

- sequence `3634` is the canonical MA15 closure;
- sequence `3636` is later reconciliation evidence with `state_effect=NONE` and explicitly preserves 3634 as canonical;
- `vera_coordination_latest` nevertheless returns 3636 because it is newer.

Therefore no START / RESUME / workload / authority decision may consume `vera_coordination_latest` as current assignment state.

Existing bug: `5c4ca43f-d253-4a9f-90c3-dd6d4361ef9e`.

Required output split:

- `LATEST_OBSERVATION` / `RAW_THREAD_HEAD`: newest provider chronology/head evidence;
- `CURRENT_ASSIGNMENT_STATE`: admitted typed reduction over the trusted scoped lineage.

A later REVIEW / ACK / evidence / reconciliation / workload-copy record may advance observation chronology without altering controlling assignment state.

## 3. R9A0 candidate views retain the same chronology/state hazard

Exact database candidate `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`, migration `20260806224900_r9a0_coordination_integrity_repairs.sql`, was independently inspected.

Its `validate_event_chain()` treats either `supersedes_event_id` or `acknowledges_event_id` as consuming a thread head. `thread_heads` removes the predecessor; `latest_thread_state` then selects the highest remaining sequence.

That is a valid raw causal-head projection, but it does not by itself distinguish admitted state transitions from non-state acknowledgements/review evidence. A non-state successor can become the sole “latest_thread_state” head while an earlier admitted transition remains controlling.

Therefore R9A0 must not merely substitute `r9a0_coordination.latest_thread_state` for the legacy raw-latest view. Protected currentness needs a separate mechanically closed admission + state reducer.

No duplicate ticket is needed; this is the same chronology-versus-state class tracked by `5c4ca43f-d253-4a9f-90c3-dd6d4361ef9e`.

## 4. Terminal disposition is absorbing unless explicitly reactivated

Cross-system BT2 recurrences independently demonstrate the failure mode: later workload/addendum copying repeatedly listed assignments as current after their terminal state, despite no predecessor-bound reactivation.

MU6 therefore requires terminal absorption as a reducer invariant:

- `COMPLETE`, `CANCEL`, and admitted terminal-block dispositions remain terminal under later non-state ACK/review/workload/evidence rows;
- a workload snapshot has zero transition authority and cannot resurrect a lane;
- a later status label alone cannot resurrect a lane;
- reactivation/reopen must be an **explicit admitted state transition bound to the correct terminal predecessor/generation** and must create the new current attempt under the closed transition policy.

Hostile pair:

1. `ASSIGN -> COMPLETE -> later workload-copy/ACK` => still terminal / zero executable capacity.
2. `ASSIGN -> COMPLETE -> admitted predecessor-bound REACTIVATE` => new current attempt, subject to the normal currentness/authority/effect gates.

This reinforces `RAW_CHRONOLOGY != ASSIGNMENT_STATE`; it does not create a new resolver subsystem.

## 5. Source completeness is independent from admission authority

Live canonical evidence for `vera-r9a0/assignments/voss/anticipatory-pragmatics-design-freeze-v1` remains at sequence `3315 / BLOCKED`. Separately observed later coordination evidence records an authority-bearing closure/design-freeze decision consumed by downstream work but never canonically mirrored.

That does **not** let Slack prose mechanically close canonical state.

Correct behavior:

- `3315` remains the last admitted canonical state;
- because an expected source shows later authority-bearing but unmirrored evidence, source completeness becomes `SOURCE_INCOMPLETE / RECONCILIATION_REQUIRED`;
- the resolver must not report `3315 BLOCKED` as a clean complete-currentness answer;
- the external evidence must not silently become canonical state.

Existing bug: `3d4a7295-499c-4c30-814a-a5bb5e45f4cc`.

## 6. Internal consistency is not admission custody

CRITICAL `a72ef1f1-f750-4b85-bb93-9edf33d5338a` supplies an important admission hostile.

Current portable-bootstrap `DURABLY_BOUND` projections contain internally consistent request/binding/readback rows. But the same hosted `service_role` had broad direct base-table DML alongside the intended narrow RPC path. Fresh reviewed-source searches did not find independent immutable custody evidence for sampled request/binding/confirmation identities proving they traversed the RPC admission state machine.

Therefore:

- internal digest/foreign-key/view consistency does **not** establish admitted write-route custody;
- missing custody proof is not evidence of forgery;
- such evidence is `UNRESOLVED_ADMISSION_CUSTODY / REISSUE_REQUIRED` (or the exact governed equivalent) until independent immutable provenance proves admitted RPC custody or a fresh protected chain is issued;
- the resolver must not silently classify it ADMITTED/current;
- it also must not classify it REJECTED/forged without positive contradiction or forgery evidence.

This is the same general rule as `missing admission proof != rejection`; portable bootstrap is not a special exception.

## 7. Currentness resolution and assignment issuance are separate transactions

TRIAGED MEDIUM `ca11d679-add2-42b7-b0cc-1ec6e24eef4d` proves the present Vera coordination substrate has no workload-version CAS, vacancy claim, or single-writer replenishment transaction.

Fresh read-only catalog verification additionally shows:

- `service_role` currently has direct `INSERT` on `public.vera_coordination_events`;
- RLS is enabled but not forced;
- the only table policy is a deny policy for `anon,authenticated`;
- hosted `service_role` is `BYPASSRLS`;
- no narrow current public append/replenishment function was found; the only public function referencing the table in the reviewed catalog was the mutation-block helper.

So even a future correct replenishment RPC would not establish confinement if authority-bearing ASSIGN/REROUTE/REACTIVATE records remained directly insertable around it.

Required mutation invariant:

`RESOLVE_EXACT_WORKLOAD_VERSION -> ACQUIRE_REPLENISHMENT_LOCK/CAS -> RE-RESOLVE_IN_TRANSACTION -> ATOMIC_ROOT/ID_ALLOCATION -> APPEND GOVERNED ASSIGNMENT TRANSITIONS -> COMMIT`

A stale competing batch fails closed. A later workload snapshot cannot retroactively legalize duplicate roots. Cross-thread append/thread locks are insufficient because two coordinators may independently fill the same logical vacancy with distinct valid roots.

This is **not** part of the read resolver. The resolver reports factual currentness/version; the issuance path consumes that version under a separate writer transaction and append-path-confinement policy.

## 8. Final resolver pipeline

### A. Raw source adapters

Normalize immutable observations with source/provenance identity. Chronology alone has no state authority.

### B. Source completeness

Establish whether all policy-required sources/custody evidence for the requested decision are represented and reconciled. Missing expected authority-bearing evidence or missing required admission custody fails closed.

### C. Trusted exact-scope graph

Construct the complete authority-eligible scope before privacy filtering. Validate roots, predecessor links, forks, cycles, disconnected nodes, cross-scope edges, duplicate/colliding identity, and generation boundaries.

### D. Admission / semantic adapter

Only mechanically admitted typed state transitions may mutate assignment state. Legacy unstructured corrections remain `SEMANTICS_UNKNOWN_LEGACY_UNSTRUCTURED` unless a separately reviewed deterministic adapter exists. Internally coherent but custody-unproven records remain unresolved, not admitted by appearance.

### E. State reducer

Reduce the admitted lineage under the closed transition registry. Terminal states absorb later non-state evidence; only explicit valid predecessor-bound reactivation/reopen creates a new attempt.

### F. Caller privacy projection

After internal adjudication, minimize disclosure. Hidden controlling evidence may yield a generic unavailable/unresolved/controlled answer but never re-promotes an older visible node.

### G. Separate mutation admission

Any action that creates or changes assignments must re-use the resolver result/version inside an authorized serialized/CAS transaction. Read correctness alone confers no write authority and no concurrency safety.

## 9. Minimum acceptance invariants

1. `LATEST_OBSERVATION != CURRENT_ASSIGNMENT_STATE` by contract and naming.
2. Event sequence/head chronology has no standalone state authority.
3. Only admitted typed state transitions may alter assignment state.
4. Non-state ACK/review/evidence/workload rows may advance chronology without changing state.
5. Terminal disposition is absorbing absent explicit valid predecessor-bound reactivation/reopen.
6. Workload snapshots have zero transition authority.
7. Expected-source incompleteness is explicit and fail-closed.
8. Unmirrored authority-bearing external evidence does not silently become canonical state and does not permit stale canonical state to be reported as source-complete.
9. Trusted full governed exact-scope graph is resolved before privacy projection.
10. Hidden successors/siblings cannot make an older visible record current.
11. Fork/cycle/disconnected/cross-scope conflicts never resolve by timestamp/UUID.
12. Legacy unstructured correction semantics are never NLP-inferred into policy control.
13. Internally consistent evidence with unavailable required admission custody is unresolved/reissue-required, not silently admitted and not labeled forged without proof.
14. `public.vera_coordination_latest` and candidate `r9a0_coordination.latest_thread_state` remain raw observation/head views unless explicitly rebound behind an admitted reducer.
15. Workload, START, RESUME and USE_AUTHORITY consume the admitted currentness result, not raw latest chronology.
16. Replenishment/assignment issuance consumes an exact currentness/workload version under CAS/lock + in-transaction re-resolution; stale competing batches fail closed.
17. Append-path confinement is required for authority-bearing assignment writes; a correct CAS facade is insufficient if the same runtime principal can bypass it with direct state-changing INSERTs.

## Final disposition

`FINAL_READY_FOR_REVIEW`

The MU6 proof is now one integrated contract: full governed graph first, source/custody completeness explicit, admitted typed reduction separate from chronology, terminal states absorbing, privacy last, and mutation admission/concurrency outside the resolver but mechanically bound to its exact versioned output.

Existing related defects are already reported and triaged; no duplicate bug tickets are created by this final.

No schema, production row, canonical coordination row, provider configuration, protected producer branch, credential, installation, deployment or canonical memory was modified by MU6.
