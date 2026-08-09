# Mune MU11 — H35 V3 Install-Machine Hostile Review

**Assignment:** provisional `MU11 / H35_V3_INSTALL_MACHINE_HOSTILE_REVIEW` from Voss Slack 2026-08-09 09:14 EDT  
**Canonical H35 basis:** sequence `3699`, `R9A0_RELEASE_EVIDENCE_COMBINER_V2`  
**Candidate native basis:** `ddcd98b4e61df09f06886f2073ecbdfad21c8f12`  
**Class:** read-only architecture falsification  
**Disposition:** `READY_FOR_REVIEW / H35_V2_DIRECTION_SOUND_WITH_V3_MACHINE_BINDING_REQUIREMENTS`  
**Mutation performed:** no provider/schema/installation/producer mutation

## Executive verdict

H35 sequence 3699 has the correct high-level separation: build validity, database release gate, pre-release qualification, release admission, route-scoped install eligibility, post-effect installation evidence, installed-artifact historical truth, current installed qualification, and future protected-effect eligibility are not one ceremonial PASS.

The next machine contract should preserve that structure but make four currently prose-level boundaries mechanically closed:

1. one stable **install-attempt identity** across every post-dispatch subordinate receipt;
2. a closed/versioned **qualification-environment composite** with dependency-scoped drift semantics;
3. fixed **route class per attempt** so user-manual and assistant/tool authority cannot be laundered across one install history;
4. an explicit acyclic phase split where isolated qualification is pre-release and **in-situ qualification is post-install only**.

Two existing TRIAGED MEDIUM bugs already cover the concrete current-byte failures:

- `0fd06067-d13b-4868-967a-e5a8a5918b56`: installation evidence lacks stable attempt identity and can mix overlapping attempts;
- `9cbc732c-e272-46bb-8fb8-9846a28f77df`: completed-receipt/cold-start dependency cycle.

No duplicate bug is warranted by MU11.

## 1. Independent exact-byte verification

Exact candidate receipt template blob `2b8be7afc2816f7fa9547ef28cc95a4d2bebd260` has no install-attempt identity, no route class, and no parent step identity. It contains aggregate booleans such as `cold_start_readback_passed` and `project_settings_replaced`, which can be populated from evidence produced by different attempts unless the successor schema adds a shared attempt key.

Exact Cold Start blob `4c3a14e6fd651086dc1a8dff159c3255233a8074` says to resolve installation state from the completed receipt before emitting the cold-start receipt.

Exact Post-Install blob `64337aaa8651219f9e897129b66522e0277bff06` requires the final installation receipt to read back successfully before `INSTALLED_VERIFIED`.

That reproduces the known cycle in the current bytes. H35 3699 correctly repairs the direction to:

`INSTALL_BASE_OUTCOME_READBACK -> COLD_START_RUNTIME_READBACK + POST_INSTALL_ENVIRONMENT_CHECK -> IN_SITU_PROJECT_QUALIFICATION_CURRENT -> FINAL_INSTALL_RECEIPT -> FINAL_INSTALL_RECEIPT_READBACK`

The next machine contract must encode this as a dependency rule, not merely repeat the arrow in prose.

## 2. Stable install-attempt identity is the spine

Define a closed `INSTALL_ATTEMPT_V1` identity before any install effect is dispatched.

Minimum identity-bearing fields:

- `install_attempt_id` — opaque stable identifier minted once before dispatch;
- exact candidate/release identity and candidate digest;
- exact target Project/configuration identity;
- `route_class = ASSISTANT_TOOL | USER_MANUAL` for V1;
- exact install precondition digest;
- authority evidence locator/digest appropriate to the route;
- attempt-state policy version;
- creation/observation cut.

Every subordinate post-dispatch record must bind the same `install_attempt_id` and candidate/target/route identity:

- transition-in-progress record;
- dispatch/effect observation where applicable;
- install base outcome readback;
- cold-start runtime readback;
- post-install environment check;
- in-situ Project qualification;
- final installation receipt;
- final receipt persistence/readback confirmation;
- recovery/reconciliation record if the attempt fails or remains ambiguous.

Subordinate steps may have their own operation/receipt IDs, but those IDs are children of the one attempt. They are not substitutes for it.

