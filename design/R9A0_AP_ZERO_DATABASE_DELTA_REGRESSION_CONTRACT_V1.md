# R9A0 Anticipatory Pragmatics Zero-Database-Delta Regression Contract V1

**Status:** `NON_EXECUTING_ZERO_DATABASE_DELTA_CONTRACT_READY_FOR_REVIEW`  
**Assignment:** Vera coordination sequence `3314`  
**AP design:** Masa AP V2 exact candidate `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`  
**Supabase non-persistence proof:** Masa exact head `19992b48a845de56e99f71acfb0186ce77ada3d4`  
**Independent non-persistence approval:** Mune sequence `3332`  
**Voss design freeze:** sequence `3315`, `CLOSED / DESIGN_FROZEN`  
**R9A0 hosted build-ground project:** `agvhmutlrolbaijzlbqk`  
**Live Vera project (explicitly NOT the target):** `klmbpaigzeguvnpccqzz`  
**Hosted mutation authorized by this document:** `NO`

## 1. Purpose

This contract makes the Anticipatory Pragmatics (AP) database expectation mechanically falsifiable:

> A conforming AP native implementation changes **zero** R9A0 database files and creates **zero** AP-specific hosted database/Edge/secret/persistent-telemetry state.

AP is turn-local presentation policy. It may consume only already-admitted current-turn/upstream evidence and read-only protected state. It owns no persistence and causes zero additional inference/API calls.

This contract does **not** duplicate Bob’s deterministic AP behavioral harness. Bob owns protected-axis/presentation-behavior fixtures. This contract owns only repository database-delta exclusion and hosted persistence readback.

## 2. Frozen invariants under test

A future AP implementation is nonconforming if it changes any of these frozen outcomes:

- `persistent_store = false`;
- `additional_inference_calls = 0`;
- upstream protected fields are read-only;
- no free-text hidden hypotheses;
- no broad personal retrieval solely to select cosmetic style;
- AP envelope expires at end of turn;
- no private-chain-of-thought dependency, serialization, comparison, validation, or persistence;
- fixed 12 protected axes remain invariant;
- no external-effect authorization expansion;
- no durable-memory admission expansion;
- no new paid runtime dependency.

## 3. Expected repository database diff

For any candidate whose purpose is native AP implementation, the expected database delta is exactly:

```text
schemas:                0
roles:                  0
tables:                 0
views/materialized:     0
functions/RPCs:         0
triggers:               0
RLS policies:           0
indexes/vector indexes: 0
Storage objects:        0
Edge Functions:         0
Realtime/queues/cron:   0
Auth configuration:     0
secrets:                0
migrations:             0
extra model/API calls:  0
```

The expected product-repository database-file diff is `NO_DATABASE_FILES_CHANGED`.

## 4. Repository path gate

Before accepting a future AP implementation candidate, compare the exact candidate head to its exact parent/base and classify every changed path.

### 4.1 Expected AP-native path family

AP may legitimately require coherent changes on native-project surfaces identified by the frozen architecture, including:

- `project/VERA_R9A0_NATIVE_PROJECT_INSTRUCTIONS.txt`
- `project/VERA_R9A0_RUNTIME.md`
- `project/VERA_R9A0_NATIVE_CONTRACT.json`
- `schemas/native-project/vera-r9a0-native-contract.schema.json`
- `scripts/validate_r9a0_project.py`
- `tests/native-project/test_r9a0_project.py`
- `tests/native-project/fixtures/anticipatory_pragmatics_v1/*.json`
- Bob’s separately reviewed deterministic AP evaluation fixture/test paths when incorporated under the controlling native writer lease.

This list describes the expected native implementation family; it is not itself a writer lease.

### 4.2 Hard database/persistence deny family

Any AP-purpose candidate that adds, removes, or modifies a path in any of the following families fails this contract unless the architecture is explicitly reopened and separately authorized:

