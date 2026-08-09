# Mune MU6 — Correction / Currentness Resolver Integrated Final V3

**Assignment:** `VOSS-20260808-MU6` / canonical root `3464`, amendment `3665`  
**Class:** read-only resolver/currentness proof  
**Disposition:** `FINAL_READY_FOR_REVIEW`  
**Provider/schema mutation:** none

## Final verdict

`PROOF_ACCEPTED_WITH_CLOSED_RELATION_CLASSES_AND_SEPARATE_MUTATION_ADMISSION`

A deterministic currentness system is viable only if the following concerns remain mechanically distinct:

1. raw source observation/provenance;
2. source completeness/reconciliation;
3. trusted exact-scope graph construction;
4. admission and typed relation semantics;
5. assignment-state reduction;
6. caller privacy projection;
7. mutation admission, retry safety, and replenishment concurrency.

The first six produce factual currentness. The seventh consumes an exact version of that result under a separately governed writer transaction. A correct resolver is not a write lock, and a correct writer transaction is not a resolver.

## 1. Full governed graph before privacy projection

The original privacy-first proof was wrong. Read-only synthetic hostiles reproduced all three false-currentness cases:

- visible root `r` + hidden controlling successor `h` -> visible-only graph falsely promotes `r`;
- visible node + hidden sibling -> visible-only graph falsely removes a real fork;
- hidden controller -> visible-only subset falsely reports an older visible state as current.

Required order:

`TRUSTED_FULL_GOVERNED_EXACT_SCOPE_GRAPH -> ADMISSION/STATE_REDUCTION -> CALLER_VISIBILITY_PROJECTION -> PRIVACY_MINIMIZED_RESULT`

Privacy may suppress identifiers/details or force a generic unavailable/unresolved answer. It may never delete a governing node before currentness is resolved.

Existing bug: `1be2c5ab-2eee-4916-ad07-8d5a7ca84455`.

## 2. Relation classes are mechanically different

Fresh inspection of exact R9A0 database candidate `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`, migration `20260806224900_r9a0_coordination_integrity_repairs.sql` blob `1c426b34c624f687e543e0a79ea8f28b93be4418`, independently confirms the current candidate treats `supersedes_event_id` and `acknowledges_event_id` as one state-consuming predecessor class:

- either edge removes the referenced row from `thread_heads`;
- any non-initial row must point to exactly one current head;
- `v_link_count <> 1` rejects a row carrying both relation types;
- cross-thread references are rejected;
- `acknowledges_event_id` is UNIQUE, allowing only one acknowledgement child.

That model is incompatible with both currentness semantics and observed Vera evidence topology.

Fresh live Vera readback gives:

- acknowledgement edges: `1368`;
- same-thread acknowledgement edges: `895`;
- cross-thread acknowledgement edges: `473`;
- acknowledgement parents with more than one child: `252`;
- maximum observed acknowledgement fan-out: `18`;
- events carrying both supersedes and acknowledges relations: `261`;
- dual-link same-target events: `50`;
- dual-link distinct-target events: `211`;
- dual-link events with at least one cross-thread relation: `86`.

Therefore the final architecture requires at least two relation classes, and those relation classes must be able to coexist on one operation/event when the closed policy permits it.

### A. Controlling admitted state-transition lineage

Examples: admitted ASSIGN-version successor relations such as AMEND/SUPERSEDE/REROUTE/terminal transitions/valid REACTIVATE according to the closed transition registry.

Properties:

- exact assignment/generation scope;
- mechanically admitted relation vocabulary;
- predecessor constraints and transition legality;
- may change controlling assignment state;
- participates in state reducer/current controller selection;
- invalid forks/cycles/cross-scope collisions fail closed.

### B. Non-consuming evidence/reference lineage

Examples: ACK, REVIEW, evidence citation, reconciliation locator, cross-thread dependency/provenance reference.

Properties:

- may fan out;
- may cross threads when policy permits;
- may coexist with one controlling state-transition relation on the same event/operation;
- may target the same or a different event than the controlling relation when the relation subtype permits it;
- may advance raw observation chronology;
- may affect source-completeness/reconciliation evidence;
- **does not consume or replace controlling assignment state merely by existing**;
- must not be constrained by a single-state-head UNIQUE rule unless the specific relation subtype explicitly requires it.

The relation type determines whether an edge participates in state reduction. A generic `predecessor` abstraction that lets ACK behave like SUPERSEDE is unsafe. Likewise, a schema that forces one relation slot total is lossy because state transition and evidence linkage are orthogonal facts.

Existing bugs already track the concrete defects:

