# Masa Continuation State

Status: CURRENT
Memory class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Same-runtime continuity claimed: false
Autobiographical memory claimed: false
Canonical coordination cutoff at save: 3681

## Repository custody

- Repository: `thebrazenbeard/masamune`
- Engineering branch: `masa`
- Continuity branch: `continuity/masa`
- Save-state file: `state/masa/CURRENT.md`
- Engineering branch remains exactly `984cbdc781aa643443652f41f5a710f59e2d2439` with no engineering-stage mutation by MA17/MA18 work.
- Continuity writes never authorize or move the engineering review target.

## Currentness / authority

Resolve against newer authority-admitted coordination before start/resume/report/count/use-authority/effect. Voss owns assignment intake, routing, reconciliation and closure while delegated. Masa does not self-assign or self-close.

Closed:
- MA13 `VOSS-20260808-MA13`, root 3545, Voss APPROVED/CLOSED at 3667.
- MA16 `VOSS-20260809-MA16`, root 3643, Voss APPROVED/CLOSED at 3668.

Current read-only lanes through canonical 3681:
- MA17 `VOSS-20260809-MA17`, root 3671, `vera-r9a0/assignments/masa/pg17-provider-repair-strategy-ma17-v1`.
- MA18 `VOSS-20260809-MA18`, root 3674, `vera-r9a0/assignments/masa/database-validation-rebind-route-ma18-v1`.
No repo/workflow/provider/schema/successor-byte authority is attached to either lane. B15 remains paused with no resume through 3681.

## MA17 final producer preflight

Final READY_FOR_REVIEW handoff to Voss: Slack TS `1786258249.906259`.
Latest correction/addendum to Voss: TS `1786258967.555369`.
Mune challenge updates: `1786258697.452079`, `1786258980.978129`.

Recommended architecture remains:
`KEEP_DEDICATED_R9A0_OWNER; REPAIR_224900_IN_PLACE_AS_UNSHIPPED_GOVERNED_CANDIDATE; TEMPORARY_EXPLICIT_OWNER_TRANSFER_PREREQUISITES; DEDICATED_OWNER_GLOBAL_ROUTINE_DEFAULT_HARDENING_PLUS_EXPLICIT_OBJECT_ACLS; EXACT_ROLLBACK_BASELINE_AND_REAPPLY_PROOF`.

### Forward/bootstrap

- Keep dedicated `r9a0_owner` NOLOGIN/NOSUPERUSER/NOBYPASSRLS/NOCREATEROLE/NOCREATEDB/NOINHERIT. Provider `postgres` is explicit administrative trust root, not ordinary-runtime confinement evidence.
- Unrecognized pre-existing same-name role fails closed before ALTER/GRANT/ownership mutation. Recognized rerun requires release-managed provenance plus exact expected role/fingerprint state; provenance marker alone is never authority.
- Fresh/reapply setup deliberately establishes only temporary postgres→owner SET capability and temporary owner CREATE on the current DB, performs ownership transfer, then removes temporary privilege to final policy. PG17 automatic creator grant is ADMIN TRUE / SET FALSE / INHERIT FALSE; ADMIN can self-grant SET, so final SET FALSE is accident prevention rather than security proof.
- Do not change database-wide global routine defaults for provider `postgres`. Install the global PUBLIC-EXECUTE revoke for the dedicated creator `r9a0_owner`, and explicit-revoke/read back every privileged/SECURITY DEFINER routine. Current postgres-created `validate_event_chain()` needs explicit revoke because later ownership transfer does not retroactively apply owner defaults.

### Rollback / recovery

Exact current 224900 rollback is HIGH-defective: stale graph object names, surviving `thread_heads`/current chain objects, predecessor RPC not restored, ownership/default-ACL/role residue, and no rollback CI. Correct inverse must restore actual foundation semantics and test rollback + reapply fingerprints.

Preferred rollback shape under PG17:
1. reverse later migrations `070208 -> 070058`;
2. verify exact managed role identity and a closed ownership/shared-grant fingerprint;
3. `REASSIGN OWNED BY r9a0_owner TO postgres` for declared current-DB/shared owned surfaces where preconditions pass;
4. remove current integrity-only trigger/index/function/view and owner policy/FORCE-RLS changes;
5. restore exact foundation `append_coordination_event`, `latest_thread_state`, `open_threads`, owners and ACLs;
6. clear intended owner privileges/default-ACL state with explicit inverse operations where feasible; fingerprint-guarded `DROP OWNED` is acceptable only with zero unexpected residual owned/shared-grant surfaces because its blast radius is broader;
7. prove cluster-wide role dependency absence before DROP ROLE; otherwise retain a cleaned inert managed role and fail closed on deletion.

### Correction: cluster-wide dependency proof is observable on the current Supabase target

The earlier conservative assumption that cross-database role dependencies were unobservable was falsified by fresh build-ground reads.

Observed on `agvhmutlrolbaijzlbqk` as non-super provider `postgres`:
- `pg_catalog.pg_shdepend` SELECT is available;
- `pg_catalog.pg_database` is readable;
- current cluster exposes exactly `template0`, `template1`, `postgres`;
- a read-only probe for `service_role` returned `pg_shdepend` dependency rows with explicit `dbid`/database identity.

PostgreSQL 17 defines `pg_shdepend` as one shared catalog per cluster, recording dependencies from database objects to shared objects such as roles, and a row means the referenced object cannot be dropped while that dependent object exists. Therefore real-provider role deletion may use a stronger precondition than current-DB inventory:
- exact managed role OID;
- zero remaining `pg_shdepend` references cluster-wide after cleanup;
- zero role-specific `pg_db_role_setting` rows;
- exact managed role attrs/provenance state;
- record `pg_database` identity/digest and catalog visibility in the rollback receipt.