### Hostile A — overlapping attempts

Attempt `A` is dispatched and outcome is unknown. A second attempt `B` against the same target/candidate begins before `A` is reconciled.

Expected result: `B` is blocked. No receipt from `A` may satisfy a dependency of `B`, and vice versa. A shared candidate SHA does not establish shared attempt identity.

### Hostile B — cross-route overlap

Assistant/tool attempt `A` becomes ambiguous; a user manually starts the same installation as attempt `B`.

Expected result: unresolved `A` still quarantines the target. Manual authority for `B` cannot retroactively settle `A`, and H29 failure for `A` cannot be bypassed by attaching `B`'s manual evidence to the same attempt history.

### Hostile C — retry after ambiguous outcome

A caller retries the install effect because dispatch acknowledgement was lost.

Expected result: reconcile/read back attempt `A` first. Blindly minting `B` or replaying destructive native steps is prohibited. If an individual provider operation has its own safe idempotency token, its exact replay may occur only under parent attempt `A` and only under that operation's retry contract.

### Hostile D — identity mutation

Same `install_attempt_id` reappears with changed route, candidate, target, or install-precondition digest.

Expected result: `INVALID_CONFLICTED`, never “updated attempt.” Attempt identity is immutable.

## 3. Route class is fixed per attempt

H35 correctly distinguishes assistant/tool installation from user-manual installation. V3 should make the route a closed field on `INSTALL_ATTEMPT_V1`.

### `ASSISTANT_TOOL`

Requires at dispatch time:

- `RELEASE_ELIGIBLE` for the exact candidate;
- exact target/preconditions current;
- current assistant/tool install authority and capability;
- current H29 INSTALL-class confinement/retry/instruction-nonauthority/egress requirements as applicable;
- quarantine clear and no unresolved prior attempt.

### `USER_MANUAL`

Requires:

- `RELEASE_ELIGIBLE` for the exact candidate;
- exact target/preconditions current;
- exact current user authority for the manual action;
- quarantine clear and no unresolved prior attempt.

H29 is not automatically a universal gate over a native user action outside the audited assistant/tool surface. The assistant may observe and validate evidence afterward but may not claim it executed the manual effect.

### Route-switch hostile

An assistant/tool attempt is partially executed and then the user takes over manually.

V1 expected result: reconcile/terminate the first attempt, then mint a new manual attempt. Do not mutate `route_class` mid-attempt. If a future composite route is genuinely needed, admit a third explicit route class with its own authority composition instead of silently blending two routes.

## 4. Qualification environment must be a closed/versioned composite

H35 3699 correctly binds qualification to environment/model/settings/source/tool evidence, but V3 should replace an open-ended bundle of locators with a closed typed composite.

Recommended `QUALIFICATION_ENVIRONMENT_V1` core:

- `environment_class = PRE_RELEASE_ISOLATED | POST_INSTALL_IN_SITU`;
- exact candidate identity;
- exact target/project identity where applicable;
- model identity + mode as observed for that qualification run;
- Project Settings digest;
- active logical source-set digest;
- tool/plugin registry digest and the capability/permission subset actually consumed;
- provider/database environment digest for provider-dependent qualification;
- policy/canonicalizer/test-suite versions;
- required external-source snapshot/cut identities;
- evidence-completeness state;
- observation time/cut;
- `dependency_mask_version` describing which fields actually stale the qualification result.

The composite is evidence, not package authority. Current facts remain current only while their dependency-bound sources remain current.

## 5. Pre-release isolated qualification and post-install in-situ qualification are different nodes

The correct ordering is:

`BUILT_AND_VALIDATED + DATABASE_RELEASE_GATE + ISOLATED_BEHAVIORAL_QUALIFICATION_CURRENT + other pre-release evidence -> PRE_RELEASE_QUALIFICATION_PACKET -> RELEASE_ELIGIBLE`

Then, only after an installation effect and exact base outcome:

`INSTALL_BASE_OUTCOME_READBACK -> FRESH_COLD_START_RUNTIME + POST_INSTALL_ENVIRONMENT_CHECK -> IN_SITU_PROJECT_QUALIFICATION_CURRENT`

