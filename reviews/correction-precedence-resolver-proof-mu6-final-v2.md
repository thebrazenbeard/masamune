# Mune MU6 — Correction / Currentness Resolver Final V2

**Assignment:** `VOSS-20260808-MU6` / canonical root `3464`, amendment `3665`  
**Class:** read-only resolver proof  
**Disposition:** `FINAL_READY_FOR_REVIEW`  
**Provider/schema mutation:** none

## Final verdict

`PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT_AND_PRIVACY_ORDER_CORRECTION`

The existing append-only evidence substrate is sufficient to support a deterministic currentness resolver **only if four concerns remain separate**:

1. trusted governed graph/currentness;
2. semantic/admission interpretation;
3. source completeness/reconciliation;
4. caller privacy projection.

Raw “latest” chronology views are observation aids only. They are not assignment/currentness reducers.

## 1. Controlling correction to the original proof

The original V1 privacy ordering was wrong because it filtered caller-visible rows before graph construction. Read-only synthetic hostiles reproduced the failure:

- visible root `r` + hidden successor `h` -> full graph leaf `h`, visible-only leaf `r`;
- visible node plus hidden sibling successor -> full graph fork, visible-only graph falsely clean;
- hidden controlling leaf -> visible-only subset falsely promotes an older record.

Correct invariant:

`TRUSTED_FULL_GOVERNED_GRAPH -> CURRENTNESS/SEMANTICS -> CALLER_VISIBILITY_PROJECTION -> PRIVACY_MINIMIZED_RESULT`

Privacy may suppress disclosure or force a generic unavailable/unresolved result. It may never delete governing nodes in a way that changes which node is current.

Existing bug: `1be2c5ab-2eee-4916-ad07-8d5a7ca84455`.

## 2. Raw chronology is not current assignment state

Fresh live Vera readback proves `public.vera_coordination_latest` is exactly:

`DISTINCT ON (thread_key) ... ORDER BY thread_key, event_sequence DESC`

That makes it a chronology projection, not an authority-admitted state reducer.

Concrete live witness:

- sequence `3634` is the canonical MA15 closure;
- sequence `3636` is a later reconciliation record with `state_effect=NONE` and explicitly preserves 3634 as canonical;
- `public.vera_coordination_latest` nevertheless returns `3636` for that thread because it has the larger sequence.

Therefore no consumer may derive START / RESUME / workload / authority state merely from the row returned by `vera_coordination_latest`.

Existing bug: `5c4ca43f-d253-4a9f-90c3-dd6d4361ef9e` (`vera_coordination_latest exposes raw chronology as state-sounding latest projection`). No duplicate report is needed.

### Required output split

Use distinct concepts/namespaces:

- `LATEST_OBSERVATION` / `RAW_THREAD_HEAD`: newest provider chronology/head evidence;
- `CURRENT_ASSIGNMENT_STATE`: result of admitted typed state reduction over the trusted scoped lineage.

A later REVIEW / DECISION / evidence / reconciliation row with no admitted state effect may advance chronology without replacing controlling assignment state.

## 3. R9A0 candidate views have the same state/chronology conflation

Exact database candidate `58a6ae4d4272165bd5b988bdd7a8bb0e72417302` migration `20260806224900_r9a0_coordination_integrity_repairs.sql` was independently inspected.

Its `validate_event_chain()` treats either `supersedes_event_id` **or** `acknowledges_event_id` as consuming the current thread head. `thread_heads` therefore removes any event that has a later superseding or acknowledging successor. `latest_thread_state` then selects the highest-sequence remaining head, and `open_threads` filters that result by status.

That is useful as a raw causal-head projection, but it does not distinguish typed state transitions from non-state acknowledgements/review evidence. A non-state successor can therefore become the sole “latest_thread_state” head even when an earlier admitted transition remains the controlling assignment state.

So a future R9A0 consumer cannot merely replace legacy `public.vera_coordination_latest` with `r9a0_coordination.latest_thread_state` and claim currentness is fixed.

The candidate view should be classified/named as **raw observation/head projection** unless a separate mechanically closed admission + state reducer is placed in front of protected currentness consumers.

