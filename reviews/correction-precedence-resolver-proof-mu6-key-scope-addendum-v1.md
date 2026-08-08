# Mune MU6 Addendum — Correction Key Scope Contract

**Parent assignment:** `VOSS-20260808-MU6` / root `3464`  
**Parent proof:** `reviews/correction-precedence-resolver-proof-mu6-v1.md`  
**Class:** read-only semantic precision addendum  
**Mutation performed:** none

## Issue

MU6 needs one explicit policy choice before implementation freeze:

> Is a correction's canonical identity a globally unique `record_key`, or the scoped triple `(project_id, branch_id, record_key)`?

The answer cannot be inferred from whether a string *looks* namespaced, and the resolver must not let the caller choose whichever mode produces the preferred result.

Earlier accepted correction-custody discussion allowed either:

1. globally namespaced stable correction keys; or
2. resolver-side exact `(project_id,branch_id,record_key)` scoping.

A later Voss Slack nudge used stronger wording: fail `CROSS_SCOPE_KEY_COLLISION` if a non-globally-namespaced key occurs in more than one scope.

Those are compatible only if the correction domain formally chooses which key contract it uses.

## Fresh live evidence

Current live provider readback shows:

- correction raw keys reused across more than one `(project_id,branch_id)` scope: `0`;
- all save-state raw keys reused across more than one scope: `0`.

Therefore this is a **future invariant choice**, not a current data-conflict incident.

No raw record keys are copied here.

## Recommended V1 choice

I recommend the correction domain choose one rule and encode it in the adapter/policy, rather than support per-call caller-selectable mode.

### Preferred: `SCOPED_CORRECTION_KEY_V1`

Canonical correction identity:

```text
(project_id, branch_id, record_key)
```

Rules:

- exact project+branch+key is bound before graph construction;
- every predecessor/successor edge in that correction lineage must remain inside the same scoped triple;
- a same raw `record_key` elsewhere is diagnostic `RAW_KEY_SCOPE_REUSE_OBSERVED`, not automatically a conflict for this scoped lineage;
- `vera_current_save_state` remains unsafe because it ignores project/branch partitioning, so the resolver never uses that view as authority;
- downstream receipts bind the full scoped identity, never bare `record_key`.

This is the smallest rule aligned with the fact that `project_id` and `branch_id` are already first-class columns.

### Alternative: `GLOBAL_CORRECTION_KEY_V1`

If the design instead wants bare `record_key` to be globally canonical across all projects/branches, then:

- key construction must be mechanically namespaced/versioned by the trusted writer/adapter;
- any raw-key reuse across more than one scope is `CONFLICTED_CROSS_SCOPE_KEY_REUSE`;
- the resolver may still bind project/branch for privacy/routing, but global uniqueness is an additional invariant;
- future persistence tests must prove the key namespace rather than rely on current cleanliness.

This is also defensible, but it should be chosen deliberately because it creates a stronger writer contract than the current database constraint provides.

## What is unsafe

Reject this ambiguous rule:

```text
if key looks globally namespaced, treat as global;
otherwise sometimes scope it, sometimes declare collision
```

Reasons:

- namespace semantics become string heuristics;
- a future naming-format change alters authority/currentness without a schema/policy version change;
- caller can potentially influence interpretation;
- the same stored lineage can resolve differently across runtimes.

Likewise, do not inspect statement/payload prose to decide whether a key was "meant" to be global.

## Relation to generic save-state

Do not impose correction key rules on the entire save-state table.

Fresh MU6 topology evidence already shows generic `CONTINUITY` supersession frequently changes key/scope. The correction adapter can demand same scoped key because that is a **correction-domain invariant**, not because `supersedes_record_id` globally means same-key replacement.

## Proposed resolver contract refinement

Replace caller-facing `key_mode` with adapter-owned:

```text
correction_key_contract = SCOPED_CORRECTION_KEY_V1
```

or, if Voss chooses the stronger global design:

```text
correction_key_contract = GLOBAL_CORRECTION_KEY_V1
```

The request carries only the required canonical identity fields. The trusted correction adapter supplies the contract/version.

This removes one unnecessary policy lever from the caller and makes cross-runtime results deterministic.

## Verdict

`KEY_SCOPE_POLICY_MUST_BE_FROZEN_BY_CORRECTION_ADAPTER; DO_NOT INFER FROM STRING SHAPE`

My recommendation is `SCOPED_CORRECTION_KEY_V1`, with the full `(project_id,branch_id,record_key)` bound into every resolver receipt. If Vera wants global bare-key uniqueness instead, make that a mechanically enforced writer/adapter invariant and fail reuse explicitly.

No save-state row, schema, view, index, policy, Project file or canonical coordination state was modified.