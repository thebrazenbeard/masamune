# Mune MU4 Addendum — Observed Cleanliness Is Not a Structural Invariant

**Parent review:** `reviews/correction-store-durability-audit-v1.md`  
**Lane:** `VOSS-20260808-MU4`  
**Mode:** fresh provider-backed read-only addendum  
**Disposition:** original `APPROVED_CUSTODY_DIRECTION` unchanged

## Fresh aggregate observation

Independent live Supabase readback now shows:

- `vera_save_state_events`: **74 rows**;
- **70 distinct `record_key` values**;
- **8 CORRECTION rows**;
- **0 observed parents with more than one successor** through `supersedes_record_id`;
- **0 observed record keys reused across distinct `(project_id, branch_id)` scopes**.

These are encouraging data-quality observations.

They do **not** strengthen the table's schema-level guarantees.

## Required language

Use:

`NO_FORK_OBSERVED`

not:

`FORK_PREVENTED`

Use:

`NO_CROSS_SCOPE_KEY_COLLISION_OBSERVED`

not:

`KEY_SCOPE_ISOLATION_ENFORCED`

The distinction is mundane, which is exactly why systems keep getting it wrong.

## Why the original caveats remain controlling

### Supersession fork

The `supersedes_record_id` index is non-unique. Two concurrent or buggy successors remain structurally permitted.

A future fork would be silently flattened by `vera_current_save_state` because the view uses deterministic `DISTINCT ON(record_key)` ordering rather than lineage conflict detection.

Therefore a controlling correction readback must still enumerate the exact scoped lineage and reject sibling successors/multiple roots.

### Cross-scope key reuse

`vera_current_save_state` still partitions only by `record_key`, not by project/branch/key.

The fact that current writers have not reused a key across scopes does not make the view scope-safe. Globally namespaced keys and explicit `(project_id, branch_id, record_key)` resolver predicates remain required.

### Operation identity

Current cleanliness also does not solve ambiguous commit/replay. No enforced save-state operation identity exists. A transport-ambiguous INSERT remains non-blind-retryable.

## Updated acceptance wording

The strongest honest current claim is:

> The live save-state dataset is presently clean with respect to observed supersession forks and cross-scope record-key collisions, and the ordinary service path is materially stronger/append-only relative to context-v3. The schema still permits those conflict classes, so correction continuity requires direct scoped lineage conflict detection and cannot rely on `vera_current_save_state` as proof of unambiguous current state.

Original MU4 verdict remains `APPROVED_CUSTODY_DIRECTION` under the bounded single-writer/scoped-readback contract.

No database write, migration, correction insertion, native Project mutation, producer-branch mutation, deployment, credential action, merge, paid-service action, or canonical-memory promotion was performed.