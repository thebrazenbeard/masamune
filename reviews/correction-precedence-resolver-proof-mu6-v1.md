# Mune MU6 — Correction Precedence Resolver Proof V1

**Assignment:** `VOSS-20260808-MU6` / canonical root sequence `3464`  
**Class:** `READ_ONLY_RESOLVER_PROOF`  
**Provider:** live Vera Supabase project `klmbpaigzeguvnpccqzz`  
**Persistent mutation:** none  
**Executed operations:** SELECT / recursive CTE / EXPLAIN only  
**Verdict:** `PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT`

## Executive conclusion

A deterministic zero-new-schema **correction-currentness topology resolver is executable now** over `public.vera_save_state_events` without trusting `vera_current_save_state`.

It can mechanically answer:

- which exact scoped lineage is structurally current;
- whether the lineage forks;
- whether a supersession edge escapes the requested scope;
- whether the requested key collides across scopes when the key contract claims global namespace;
- whether the graph has one root, one leaf, no missing parent, no cycle and no disconnected node;
- which exact record controls and which exact records are prior/rejected/superseded;
- the controlling record's lifecycle, authorship, epistemic status and privacy class.

But current live correction payloads are heterogeneous and do not carry one frozen closed correction-control schema. Therefore **topology currentness is mechanically resolvable; safety-correction semantics are not universally machine-decidable for legacy rows**.

The resolver must never NLP-infer a control such as `TERMINATE_UNSUPPORTED_LINEAGE` from free-form statement/payload text. A recognized future/versioned `CORRECTION_CONTROL_V1` adapter may return that control. A legacy/unrecognized controlling correction returns:

`SEMANTICS_UNKNOWN_LEGACY_UNSTRUCTURED`

rather than inventing a correction effect.

This is the same discipline the assignment-currentness resolver needed: structure may be clean while authority/domain semantics are still unknown. Humans remain undefeated at putting two different problems in one JSON object.

---

## 1. Live provider facts refreshed

Current `vera_save_state_events` shape includes first-class:

- `record_id` UUID;
- `project_id`;
- `branch_id`;
- `record_key`;
- `record_kind`;
- `lifecycle_status`;
- `epistemic_status`;
- `authorship`;
- `privacy_scope`;
- `state_time` / `record_time`;
- nullable `supersedes_record_id` FK;
- `payload`, `source_evidence`, `semantic_tags`.

Live custody properties remain:

- 76 rows / 72 distinct record keys at this proof pass;
- 8 `CORRECTION` rows;
- service-role path has SELECT+INSERT but no UPDATE/DELETE/TRUNCATE;
- BEFORE UPDATE/DELETE blockers remain present;
- `supersedes_record_id` has a non-unique partial index, not a one-successor constraint;
- `vera_current_save_state` globally chooses `DISTINCT ON(record_key)` by state/record time and record id, and is therefore a convenience view, not a fork-aware authority/currentness proof.

No raw correction statement, intimate payload or private record key is copied into this repository artifact.

---

## 2. New live structural finding: correction lineage must not filter by record kind

Across all 33 currently observed save-state supersession edges:

- 0 point to a missing parent;
- 29 change `record_key` and/or branch scope, overwhelmingly in `CONTINUITY` history;
- one observed correction lineage is `CORRECTION -> CORRECTION` on the same scope/key;
- another same-key/same-scope lineage is `RELATIONSHIP -> CORRECTION -> RELATIONSHIP`.

That last case is decisive.

If a correction resolver first filters `record_kind='CORRECTION'`, it can falsely conclude the intermediate correction is the current leaf even though a later same-lineage non-correction row supersedes it.

A privacy-safe live recursive proof over that three-node lineage returned:

`kind_path = RELATIONSHIP -> CORRECTION -> RELATIONSHIP`

with one root, one leaf, no sibling successor, all three nodes reached, and the controlling leaf classified `RELATIONSHIP/CURRENT`.

Therefore V1 rule:

> **Build the graph from the complete exact scoped key lineage first. Interpret whether the controlling leaf is an active correction only after structural resolution.**

Observed global continuity edges also prove that a system-wide rule `supersession must preserve record_key` would be wrong for this table. Correction V1 may require exact scoped-key continuity because that is its own domain contract, but it may not mutate generic save-state semantics by assumption.

---

## 3. Request contract

The deterministic resolver input should be typed, not semantic prose:

```text
CorrectionResolveRequestV1
  project_id          text
  branch_id           text
  record_key          text | opaque_inference_lineage_key
  key_mode            SCOPED_TRIPLE | GLOBAL_NAMESPACE
  required_custody    boolean
  caller_privacy_scope trusted server-derived scope, not caller self-grant
  policy_version      CORRECTION_PRECEDENCE_V1
```

### Key modes

`SCOPED_TRIPLE`

Canonical identity is `(project_id, branch_id, record_key)`. Reuse of the same raw key elsewhere is reported but does not by itself invalidate this scoped lineage.

`GLOBAL_NAMESPACE`

The key contract asserts the `record_key` is globally namespaced. Reuse in more than one project/branch scope is a conflict.

