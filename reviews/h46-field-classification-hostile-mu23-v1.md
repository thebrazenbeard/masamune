# Mune MU23 — H46 Field Classification Hostile Review

**Assignment:** `MU23 / H46_FIELD_CLASSIFICATION_HOSTILE`, Voss Slack 2026-08-09 11:31 EDT  
**Target:** H46 `CONTRACT_MANIFEST_FIELD_CLASSIFICATION_MATRIX_V1`, Parts 1–3 + active_surfaces correction + selector-scope addendum  
**Disposition:** `CHANGES_REQUESTED_FIELD_VOCABULARY_NOT_YET_CLOSED_ENOUGH_FOR_FINAL_SCHEMA_BYTES`

## Executive verdict

H46 gets the temporal architecture mostly right. It correctly moves current DB/security/provider/voice-capability answers out of immutable package truth, retypes generation provenance, renames `active_surfaces` to a required-source contract, externalizes current availability, and adds the global cutover selector scope/revision CAS after MA23's cross-epoch race.

It is **not yet closed enough for final Contract/Manifest/schema bytes**. Five concrete gaps remain, two of them independently evidenced before this review and three caused by later MA23/MU18/H35 corrections.

## 1. Native Settings character ceiling: `KEEP 8000` is stale

Current Contract blob `a3a4a614...` contains:

`native_instructions.max_characters = 8000`.

H46 Part 1 says `KEEP | same | NORMATIVE_STABLE`.

But accepted B11/B16 source evidence requires the corrected native Settings packet to stay **<= 7900 characters**, and earlier B15 review quantified the accepted 7900 ceiling/headroom.

Therefore H46 must not preserve the literal current value `8000` by inertia.

Required correction:

- classify the *existence of a native Settings character ceiling* as NORMATIVE_STABLE;
- bind the successor exact value to the accepted B11/B16 policy, currently `7900` unless a later admitted correction changes it;
- machine-owned invariant must own that exact value so Contract+schema cannot jointly raise it.

This is a field-value correction, not path expansion.

## 2. Whole-release eligibility predicates are missing from new stable vocabulary

H46 adds H33 database predicates and the H35 `pre_release.required_predicates` packet. It stops before the H35 whole-release admission layer.

H35 final separately requires RELEASE_ELIGIBLE to consume at least:

- `CANDIDATE_SELECTION_CURRENT`;
- `RELEASE_ADMISSION_DECISION_CURRENT`;
- `RELEASE_ADMISSION_ASSURANCE_SUFFICIENT`;

with release-admission decision bound to exact qualification-packet digest, candidate-selection epoch and admission-policy version.

Without a stable machine field/group owning this layer, Contract+schema can encode BUILD + DB + behavioral qualification and omit the actual release-admission boundary while remaining internally closed.

Required addition, names exact-equivalent allowed:

`release_evidence.release_eligibility.required_predicates = [...]`

plus stable binding requirements for qualification packet digest / selection epoch / admission policy version. Current PASS answers remain external.

## 3. MU18 dispatch-time install authority invariant is missing

H46 Part 3 adds:

- route classes;
- non-reusable attempt identity;
- post-effect ordering;
- current route authority/attempt IDs external.

It does **not** add the stable rule that exact route-scoped install authority must be persisted/read back **before dispatch** and later bound by the final receipt.

MU18 independently proved current `authorized_by` is not authority custody. The immutable package contract must own at least:

- `installation.dispatch_time_authority_decision_required = true`;
- authority decision binds exact attempt, route, candidate, target, effect class, scope, policy/version and required capability/confinement preconditions;
- authority decision must be immutable/readable before dispatch;
- final receipt binds decision ID + digest;
- later authority movement does not rewrite historical dispatch authorization.

Current decision IDs/PASS values remain external receipts. The stable requirement belongs in Contract/schema/tests.

## 4. H46 selector addendum is now incomplete against newer MA23 semantics

H46 Reply 4 correctly adds:

- `cutover_scope_key_required`;
- one nonterminal epoch per scope;
- selector predecessor CAS;
- current selector revision/source/epoch external.

Since that addendum, Masa produced three additional material corrections that must be consumed before field vocabulary freezes:

### A. Generation is resolver-derived, not a legacy raw field