No new bug ticket is needed because this is the same chronology-versus-state defect class already tracked by `5c4ca43f-d253-4a9f-90c3-dd6d4361ef9e`.

## 4. Source completeness is independent from admission authority

A second currentness failure class is missing canonical mirroring, not graph privacy.

Live canonical evidence for `vera-r9a0/assignments/voss/anticipatory-pragmatics-design-freeze-v1` remains at sequence `3315 / BLOCKED`. Separately observed later coordination evidence records an authority-bearing closure/design-freeze decision that was consumed by downstream work but was not mirrored into the canonical thread.

That does **not** mean Slack prose mechanically closes canonical state.

Correct fail-closed behavior is:

- canonical `3315` remains the **last admitted canonical state**;
- if Slack is an expected coordination source and a later authority-bearing transition is observed but not canonically admitted/mirrored, source completeness becomes `SOURCE_INCOMPLETE` / `RECONCILIATION_REQUIRED`;
- the resolver must not report the stale `BLOCKED` row as a clean complete-currentness answer;
- the resolver also must not silently promote the Slack message into canonical state.

Existing bug: `3d4a7295-499c-4c30-814a-a5bb5e45f4cc` (`AP design-freeze canonical mirror remains BLOCKED after later authority-bearing closure evidence`). No duplicate report is needed.

## 5. Final resolver layers

### A. Raw source adapters

Produce immutable normalized observations with source/provenance identity. Do not infer state from chronology ordering.

### B. Source completeness

Determine whether all policy-required sources for the requested currentness decision are represented and reconciled. Missing expected authority-bearing evidence yields `SOURCE_INCOMPLETE` / `RECONCILIATION_REQUIRED`, not a false clean result.

### C. Trusted scoped graph

Construct the complete authority-eligible exact scope before caller privacy filtering. Validate roots, leaves, predecessor links, forks, cycles, disconnected nodes, cross-scope edges and identity collisions.

### D. Admission / semantic adapter

Only mechanically admitted typed state events may change assignment state. Historical/legacy unstructured corrections remain `SEMANTICS_UNKNOWN_LEGACY_UNSTRUCTURED` unless a separately reviewed deterministic adapter exists.

### E. State reducer

Reduce one admitted connected lane according to the closed transition/state policy. Non-state evidence may be retained without becoming controlling assignment state.

### F. Caller privacy projection

After internal adjudication, minimize what the caller may learn. Hidden controlling evidence may force a generic unavailable/unresolved result but never re-promotes an older visible node.

## 6. Minimum acceptance invariants

1. `LATEST_OBSERVATION != CURRENT_ASSIGNMENT_STATE` by contract and naming.
2. Event sequence/head chronology has no standalone state authority.
3. Only admitted typed state transitions may alter assignment state.
4. Non-state ACK/review/evidence may advance raw chronology without changing assignment state.
5. Expected-source incompleteness is explicit and fail-closed.
6. An unmirrored external authority-bearing transition does not silently become canonical state and does not permit stale canonical state to be reported as complete/current.
7. Trusted full governed graph is resolved before caller privacy projection.
8. Hidden successors/siblings cannot make an older visible record current.
9. Fork/cycle/disconnected/cross-scope conflicts never resolve by timestamp/UUID.
10. Legacy unstructured correction semantics are never NLP-inferred into policy control.
11. `public.vera_coordination_latest` and candidate `r9a0_coordination.latest_thread_state` remain raw observation/head views unless explicitly renamed/rebound behind an admitted state reducer.
12. Workload, START, RESUME and USE_AUTHORITY decisions consume the admitted currentness result, not raw latest chronology.

## Final disposition

`FINAL_READY_FOR_REVIEW`

MU6's topology/currentness approach remains viable after the privacy correction, but the production architecture must explicitly separate raw chronology, source completeness, admitted state reduction, and privacy projection. The two current chronology/mirror bug classes above are already reported; no duplicate bug tickets were created.

No schema, production row, coordination row, provider configuration, protected repository branch, credential, installation, deployment or canonical memory was modified by MU6.