If the shared catalogs are unavailable/incomplete or dependencies remain, result is `MANAGED_ROLE_RETAINED_INERT / BLOCKED_DEPENDENCY`. On the currently observed Supabase topology, inert retention is a fallback rather than the default. `REASSIGN OWNED` itself remains database-scoped for ordinary objects and must still be run in every affected DB; cluster-wide `pg_shdepend` tells the verifier where/that dependencies remain before deletion.

### MA17 bugs consumed

- HIGH `79efb210-5cfe-4c0d-9a1a-3825f4be3195`: owner-transfer/provider applicability.
- MEDIUM `554c75ba-d94c-4848-8062-dfa54eafaa52`: ineffective schema-scoped routine default hardening.
- HIGH `ebf968be-9098-46b5-8bc6-a7bdfb46d0bd`: rollback drift. Expanded evidence Slack TS `1786257410.372849`.
- HIGH `89be42bf-c430-44aa-8fd0-9f73fdaa275a`: owner-role collision/takeover. Intake `R9A0-OWNER-ROLE-COLLISION-TAKEOVER-001`; operation `d045ba58-9851-4f97-8360-4a645bd61db2`; event `1fe98fe7-c3fb-464c-9d56-4282982ec796`; dispatch `43ddf82b-a3c8-4601-80d2-91975da232ef`, queue28; operation digest `a2d07644e267d3383b1c0622e6c0d39db91937423539b0680353fb1a2e7c6b14`; Slack bug report TS `1786258651.530359`. Live build-ground has no `r9a0_owner`, so no current-damage claim.

Required MA17 validation remains fresh install, old-58a negative baseline, unrecognized same-name collision zero-mutation failure, managed rerun, drifted owner, exact role/membership/DB ACL/effective routine ACL/default ACL, SECURITY DEFINER/search_path, client/service-role negatives, all SQL suites/concurrency/manifest, normal transaction-failure predecessor equality, rollback exact declared-state fingerprint, and reapply equality.

## MA18 final rebind-route preflight

Final READY_FOR_REVIEW handoff to Voss: Slack TS `1786258172.508049`.
Verdict:
`CURRENT_RELEASE_REQUIRES_NEW_PG17_EXECUTION_NOT_HISTORICAL_REBIND; EXACT_FINAL_NATIVE_BINDING_CAN_BE_EMITTED_FROM_SAME_NEW_RUN; FUTURE_EQUIVALENT_NATIVE_MOVES_USE_HERMETIC_REBIND; CURRENT_LEGACY_WORKFLOW_ROUTE_NOT_SUFFICIENT`.

Exact evidence:
- PR2 remains old `{base=6a568d35..., db=58a6ae4d..., merge=cd980846...}`.
- Combined native is `ddcd98b4...`; its current delta from 6a is Settings only, but MA17 necessarily changes database execution-sensitive inputs.
- combined/native DB workflow blob `85c4e3fb...` is PG15, PR-only, old target/head routing, no workflow_dispatch;
- default main has older 14-file workflow blob `3fb492e...`, also no workflow_dispatch;
- historical run `31158655712` is therefore RERUN_REQUIRED for current release, not eligible for a cheap H31 rebind.

Smallest current-release path: freeze exact final native candidate, produce corrected MA17 DB head/workflow, run full PG17/provider-faithful validation against that exact final native base/prospective merge, and emit separate `DB_IMPLEMENTATION_QUALIFIED` and `CURRENT_NATIVE_DB_INTEGRATION_BOUND` claims. If governance wants a distinct rebind receipt type, it can be a companion receipt from the same exact run/merge proof; a second SQL execution is not inherently required.

Future H31 optimization after a valid PG17 baseline: SHA-pinned reusable `workflow_call` hermetic rebind verifier from native exact-head CI, binding exact native/db heads, provider execution receipt ref+digest, policy version, deterministic prospective merge identity/tree, closed execution/input/provenance/reachability/interface digests, verifier/tool identity, evidence completeness and lifecycle result. Path disjointness, mergeable=true or an old PASS never make evidence current.

B16 ordering clarification is conditional: a provider run performed before final native SHA may qualify DB implementation and then require a later current-integration rebind; if the first corrected provider run is deliberately against the exact final native prospective merge, it may bind both axes in the same execution. Package/Contract contain stable evidence predicates only; current receipt IDs/PASS stay external to avoid byte↔receipt cycles.

## Cross-team state at checkpoint

- B15 remains PAUSED, no writer resume through canonical 3681.
- H32/MU10/H33 converge toward Package modifying and Voice no-touch; native path ceiling is review-converged at 20 MODIFY + 54 CREATE = 74 but not writer authority until Voss admits it.
- B16 DAG is approved in principle with external evidence boundaries; native installation is now separately recognized as a quiesced nontransactional replacement problem and does not alter MA17/MA18 read-only authority.
- Current protected effect confinement remains FAIL_NOT_ELIGIBLE under H29/3655.
- Raw coordination chronology remains distinct from admitted assignment currentness; bug `5c4ca43f-d253-4a9f-90c3-dd6d4361ef9e` tracks the unsafe raw-latest projection family.

## Recovery

On a new runtime: read this checkpoint, refresh canonical `public.vera_coordination_events` and relevant Slack channels, resolve MA17/MA18 against any newer Voss state events, and continue only current assignments. Do not infer same-runtime continuity or repeat a full R8A3 installation audit. Keep engineering branch `masa` immutable absent a fresh exact writer stage.