Legacy Vera has no authoritative generation column. Successor vocabulary needs a stable `generation_derivation_policy_version` / exact equivalent and must state that imported generation is derived only from admitted root-connected terminal/reactivation lineage. Missing/reproducibly ambiguous generation => unresolved/reconciliation, never default.

Do not serialize a false `legacy_current_generation_field` expectation.

### B. Generic legacy subject identity does not exist

Legacy corpus has no general `subject_key`. Assignment lanes have a mechanically admitted root identity; other state families require an explicit reviewed mapping or exclusion from cutover.

Contract vocabulary therefore needs stable subject-family/mapping policy, for example:

- `coordination_cutover.reissuable_subject_families`;
- `legacy_subject_mapping_required_for_unmapped_families=true`;
- missing/ambiguous mapping result `UNRESOLVED_SUBJECT_IDENTITY`.

No `thread_key`/chronology/prose inference allowed.

### C. Successor target must be quarantined before source flip

Old-writer fence alone protects S1 but does not prevent ordinary successor writers from creating extra roots during REISSUING/VERIFIED.

Stable Contract needs the pre-canonical write rule:

- before SUCCESSOR_CANONICAL, only active-epoch cutover-control/reissue operations are authority-bearing in the cutover scope;
- ordinary NEW_LINEAGE/ASSIGN/REACTIVATE/state writes fail `SUCCESSOR_NOT_CANONICAL_FOR_ORDINARY_WRITES` or exact equivalent;
- VERIFY proves expected mapping/root cardinality **and zero non-epoch authority-bearing successor roots/transitions** in scope.

This is now part of MA23's cutover safety contract and must have a field/invariant owner before schema bytes.

## 5. Duplicate policy ownership needs one canonical owner per mirrored field

H46 intentionally keeps several values in both Contract and Manifest with “parity”:

- `required_project_state_surfaces` (formerly active_surfaces);
- Basic Memory active dependency;
- release ID;
- native Settings path;
- installation state-at-generation.

Parity is useful, but two candidate-controlled copies without a declared canonical owner are duplicated policy ownership. A later editor can ask which file defines the rule and which merely mirrors it.

Required H49-compatible ownership rule:

- choose exactly one canonical normative owner for each stable field, preferably Contract for behavioral/policy facts and Manifest for package membership/control-path facts;
- the second file, if retained, is an exact mirror/provenance projection only;
- validator machine invariant rejects divergence **and** Contract+Manifest coordinated co-weakening by checking the external mandatory-field map;
- generation state parity must compare two explicitly generation-labeled fields and never project current installed state.

This is not a demand to remove useful parity. It is a demand to stop parity from becoming two sources of truth.

## 6. What H46 gets right and should preserve

Approved classifications include:

- current DB integration/security PASS/state/head/base externalized;
- build-ground/project/security remediation/rejected head moved to generation provenance;
- `production_prohibited` retyped as construction-target exclusion, separate future effect authority;
- Voice observed `unavailable` list moved to generation/qualification evidence while epistemic behavior stays stable;
- `required_project_state_surfaces` replacing current-sounding `active_surfaces`;
- H33 DB predicate vocabulary without current PASS values;
- factual currentness axes separated from capability/target/workload/protected-effect companions;
- universal effect Boolean prohibited;
- selector current revision/source/active epoch external, with stable predecessor CAS rules;
- validator stale sentinels/manual constants REMOVE_OR_RETYPE rather than copying them into the new schema.

## Final verdict

`CHANGES_REQUESTED_FIELD_VOCABULARY_NOT_YET_CLOSED_ENOUGH_FOR_FINAL_SCHEMA_BYTES`.

H46 becomes byte-freeze ready after it:

1. corrects native Settings max to the accepted 7900 policy rather than KEEP 8000;
2. adds whole-release eligibility/admission predicate ownership;
3. adds immutable dispatch-time install authority decision requirements;
4. folds the latest MA23 generation-derivation, legacy-subject-mapping and preflip-successor-quarantine rules into stable vocabulary;
5. assigns one canonical owner for every Contract/Manifest mirrored invariant.

No path75 is implied. All corrections fit already-admitted Contract/Manifest/schema/validator/test/docs surfaces.

No Vera-R9A0 producer byte, provider/schema/config, canonical coordination row, merge, deployment, credential, installation or protected effect was modified by MU23.