`RELEASE_ELIGIBLE` must never depend on `IN_SITU_PROJECT_QUALIFICATION_CURRENT`; that would require the release to be installed before it could become eligible to install.

Conversely, isolated behavioral qualification cannot substitute for in-situ qualification because the actual active Project files, Settings, model/runtime/tool surface, and installation state are different evidence.

## 6. No final-receipt self-dependency

Final receipt dependencies must be one-way:

`ATTEMPT + BASE_OUTCOME + COLD_START + POST_INSTALL_ENV + IN_SITU_QUALIFICATION -> FINAL_INSTALL_RECEIPT -> FINAL_INSTALL_RECEIPT_READBACK`

Forbidden edges include:

- cold-start requires completed final receipt;
- post-install environment requires final receipt;
- in-situ qualification requires final receipt;
- final receipt contains a requirement that its own final readback already succeeded;
- final receipt readback is used to generate the receipt it is supposed to confirm.

`FINAL_INSTALL_RECEIPT_READBACK` is a postcondition. Historical installed-artifact identity may be projected only after that postcondition passes.

## 7. Bounded volatile-source drift matrix

Drift must stale only evidence that actually depends on the changed source.

### Before release admission

If a field inside the pre-release qualification dependency mask moves, the affected qualification node becomes `REVALIDATE_REQUIRED` or `RERUN_REQUIRED`; `BUILT_AND_VALIDATED` remains true for unchanged bytes.

Example: model/runtime change affecting behavioral qualification stales that qualification. A GitHub branch tip moving away from an exact selected immutable candidate does not automatically stale the candidate unless selection policy says so.

### After release eligibility but before install dispatch

Install-route authority/tool capability/target drift re-evaluates `INSTALL_ACTION_ELIGIBLE`; it need not falsify candidate release eligibility unless the moved fact was also an input to release admission.

### After base outcome but before in-situ qualification

A model/tool/Settings/source change in the installed environment invalidates the affected post-install evidence and requires fresh cold-start/post-install/in-situ qualification. Reinstallation is required only if the active installed source/config identity itself no longer matches the intended base.

### After final receipt readback

Later environment/model/tool drift does not erase `INSTALLED_ARTIFACT_IDENTITY_VERIFIED`. It may make `INSTALLED_VERIFIED_CURRENT` or `CURRENT_PROTECTED_EFFECT_ELIGIBILITY` stale/blocked.

This is the same temporal discipline used elsewhere in R9A0: immutable historical fact survives; current eligibility is recomputed from current dependencies.

## 8. Minimal hostile acceptance matrix

1. two overlapping attempts, same route -> second blocked;
2. overlapping manual/tool attempts -> second blocked, no evidence mixing;
3. ambiguous attempt then blind retry -> blocked pending reconciliation;
4. same attempt ID with changed candidate/target/route/preconditions -> conflict;
5. base outcome from attempt A + cold start from attempt B -> invalid evidence chain;
6. final receipt referenced by its own prerequisite -> dependency cycle / invalid graph;
7. in-situ qualification placed before install -> invalid phase dependency;
8. manual evidence used to satisfy assistant H29 gate -> invalid route composition;
9. assistant evidence used to claim manual user action executed -> invalid effect attribution;
10. pre-release model/tool drift inside dependency mask -> affected qualification stale only;
11. post-install model/tool drift after immutable artifact readback -> current qualification stale, historical installed identity preserved;
12. exact source/config drift after base readback -> quarantine/recovery until new base outcome is established.

## Final recommendation

Preserve H35's 3699 semantic decomposition. V3 should freeze the machine contract around these additional invariants:

`ONE_INSTALL_ATTEMPT_ID -> FIXED_ROUTE -> ACYCLIC_POST_EFFECT_RECEIPTS -> CLOSED_VERSIONED_QUALIFICATION_ENVIRONMENT -> DEPENDENCY_SCOPED_DRIFT`

This is a refinement, not a redesign of H35. The current candidate bytes still exhibit the already-reported attempt-mixing and receipt-cycle failures; H35 V2 provides the correct conceptual repair but the successor machine schema must make those repair properties mechanically testable.

No repository producer bytes, provider state, schema, Project Settings, credentials, installation state, deployment state, or canonical coordination state were modified by MU11.