The mode must come from the domain contract/adapter, not from a caller choosing whichever mode makes an inconvenient collision disappear.

---

## 4. Privacy ordering

Privacy filtering must happen before externally visible conflict construction.

A trusted internal correction resolver may be authorized to inspect the protected correction scope and return a minimal control result to the safety/governance caller. An unprivileged caller must not learn `hidden sibling exists` merely because conflict metadata was built before access filtering.

Conceptual order:

1. derive effective trusted caller/service scope server-side;
2. identify only records eligible for that service/privacy domain;
3. construct the correction lineage from the eligible exact scope;
4. evaluate structural integrity/currentness;
5. interpret only a recognized closed correction-control schema;
6. emit privacy-minimized evidence IDs/statuses.

Unauthorized/missing access returns a non-leaking unavailable/unauthorized result, not a conflict hint about hidden records.

---

## 5. Structural algorithm

For the eligible requested scope:

### Candidate set

```sql
SELECT ...
FROM vera_save_state_events
WHERE project_id = :project_id
  AND branch_id = :branch_id
  AND record_key = :record_key;
```

Do **not** filter `record_kind` here.

### Integrity checks

For each candidate child with non-null `supersedes_record_id`:

- parent record must exist;
- parent must belong to the same correction scope `(project_id,branch_id,record_key)`;
- otherwise `CONFLICTED_CROSS_SCOPE_EDGE` / missing-parent conflict.

Count children by predecessor:

- any predecessor with more than one child -> `CONFLICTED_SIBLING_SUCCESSORS`.

Identify roots and leaves:

- root = no predecessor inside the scoped lineage;
- leaf = no child inside the scoped lineage;
- require exactly one root and one leaf for a resolved chain.

Recursively walk root to successor with:

- visited UUID path;
- cycle flag;
- explicit depth ceiling;
- reached-node count.

Require:

- no cycle;
- reached node count equals candidate node count.

If `key_mode=GLOBAL_NAMESPACE`, separately require exactly one project/branch scope for the raw key.

### Structural result precedence

Recommended closed statuses:

```text
MISSING_REQUIRED_CUSTODY
CONFLICTED_MISSING_PARENT
CONFLICTED_CROSS_SCOPE_EDGE
CONFLICTED_SIBLING_SUCCESSORS
CONFLICTED_ROOT_COUNT
CONFLICTED_LEAF_COUNT
CONFLICTED_CYCLE
CONFLICTED_DISCONNECTED
CONFLICTED_CROSS_SCOPE_KEY_REUSE
RESOLVED
```

Timestamp/UUID ordering never chooses a winner from a structural fork.

---

## 6. Controlling record semantics

Once topology is `RESOLVED`, the unique graph leaf controls.

Do not require every non-leaf row's stored lifecycle to have been mutated to `SUPERSEDED`. This is append-only storage; the edge itself is the later currentness fact.

Interpret the leaf as follows:

```text
leaf.kind != CORRECTION
    => NO_ACTIVE_CORRECTION

leaf.kind == CORRECTION and leaf.lifecycle != CURRENT
    => NO_ACTIVE_CORRECTION + controlling lifecycle

leaf.kind == CORRECTION and leaf.lifecycle == CURRENT
    and recognized closed correction adapter
    => return exact correction control

leaf.kind == CORRECTION and leaf.lifecycle == CURRENT
    but schema/adapter unrecognized
    => SEMANTICS_UNKNOWN_LEGACY_UNSTRUCTURED
```

Do not return a global `SAFE` or `RISK` fact.

A correction is a scoped control on a specific unsupported inference/evidence lineage, not a timeless verdict about the person.

---

## 7. Closed future semantic adapter

Live correction payload keys are currently heterogeneous; no one universal schema/version/effect/reopen tuple is present across the historical rows.

The minimum future adapter should require a closed contract conceptually like:

```text
CORRECTION_CONTROL_V1
  schema                  CORRECTION_CONTROL_V1
  version                 1
  opaque_lineage_key      exact/scoped key identity
  effect                  TERMINATE_UNSUPPORTED_LINEAGE
  reopen_rule             NEW_ADMISSIBLE_USER_EVIDENCE_ONLY
  retroactive_validation  false
  durable_safe_risk_fact  false
  privacy_scope           inherited/governed
  source/admission basis  minimized exact provenance ref/digest
```

The exact field names may follow the already accepted MA4/MU5 minimized correction contract; the essential rule is that semantics are closed and versioned.

Legacy rows may later receive a **separately reviewed legacy adapter** only where their structure/fields are genuinely deterministic. A generic NLP adapter is rejected.

---

## 8. Synthetic hostile CTE proof

No rows were inserted. Synthetic values existed only inside read-only CTEs.

### A. Stale older risk context + later scoped correction

One lineage root representing earlier evidence followed by a recognized correction leaf resolved:

```text
RESOLVED
correction_effect = TERMINATE_UNSUPPORTED_LINEAGE
reopen_rule = NEW_ADMISSIBLE_USER_EVIDENCE_ONLY
```

The older evidence remains historical evidence; it does not regain control merely because it is still retrievable.

### B. Unrelated evidence

