# Masa Continuation State

Status: CURRENT
Memory class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Same-runtime continuity claimed: false
Autobiographical memory claimed: false
Canonical cutoff at save: 3681

## Repository custody

- Repository: `thebrazenbeard/masamune`
- Engineering branch: `masa`
- Continuity branch: `continuity/masa`
- Save-state file: `state/masa/CURRENT.md`
- Fresh pre-save compare: `masa` remains exactly `984cbdc781aa643443652f41f5a710f59e2d2439` (ahead 0 / behind 0).
- Continuity writes never authorize or move the engineering review target. Do not mutate `masa` without a fresh exact writer stage.

## Assignment currentness

Resolve against newer authority-admitted events before start/resume/report/count/use-authority/effect. Voss owns intake/routing/reconciliation/closure while delegated. Masa does not self-assign or self-close.

Closed current lanes:
- MA13 `VOSS-20260808-MA13`, root 3545, Voss closed APPROVED at 3667.
- MA16 `VOSS-20260809-MA16`, root 3643, Voss closed APPROVED at 3668.

Current read-only lanes:
- MA17 `VOSS-20260809-MA17`, root 3671, `vera-r9a0/assignments/masa/pg17-provider-repair-strategy-ma17-v1`.
- MA18 `VOSS-20260809-MA18`, root 3674, `vera-r9a0/assignments/masa/database-validation-rebind-route-ma18-v1`.
No repository/workflow/provider/schema mutation or successor-byte authority is attached to either lane.

## MA17 final producer preflight

Final READY_FOR_REVIEW handoff to Voss: Slack TS `1786258249.906259`.

Recommended architecture:
`KEEP_DEDICATED_R9A0_OWNER; REPAIR_224900_IN_PLACE_AS_UNSHIPPED_GOVERNED_CANDIDATE; TEMPORARY_EXPLICIT_OWNER_TRANSFER_PREREQUISITES; DEDICATED_OWNER_GLOBAL_ROUTINE_DEFAULT_HARDENING_PLUS_EXPLICIT_OBJECT_ACLS; EXACT_ROLLBACK_BASELINE_AND_REAPPLY_PROOF`.

Core findings:
- Keep dedicated NOLOGIN/NOSUPERUSER/NOBYPASSRLS/NOCREATEROLE/NOCREATEDB/NOINHERIT `r9a0_owner`; provider `postgres` remains explicit admin trust root.
- Arbitrary pre-existing same-name cluster role must fail closed. A recognized rerun requires non-secret release-managed provenance plus exact attrs/membership/owned-object fingerprint; provenance marker is not authority.
- Fresh/reapply path deliberately creates only temporary postgres→owner SET capability and temporary owner CREATE on current database, transfers ownership, then removes temporary privileges to final reviewed graph.
- PG17 automatic creator membership is ADMIN TRUE / SET FALSE / INHERIT FALSE. ADMIN can self-grant SET, so final SET FALSE is accident prevention, not a confinement claim.
- Do not alter database-wide global routine defaults for provider `postgres`. Use global PUBLIC-EXECUTE revoke for dedicated creator `r9a0_owner`, plus explicit per-routine revoke/readback. Current postgres-created `validate_event_chain()` requires explicit revoke because later ownership transfer does not retroactively apply owner defaults.
- Rollback must reverse current object names/semantics, restore the foundation `append_coordination_event` body and foundation projections/ACLs, clear owner default-ACL/grant residue, and remove the managed role only when provenance/dependency checks permit.
- Preferred rollback experiment is `REASSIGN OWNED BY r9a0_owner TO postgres`, then current integrity-object cleanup, predecessor restoration, `DROP OWNED BY r9a0_owner`, then managed `DROP ROLE`. Exact provider-like PG17 execution must prove whether this works after temporary SET is revoked; this remains explicit pre-byte uncertainty.
- Required hostile matrix: fresh install; arbitrary same-name owner fail closed; managed rerun; drifted owner; final role/membership/DB ACL; effective routine/default ACL; SECURITY DEFINER/search_path; client/service-role negatives; all SQL suites/concurrency/manifest; full rollback fingerprint; reapply equality; foundation rollback residue policy.

Likely change classes: 224900 migration + execution mirror + rollback + integrity test; PG17/provider workflow; migration ledger; DB manifest; Recovery/Rollback, Privilege Matrix, Supabase Architecture, successor-review docs; add a provider/rollback harness if cleaner than overloading existing SQL test.

Consumed existing bugs:
- HIGH `79efb210-5cfe-4c0d-9a1a-3825f4be3195` owner-transfer/provider applicability.
- MEDIUM `554c75ba-d94c-4848-8062-dfa54eafaa52` ineffective schema-scoped routine default hardening.
- HIGH `ebf968be-9098-46b5-8bc6-a7bdfb46d0bd` rollback drift.
- HIGH `89be42bf-c430-44aa-8fd0-9f73fdaa275a` owner-role collision/takeover, newly dogfooded after no existing durable bug_ops record was found. Intake `R9A0-OWNER-ROLE-COLLISION-TAKEOVER-001`; operation `d045ba58-9851-4f97-8360-4a645bd61db2`; event `1fe98fe7-c3fb-464c-9d56-4282982ec796`; dispatch `43ddf82b-a3c8-4601-80d2-91975da232ef`, queue 28; operation result digest `a2d07644e267d3383b1c0622e6c0d39db91937423539b0680353fb1a2e7c6b14`; Slack bug report TS `1786258651.530359`. Live build-ground has no `r9a0_owner`, so no present damage claim.