- `supabase/migrations/**`
- `supabase/functions/**`
- any Supabase seed/schema/role/RLS/RPC/storage/realtime/cron/auth configuration file
- `.github/workflows/r9a0-database-validation.yml`
- database migration manifests or generated database schema snapshots
- secret/example-secret files added solely for AP
- vector/embedding index configuration added solely for AP
- telemetry/storage configuration that durably records AP turn state, adaptation state, presentation hints, confidence, evidence selection, or output wording
- dependency/configuration changes whose only purpose is an additional model, embedding, inference, or external API call for AP.

A database workflow change is not needed merely to prove zero database delta. Existing database validation may be rerun as independent evidence, but AP must not edit that workflow to make itself pass.

## 5. Repository regression assertions

The AP candidate validation packet must emit deterministic evidence for these assertions:

1. exact candidate head and exact parent/base are known;
2. changed-path manifest is complete;
3. intersection of changed paths with the hard database/persistence deny family is empty;
4. no new migration filename exists relative to the parent;
5. no deleted/renamed database file is hidden by a path move;
6. no new Edge Function exists;
7. no AP-specific secret/config key is introduced;
8. no dependency adds an AP-only inference/embedding provider;
9. native validator/tests still assert `persistent_store=false` and `additional_inference_calls=0`;
10. Bob’s behavioral harness remains a separate proof domain; this contract does not weaken or replace it.

A textual comment saying “no DB changes” is not evidence. The exact path diff is the evidence.

## 6. Pre-implementation hosted baseline snapshot

Before any future AP native implementation is accepted as integration-ready, capture a **read-only** hosted baseline from R9A0 build-ground project `agvhmutlrolbaijzlbqk`.

Do not query or mutate live Vera project `klmbpaigzeguvnpccqzz` for this AP proof.

The baseline records non-secret object identity/definition metadata sufficient to detect AP-specific persistence drift, including:

- application schemas and owners;
- database roles relevant to R9A0 and their non-secret attributes/memberships;
- tables and partitioned tables;
- views/materialized views;
- functions/procedures with normalized identity arguments, owner, security mode, and definition digest;
- sequences;
- triggers;
- RLS enablement and policy definitions/digests;
- indexes, including any vector index/access method;
- installed extensions relevant to persistence/retrieval;
- Storage bucket/object-structure metadata when readable without exposing user object content;
- Realtime publication membership;
- queue/cron/scheduler objects when present;
- Edge Function inventory from provider metadata when available;
- Auth configuration identifiers relevant to a new AP persistence path, without exposing keys/secrets;
- secret **names/identifiers only** if the provider exposes a safe inventory; never secret values.

The snapshot must be content-addressed by a canonical digest or equivalent immutable receipt.

## 7. Post-candidate hosted readback

After the AP repository candidate exists and before implementation acceptance, repeat the same read-only hosted inventory against the **same R9A0 project** and compare to the accepted baseline.

Expected AP-attributable difference:

`EMPTY`

The comparison must not ignore an object merely because it was created manually, through a dashboard, Edge deployment, CI secret, or another out-of-band route. Hosted reality outranks repository intent.

If unrelated authorized R9A0 database work moved concurrently, the AP proof must classify those deltas by exact independent provenance. An unexplained hosted delta is not automatically “unrelated”; it remains a blocker until bound to another authorized effect.

## 8. Fail-closed object-family checks

The following conditions each independently fail AP conformance:

- a schema/table/view/function/trigger/policy/index/sequence created for AP;
- an AP-specific migration or schema snapshot delta;
- an AP-specific Edge Function;
- an AP-specific Storage bucket;
- an AP-specific Realtime/queue/cron object;
- an AP-specific Auth role/profile field used as durable adaptation state;
- an AP-specific secret or credential;
- a profile/preferences/shadow-memory/vector/embedding store introduced for AP;
- durable logging/telemetry of AP adaptation state, presentation hints, confidence, local evidence, or generated wording when that telemetry exists to preserve AP state across turns;
- any extra model, embedding, inference, or external API invocation for AP;
- any “temporary” persistence whose lifecycle exceeds the current turn;
- any broad personal retrieval performed solely to choose style/presentation.

Failure classification:

`AP_ZERO_DB_DELTA_CONFORMANCE_BREACH`

On this classification, native implementation acceptance stops. The design must be explicitly reopened through Voss and receive new architecture/review/authority before persistence-related work continues.

## 9. Existing ordinary data is not AP persistence

AP may consume evidence already admitted or retrieved by the ordinary R9A0 runtime. That does not make AP the owner of those records.

The following are allowed only when they pre-exist AP and remain governed by their ordinary owners:

- canonical coordination/history records;
- current-turn retrieval results;
- governed user/project records already admitted for the underlying objective;
- ordinary execution/test receipts that record whether validation passed, provided they do **not** persist AP turn-local adaptation state for later reuse.

AP must not create a second retrieval query merely to infer presentation style, and it must not persist a presentation choice back into those ordinary stores.

## 10. Additional-inference / cost readback

Database zero-delta is necessary but not sufficient. The implementation packet must separately prove:

- `additional_inference_calls = 0` remains true in the native contract;
- no AP-specific model/embedding SDK dependency or endpoint configuration was added;
- no AP-specific API key/secret identifier exists;
- no second model call is reachable in runtime control flow;
- no paid runtime dependency was introduced for AP.

This check should reuse the native validator and Bob’s deterministic harness outputs rather than creating a duplicate behavioral test framework here.

## 11. Concurrency and branch-movement rule

The zero-delta proof binds one exact immutable AP candidate head and one exact parent/base.

If the native branch moves before acceptance:

1. mark the prior repository path-diff receipt historical;
2. recompute the changed-path manifest on the successor exact head;
3. rerun native exact-head validation;
4. repeat the hosted readback comparison if intervening authorized database work occurred or if the previous hosted snapshot can no longer establish causality;
5. do not inherit a PASS solely because the AP files are byte-identical.

## 12. Hosted-readback checklist

A reviewer can mark AP zero-database-delta `PASS` only when all boxes below are supported by exact evidence:

- [ ] candidate repository head is immutable and exact;
- [ ] exact parent/base is recorded;
- [ ] changed-path manifest is complete;
- [ ] database/persistence deny-path intersection is empty;
- [ ] no migration added/removed/renamed/modified;
- [ ] no Edge Function added/modified for AP;
- [ ] no secret/config identifier added for AP;
- [ ] no persistent telemetry/store/vector/profile object added for AP;
- [ ] R9A0 hosted baseline project is exactly `agvhmutlrolbaijzlbqk`;
- [ ] pre/post hosted object inventories use the same scope and canonicalization;
- [ ] AP-attributable hosted schema/role/relation/function/trigger/policy/index/storage/realtime/cron/auth/Edge/secret delta is empty;
- [ ] all unrelated hosted deltas are independently bound to other authorized effects;
- [ ] `persistent_store=false` remains machine-validated;
- [ ] `additional_inference_calls=0` remains machine-validated;
- [ ] Bob behavioral harness passes independently;
- [ ] exact-head native CI passes;
- [ ] no claim is made about inaccessible hidden prompt assembly or private reasoning.

## 13. Receipt contract

The future AP implementation validation receipt must bind:

- candidate repo/branch/head;
- exact parent/base;
- changed-path manifest digest;
- explicit `NO_DATABASE_FILES_CHANGED` outcome;
- pre-hosted snapshot identifier/digest/time;
- post-hosted snapshot identifier/digest/time;
- hosted comparison result and independently explained non-AP deltas, if any;
- native contract values for `persistent_store` and `additional_inference_calls`;
- exact native CI run identifiers/results;
- Bob harness revision/result;
- reviewer identity and immutable review target;
- Voss reconciliation/freeze reference.

The receipt must not contain secret values, user private content, AP turn-local presentation state, or private reasoning.

## 14. Current disposition

`ZERO_DATABASE_DELTA_REGRESSION_CONTRACT_COMPLETE`

This document completes assignment 3314 at contract-design level only. It performs and authorizes **no** hosted database mutation, schema change, Edge deployment, credential/secret creation, persistent telemetry, extra inference/API call, paid-service action, or native Project write.