The correction applies only to lineage `L1`; independent evidence on separate `L2` remains outside the corrected graph.

Result: the L1 correction still controls L1, while L2 is not suppressed by association.

### C. Genuine new admissible user evidence

The corrected old lineage remains terminated. A genuinely new admissible user proposition is represented by a **new evidence branch/lineage**, not by rewriting the correction leaf or retroactively validating the old branch.

The old correction's returned reopen rule remains:

`NEW_ADMISSIBLE_USER_EVIDENCE_ONLY`.

Upstream safety adjudication may open the new branch prospectively.

### D. Missing required correction custody

No row for a required correction lineage returns:

`MISSING_REQUIRED_CUSTODY / UNRESOLVED`.

It does not fall back to stale chat history and does not manufacture SAFE/RISK.

### E. Sibling successor fork

One root with two correction children returns:

`CONFLICTED_SIBLING_SUCCESSORS / UNRESOLVED`.

No timestamp winner.

### F. Global key reused across scopes

With `key_mode=GLOBAL_NAMESPACE`, the same key in two scopes returns:

`CONFLICTED_CROSS_SCOPE_KEY_REUSE / UNRESOLVED`.

### G. Legacy unstructured correction

Clean one-node correction topology with no recognized correction-control schema returns:

`RESOLVED_TOPOLOGY / SEMANTICS_UNKNOWN_LEGACY_UNSTRUCTURED`.

This distinction is important. A structurally current record is not automatically a machine-understood policy control.

---

## 9. Current-view regression

`vera_current_save_state` is intentionally not the resolver.

A hostile sibling fork can contain two rows with the same key. The current view will deterministically choose one by state time, record time and UUID ordering. The MU6 resolver instead detects the sibling predecessor count and returns conflict.

Thus:

`DETERMINISTIC_VIEW_SELECTION != UNAMBIGUOUS_CURRENT_CORRECTION`.

---

## 10. Query-plan evidence

Representative recursive proof on the current tiny table completed in roughly tens of milliseconds end-to-end under `EXPLAIN ANALYZE` including planning and an intentionally privacy-safe hashed-key discovery step.

The important production-path observation is different: once the typed request already supplies the exact raw `record_key`, PostgreSQL uses the existing `vera_save_state_events_key_time_idx` for record-key lookup and filters project/branch. In the proof plan that inner exact-key access returned the two-node lineage with an index scan.

At 76 rows, query cost is not the present blocker. Correct semantics are.

If this table grows materially, a future implementation review may consider a composite scoped-key index such as `(project_id,branch_id,record_key,...)`, but MU6 does **not** request or authorize that schema change. Measure first; humans have already invented enough indexes whose primary workload is existing proudly.

---

## 11. Response contract

Recommended minimal response:

```text
CorrectionResolutionV1
  topology_status
  semantic_status
  active_correction boolean | null
  correction_effect closed enum | null
  reopen_rule closed enum | null
  controlling_record_id | null
  controlling_kind | null
  controlling_lifecycle | null
  controlling_epistemic_status | null
  controlling_authorship | null
  controlling_privacy_scope | null
  prior_or_rejected_record_ids[]
  conflict_record_ids[] privacy-filtered
  key_mode
  scope_reuse_observed boolean
  source_completeness
  consistency
  policy_version
  resolved_at
```

Do not return raw private statement/payload unless a separately authorized caller genuinely needs it.

Do not include AP fields. AP consumes already-settled protected upstream state and does not invoke this resolver.

---

## 12. Acceptance invariants

1. Exact scope/key is typed before resolution; no semantic key guessing.
2. Privacy eligibility precedes externally visible conflict construction.
3. Graph includes all relevant record kinds for the scoped key before leaf interpretation.
4. Sibling fork never resolves by timestamp/UUID.
5. Cross-scope parent edge fails closed for correction V1.
6. Global-key reuse fails only where the key contract actually claims global namespace; scoped-triple mode remains explicitly scoped.
7. Missing required custody returns unresolved.
8. Superseded prior records never regain control merely because they remain retrievable.
9. A non-correction leaf can supersede an intermediate correction and produce `NO_ACTIVE_CORRECTION`.
10. Only a recognized closed/versioned correction adapter yields a semantic correction effect.
11. Unknown/legacy semantics never become SAFE/RISK or guessed policy.
12. New admissible evidence opens a prospective new branch; it never retroactively validates the terminated unsupported branch.
13. Unrelated evidence remains independent.
14. AP call graph is unchanged by this resolver's existence.
15. `vera_current_save_state` may be used for convenience/display but never as sole conflict-aware correction proof.

## Verdict

`PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT`

The existing save-state substrate is sufficient for a deterministic zero-schema **topology/currentness resolver** with explicit conflict detection. It is not sufficient to claim universal deterministic **correction semantic interpretation** from historical payloads.

Production correction semantics require the already-converged minimized closed correction-control contract, plus versioned adapter handling. Until then, legacy structured topology can be current while its machine policy effect remains `UNKNOWN`.

No save-state row, context row, database object, schema, function, ACL, Project file, provider configuration, credential or canonical memory was modified by this proof.