- MEDIUM `95e63d67-c439-46cf-ab23-ad4b2c544eef`: ACK can consume active state and make open work disappear;
- HIGH `2ee0bc39-a9cb-469b-b551-c2d67cd549b5`: strict single-chain/cross-thread-forbidden acknowledgement model cannot represent observed Vera fan-out/cross-thread/dual-link evidence lineage.

No duplicate ticket is needed.

## 3. Raw chronology is not assignment state

`public.vera_coordination_latest` is a sequence projection, not a reducer. The known 3634/3636 witness remains decisive: 3636 is later non-state reconciliation evidence while 3634 remains the canonical controlling closure, yet raw latest returns 3636.

The exact R9A0 `thread_heads/latest_thread_state/open_threads` design repeats the same semantic collapse and additionally lets ACK edges consume state.

Required output split:

- `LATEST_OBSERVATION` / `RAW_EVIDENCE_HEADS`;
- `CURRENT_ASSIGNMENT_STATE` / `CURRENT_CONTROLLING_EVENT`;
- optional `EVIDENCE_REFERENCES` / reconciliation metadata.

START, RESUME, workload contribution, USE_AUTHORITY, and protected-effect eligibility consume admitted assignment state, never raw chronology or generic evidence heads.

Existing bug: `5c4ca43f-d253-4a9f-90c3-dd6d4361ef9e`.

## 4. Terminal disposition is absorbing absent explicit valid reactivation

Later ACK/review/workload/evidence rows have zero resurrection authority.

Required hostile pair:

1. `ASSIGN -> COMPLETE/CANCEL/TERMINAL_BLOCK -> later ACK/review/workload-copy` => remains terminal and non-executable.
2. `ASSIGN -> terminal -> admitted predecessor/generation-bound REACTIVATE or REOPEN` => creates a new current attempt subject to the closed transition policy and normal authority/effect gates.

A later status label or workload snapshot cannot retroactively legalize resurrection.

## 5. Source completeness is independent from canonical admission

The AP design-freeze witness remains the required multi-source hostile:

- canonical last admitted state remains `3315 / BLOCKED`;
- later externally observed authority-bearing evidence indicates closure/design-freeze but was not canonically admitted/mirrored.

Correct result is not “Slack wins” and not “3315 is clean current truth.” It is:

- last admitted state remains 3315;
- source completeness becomes `SOURCE_INCOMPLETE / RECONCILIATION_REQUIRED`;
- external evidence is a bounded reconciliation locator, not a silent state transition.

Existing bug: `3d4a7295-499c-4c30-814a-a5bb5e45f4cc`.

## 6. Internal consistency is not admission custody

CRITICAL `a72ef1f1-f750-4b85-bb93-9edf33d5338a` proves why relational consistency cannot substitute for write-route custody.

Portable-bootstrap request/binding/readback rows can be internally coherent while the same `service_role` historically had direct base-table DML beside the intended narrow RPC state machine. Where immutable route provenance cannot prove the narrow admission path was used:

`UNRESOLVED_ADMISSION_CUSTODY / REISSUE_REQUIRED`

is the correct bounded lifecycle.

Do not silently classify such evidence ADMITTED/current. Also do not call it forged/rejected absent positive contradiction or forgery evidence.

General invariant:

`MISSING_REQUIRED_ADMISSION_PROOF != REJECTION_PROOF`.

## 7. Mutation admission is separate from read currentness

TRIAGED MEDIUM `ca11d679-add2-42b7-b0cc-1ec6e24eef4d` independently establishes that current Vera replenishment lacks an exact workload/currentness CAS and single-writer vacancy transaction.

Fresh live catalog evidence also shows `service_role` has direct INSERT on `public.vera_coordination_events`, is BYPASSRLS, and no narrow assignment-issuance RPC currently confines authority-bearing transitions.

Therefore a future replenishment path requires both transaction correctness and path confinement:

`RESOLVE_EXACT_WORKLOAD/CURRENTNESS_VERSION -> ACQUIRE REPLENISHMENT CAS/LOCK -> RE-RESOLVE IN TRANSACTION -> ATOMIC ROOT/ID ALLOCATION -> APPEND GOVERNED STATE TRANSITIONS -> COMMIT`

A stale competing batch fails closed. Cross-thread event locks do not solve a logical vacancy race between distinct assignment roots.

A correct CAS facade is insufficient if the same runtime principal can bypass it with direct authority-bearing INSERTs.

## 8. Retry safety is a separate mutation axis

TRIAGED MEDIUM `0a40a54c-5416-40b1-a611-35b936a96f6d` independently establishes that current Vera coordination append lacks operation identity/request-digest replay semantics.

This is distinct from concurrent replenishment:

- **CAS/concurrency failure:** two writers intentionally submit different operations from the same stale vacancy snapshot;
- **idempotency/retry failure:** one logical writer retries the same intended operation after an ambiguous outcome and creates a second valid-looking event/root.

