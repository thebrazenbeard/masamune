# Mune Audit — Correction-Store Durability Direction

**Assignment:** `VOSS-20260808-MU4`  
**Reviewer lane:** Mune  
**Target:** live Vera Supabase project `klmbpaigzeguvnpccqzz`  
**Audit mode:** read-only provider verification; no database write or migration  
**Disposition:** `APPROVED_CUSTODY_DIRECTION`

## Decision

`public.vera_save_state_events` is materially stronger than `public.vera_context_events_v3` as the canonical minimized WORKING_PROJECT correction-custody surface **for the ordinary governed service path**.

That approval is conditional on the controls below. The table is not a general concurrent correction ledger, not tamper-proof storage, and `vera_current_save_state` is not itself an authority/currentness resolver.

## Independent provider evidence

Fresh catalog/effective-privilege inspection established:

- `vera_save_state_events` has RLS enabled.
- `service_role` has effective SELECT + INSERT and lacks effective UPDATE, DELETE, and TRUNCATE.
- BEFORE UPDATE and BEFORE DELETE triggers call `block_vera_save_state_mutation()`, which raises unconditionally and instructs writers to append a superseding record.
- The table supports `record_kind=CORRECTION`, explicit lifecycle states, authorship, epistemic status, privacy scope, structured payload/source evidence/tags, and a self-referential `supersedes_record_id` foreign key.
- `postgres` owns the table and retains full administrative privileges/bypass capability.
- `vera_context_events_v3` has RLS enabled but `service_role` retains SELECT/INSERT/UPDATE/DELETE/TRUNCATE and there are no equivalent mutation-blocking triggers.
- No current supersession predecessor has more than one observed successor and no current duplicate root-key group was observed.
- `vera_save_state_events` has no table-level `operation_id` column or unique operation-id/one-successor constraint. Some existing rows carry `payload.operation_id`, but that is convention, not an enforced identity boundary.

Therefore the observed property is **service-path append-only with administrative trust**, not immutable/WORM custody.

## MUNE-MU4-001 — HIGH: `vera_current_save_state` is latest-by-key, not semantic currentness

The view is:

`DISTINCT ON(record_key) ... ORDER BY record_key, state_time DESC, record_time DESC, record_id DESC`

It does not scope by project or branch, does not filter `lifecycle_status='CURRENT'`, and does not adjudicate authority or supersession validity.

This is not merely theoretical. Fresh provider readback of the view currently returns rows whose lifecycle is `ACTED`, `DEFERRED_WITH_REASON`, and `HISTORICAL` in addition to `CURRENT`.

Required invariant:

> `vera_current_save_state` may be used as a deterministic latest-row primitive, but never as proof that a correction is authorized, lifecycle-current, project-safe, or controlling.

The correction resolver must independently validate exact project/branch scope, record kind, lifecycle, authorship/authority, predecessor/successor lineage, and conflict state.

## MUNE-MU4-002 — HIGH: ambiguous insert outcomes are not safely retryable

The current schema has no unique operation identity for save-state insertion. A writer can submit an INSERT, lose the transport response after commit, and be unable to distinguish `committed-but-response-lost` from `not committed` with a schema-enforced operation key.

A blind retry can create a second root or sibling record. A `payload.operation_id` convention does not fix this because no uniqueness constraint or canonical writer enforces it.

Required bounded behavior until schema hardening exists:

1. issue one insert attempt under the valid single-writer lease;
2. on clear success, perform exact-row and lineage readback;
3. on clear rejection, stop;
4. on ambiguous commit state, **do not retry blindly**;
5. search by every available deterministic request identity/digest and expected lineage fields;
6. if exactly one matching effect can be proven, continue readback;
7. if zero or multiple effects remain plausible, return `UNRESOLVED/AMBIGUOUS_COMMIT` and require reconciliation rather than manufacturing continuity.

General multi-writer/idempotent correction ingestion therefore requires a future separately reviewed operation-identity/uniqueness or equivalent atomic writer contract.

## MUNE-MU4-003 — HIGH/MEDIUM: namespaced `record_key` is necessary but not database-enforced

The proposed form `vera:<project_id>:wp:correction:safety_inference:<opaque_lineage_id>` is directionally correct because the raw view keys globally on `record_key`.