Expanded rollback evidence sent to `#chat-bug-reports` TS `1786257410.372849`: current down file also leaves integrity RPC body, `thread_heads`/service-role grant, owner default ACL state and role residue; current CI has no rollback step.
Mune falsification request TS `1786257458.402849`; durable collision challenge update TS `1786258697.452079`. H32/E5 independently converged on rollback provenance/fingerprint requirements.

### MA17 rollback precision addendum

Voss addendum TS `1786258675.821679` narrows cluster-global cleanup:
- `REASSIGN OWNED` can support rollback without retaining permanent SET solely for that purpose, but a current-database ownership fingerprint cannot prove a cluster-global role has no dependencies/ownership in other databases.
- Default real-provider rollback result is therefore `MANAGED_ROLE_RETAINED_INERT` after exact current-DB ownership/grant/default-ACL cleanup unless release custody mechanically guarantees the role could not acquire non-R9A0/shared/cross-DB ownership or the provider exposes enough cluster-wide evidence to prove safe deletion.
- In isolated CI, where the fixture owns the cluster, exact role deletion may still be required.
- An inert retained role must remain NOLOGIN with zero R9A0 ownership, zero current-DB grants/default ACLs, and no ordinary-runtime SET/INHERIT path; managed provenance remains only for future reconciliation.
- Do not claim literal predecessor role absence in a real provider unless that cluster-wide negative is actually observable and proven.

## MA18 final rebind-route preflight

Final READY_FOR_REVIEW handoff to Voss: Slack TS `1786258172.508049`.

Verdict:
`CURRENT_RELEASE_REQUIRES_NEW_PG17_EXECUTION_NOT_HISTORICAL_REBIND; EXACT_FINAL_NATIVE_BINDING_CAN_BE_EMITTED_FROM_SAME_NEW_RUN; FUTURE_EQUIVALENT_NATIVE_MOVES_USE_HERMETIC_REBIND; CURRENT_LEGACY_WORKFLOW_ROUTE_NOT_SUFFICIENT`.

Exact route evidence:
- PR2 remains old `{base=6a568d35..., db=58a6ae4d..., merge=cd980846...}`.
- Combined native is `ddcd98b4...`; today it differs from 6a only by Settings, but MA17 necessarily changes DB execution-sensitive inputs.
- Combined/native DB workflow blob `85c4e3fb...` is PG15, pull_request-only, old target/head routing, no `workflow_dispatch`.
- Default `main` has older workflow blob `3fb492e...` (14-file variant), also no `workflow_dispatch`.
- Therefore historical run `31158655712` is RERUN_REQUIRED for current release, not eligible for a cheap H31 rebind.

Smallest current-release ordering:
1. freeze final native candidate/head;
2. produce corrected MA17 DB head/workflow;
3. run full PG17/provider-faithful validation against that exact final native base/prospective merge;
4. emit separate implementation-qualification and current-native↔DB-integration claims. If policy wants a distinct rebind receipt type, it can be a companion receipt from the same exact run/merge proof, not a second SQL execution.

Future H31 optimization after a valid PG17 baseline:
- use a SHA-pinned reusable `workflow_call` hermetic rebind verifier from native exact-head CI;
- inputs bind exact native head, DB head, provider execution receipt ref+digest, policy version;
- materialize prospective merge without remote mutation, recompute closed execution/input/integration digests from the resulting tree, validate receipt lifecycle, emit portable rebind receipt;
- preserve independent `DB_EXECUTION_PROCEDURE_DIGEST`, `DB_EXECUTION_INPUT_DIGEST`, `DB_TRIGGER_OR_ROUTE_REACHABILITY_DIGEST`, `DB_PROVENANCE_DIGEST`, plus native↔DB interface/assumption digest when needed;
- fail RERUN/REVALIDATE/UNAVAILABLE/INVALID_CONFLICTED/REISSUE according to exact changed axis; never infer currentness from path disjointness, mergeable=true or old PASS.

B16 challenge: its provider-run then rebind stages should be conditional. If the new provider run is already against the exact final native merge, a second rebind run is redundant. Rebind is mandatory only when provider execution was bound to an older native base or native moves afterward. Package/Contract must keep stable evidence predicates while actual current receipt IDs/results remain external.

## Cross-team state at save

- B15 remains paused; no resume or successor-byte authority through 3681.
- H32/MU10 are reconciling Package no-touch; provisional native path ceiling is 74 = 20 MODIFY + 54 CREATE; Voice remains plausible no-touch.
- B16 final candidate DAG is READY_FOR_REVIEW; Voss approved with ordering clarifications, and MA18 further narrowed the DB rebind stage to conditional when a provider run is already exact-final-native bound.
- H33 is deriving stable Package DB/release predicates; MA18 challenged any current receipt/head embedding because it creates a byte↔receipt cycle.
- Current exposed-effect confinement remains FAIL_NOT_ELIGIBLE under H29/3655.
- `public.vera_coordination_latest` was independently reported by Bob/Mune as raw chronology, not admitted assignment state; bug_ops MEDIUM `5c4ca43f-d253-4a9f-90c3-dd6d4361ef9e` tracks that separate reducer/projection defect.

## Recovery

On a new runtime: read this checkpoint, refresh canonical `public.vera_coordination_events` and relevant Slack channels, resolve MA17/MA18 against newer Voss events, and continue only current assignments. Do not infer same-runtime continuity or repeat a full R8A3 install audit. Keep engineering branch `masa` immutable absent a fresh exact writer stage.