The future governed append path therefore needs both.

Minimum retry-safe contract:

- caller supplies stable `operation_id` before dispatch;
- request digest covers all identity/authority/state-bearing semantic inputs;
- operation identity is unique within the relevant namespace;
- exact replay returns the original committed receipt/event identity;
- same operation ID with changed semantic digest fails closed as conflict;
- after ambiguous outcome, independently read operation state before any retry;
- generated event UUID/sequence are results, not idempotency keys.

R9A0's exact `append_coordination_event` already demonstrates the basic operation-id/request-digest replay pattern; that useful pattern must not be conflated with its defective relation/currentness semantics.

## 9. Final resolver pipeline

### A. Raw source adapters

Normalize immutable observations with source/provenance identity. Preserve relation type. Do not infer assignment state from timestamp/sequence alone.

### B. Source/custody completeness

Determine whether policy-required sources and admission-custody evidence are present and reconciled. Missing required evidence fails closed without inventing rejection.

### C. Trusted exact-scope graph

Construct full governed scope before privacy projection. Validate identities, roots, state-transition predecessors, generations, cycles, state forks, cross-scope collisions, and relation-class legality.

Evidence/reference relations are represented separately and do not become state edges merely because they cite a state event. A state-transition edge and one or more evidence/reference edges may coexist on the same event if their independently closed relation rules all pass.

### D. Admission / semantic adapter

Admit only typed mechanically authorized state transitions into the state reducer. Legacy unstructured state-changing prose remains `SEMANTICS_UNKNOWN_LEGACY_UNSTRUCTURED` absent a reviewed deterministic adapter.

### E. Assignment-state reducer

Reduce only controlling admitted state-transition lineage. Terminal states absorb later non-state evidence. Explicit valid reactivation creates a new attempt.

### F. Caller privacy projection

Privacy is applied after internal adjudication and may minimize output without changing the internal controller.

### G. Separate mutation admission

Writes consume an exact resolver/workload version under CAS/serialization, append-path confinement, stable operation identity, request-digest replay safety, exact authority, and independent outcome/readback reconciliation.

## 10. Minimum acceptance invariants

1. `LATEST_OBSERVATION != CURRENT_ASSIGNMENT_STATE`.
2. State-transition lineage and evidence/reference lineage are different relation classes.
3. ACK/review/evidence relations do not consume assignment state merely by existing.
4. Evidence/reference relations may support policy-approved fan-out and cross-thread references.
5. A controlling state-transition relation and non-consuming evidence relation(s) may coexist on one event/operation where policy permits; one relation must not erase or prohibit the other.
6. Only admitted typed state transitions alter controlling assignment state.
7. Event sequence/timestamp/UUID has no standalone state authority.
8. Terminal state is absorbing absent explicit valid predecessor/generation-bound reactivation/reopen.
9. Workload snapshots have zero transition authority.
10. Expected-source incompleteness is explicit and fail-closed.
11. Unmirrored authority-bearing evidence does not silently become canonical state and does not permit stale canonical state to be described as source-complete.
12. Full trusted governed graph precedes privacy projection.
13. Hidden successors/siblings cannot re-promote older visible state.
14. State forks/cycles/disconnected/cross-scope collisions never resolve by chronology.
15. Legacy unstructured corrections are not NLP-promoted into control semantics.
16. Internally coherent but admission-custody-unproven evidence is unresolved/reissue-required, not silently admitted or labeled forged.
17. Raw chronology/head views cannot drive START/RESUME/workload/USE_AUTHORITY.
18. Assignment issuance consumes exact workload/currentness version under serialized CAS plus in-transaction re-resolution.
19. Authority-bearing append path must be mechanically confined; a bypassable CAS facade is not sufficient.
20. Mutation retry safety uses stable operation identity + semantic request digest + exact replay receipt.
21. Ambiguous write outcome requires readback/reconciliation before retry; blind replay is forbidden.
22. Retry-idempotency and vacancy/concurrency CAS remain independent gates.

## Final disposition

`FINAL_READY_FOR_REVIEW`

MU6 now has one integrated contract: full governed graph before privacy, closed relation classes, coexistence of controlling and evidence relations, non-consuming fan-out/cross-thread evidence lineage, admitted typed state reduction, terminal absorption, explicit source/custody uncertainty, and a separate writer path requiring both replenishment CAS/confinement and operation-id replay safety.

All concrete defects referenced above are already reported and triaged; this final creates no duplicate bug tickets.

No schema, production row, canonical coordination row, provider configuration, protected producer branch, credential, installation, deployment, or canonical memory was modified by MU6.