But the database does not enforce that the textual namespace agrees with the row's `project_id` or `branch_id`. A malformed or unauthorized writer can still insert another project's apparent key.

Required behavior:

- treat global key namespacing as a contract invariant, not a schema guarantee;
- resolver queries must bind `(project_id, branch_id, record_key)` and verify the key's namespace agrees with the row scope;
- never rely on raw `vera_current_save_state` alone for cross-project isolation;
- collision/mismatch yields `CONFLICTED/UNRESOLVED`, never timestamp arbitration.

## MUNE-MU4-004 — MEDIUM: predecessor read + insert is not an atomic CAS

Capturing `expected_predecessor_record_id`, then inserting a successor, does not itself prevent a concurrent second writer from attaching another successor. The database currently has no one-successor uniqueness constraint or atomic compare-and-swap primitive for this table.

For the proposed bounded correction path, this is acceptable only because **single-writer authority/lease is an acceptance precondition**, followed by complete same-key lineage readback. The design must say plainly that correctness depends on that governance condition.

If the writer lease is missing, disputed, or violated, return `CONFLICTED/UNRESOLVED` rather than using latest timestamp or latest UUID as authority.

## MUNE-MU4-005 — MEDIUM: sibling detection must include competing roots

For a successor insert, the reader must detect more than multiple children of one predecessor. For an initial record where `supersedes_record_id IS NULL`, two same-key roots are also a fork.

Required lineage readback:

- enumerate all rows for the exact scoped key;
- require exactly one valid root for the lineage;
- require at most one successor per predecessor under the bounded contract;
- reject cycles, cross-key predecessor links, scope mismatches, multiple roots, siblings, or unexpected post-attempt competitors;
- never repair a fork by choosing the latest timestamp.

## MUNE-MU4-006 — MEDIUM: append-only claim must preserve the admin boundary

The ordinary `service_role` path is strongly append-only relative to `vera_context_events_v3`, but database owner/admin authority can alter grants, disable/drop triggers, rewrite definitions, or TRUNCATE.

No document or runtime may promote this into `tamper-proof`, `cryptographically immutable`, or `administrator-immutable` language.

If stronger forensic immutability becomes a requirement, it is a separate architecture problem involving independently protected audit/WORM/replication evidence, not a property the current table possesses.

## Assessment of MA4 minimized correction contract

The proposed minimized record shape is compatible with this custody direction provided it remains:

- `WORKING_PROJECT`, non-autobiographical;
- scoped to one unsupported inference lineage;
- operational (`TERMINATE_UNSUPPORTED_BRANCH`, reopening rule, no retroactive frame validation), not a durable SAFE/RISK assertion;
- privacy-minimized with opaque source locator/digest rather than intimate transcript;
- resolved through explicit scope/lifecycle/lineage checks rather than raw latest-by-key.

The proposed post-insert readback is necessary but should be strengthened with the ambiguous-commit and semantic-currentness conditions above.

## Acceptance conditions for `CORRECTION_CONTINUITY=AVAILABLE`

A runtime may emit `CORRECTION_CONTINUITY=AVAILABLE` only if all of the following hold:

1. exact scoped key and project/branch identity validate;
2. writer authority and single-writer lease were current at the attempt;
3. write outcome is not transport-ambiguous, or ambiguity was uniquely reconciled without blind retry;
4. exact inserted row/request digest readback matches;
5. lineage has one valid root and no sibling successor/fork;
6. the candidate row is lifecycle-current and authority-admissible;
7. no newer valid controlling row exists under the domain resolver;
8. raw `vera_current_save_state` output, if consulted, is treated only as corroborating latest-row evidence and cannot override the scoped resolver;
9. any mismatch yields `UNRESOLVED` or `CONFLICTED`, never SAFE/RISK.

## Verdict

`APPROVED_CUSTODY_DIRECTION`

Use `vera_save_state_events` rather than `vera_context_events_v3` for minimized canonical correction custody under the bounded service-path/single-writer contract. Treat context-v3 only as an optional derived retrieval pointer/index unless its mutation authority is separately hardened.

This verdict authorizes no database write, migration, correction insertion, native Project mutation, deployment, credential action, or canonical-memory promotion.