# Mune MU21 V2 — Startup Trust Predicate Correction

**Corrects:** `reviews/startup-trust-regression-hostile-mu21-v1.md` only on verification-predicate decomposition  
**Trigger:** independent H47 refinement observed after MU21 V1  
**Disposition:** `APPROVED_TWO_PREDICATE_STARTUP_TRUST_CONTRACT`

## Correction

MU21 V1 incorrectly placed `EXPLICIT_BUILD_RELEASE_VALIDATOR_ROUTE` inside one broad `FULL_RELEASE_VERIFICATION_TRIGGERED` set whose description included deployed Settings/readback/cold-start ceremony. That conflates two evidence domains.

Replace the V1 T1–T5 umbrella with **two disjoint predicates**.

## A. `PACKAGE_BUILD_VALIDATION_TRIGGER`

Exactly:

`EXPLICIT_BUILD_RELEASE_VALIDATOR_ROUTE`

This route evaluates an immutable repository/package candidate and may require:

- exact logical candidate file set;
- manifest membership;
- Contract/schema validation;
- checksums/digests;
- static/native Settings payload validation;
- deterministic tests;
- exact-head CI/readback evidence according to release policy.

It does **not** by itself require or establish:

- deployed Project file-set readback;
- deployed Project Settings readback;
- install attempt/outcome;
- cold-start runtime readback;
- post-install environment/in-situ qualification;
- final installation receipt/readback;
- current installed release state.

A build PASS proves candidate/build evidence only.

## B. `INSTALLATION_INTEGRITY_VERIFICATION_TRIGGER`

Exactly one of:

1. `CURRENT_INSTALL_OR_REPLACEMENT`;
2. `EXPLICIT_INSTALL_OR_INTEGRITY_AUDIT` of the active/deployed Project;
3. `FORMAL_INSTALLED_STATE_CLAIM` requiring installed-state evidence;
4. `ACTUAL_ACTIVE_CONTENT_INTEGRITY_CONTRADICTION`.

This route may consume exact deployed logical files, deployed Settings, checksum/content mapping, duplicate/mixed-release evidence, H35 install-attempt/base-outcome/cold-start/post-install/in-situ/final-receipt evidence as appropriate to the requested claim or recovery decision.

It does not require rebuilding/re-running candidate CI merely because installation integrity is being checked, unless the exact install policy explicitly requires fresh candidate-build evidence and that evidence is stale/unavailable.

## C. Non-triggers

`NEW_CHAT` and `NEW_RUNTIME` alone trigger neither A nor B.

Ordinary project orientation therefore remains:

- active platform-supplied files operational immediately;
- task-relevant governing/state refresh only;
- no full candidate-build validation;
- no deployed installation audit;
- no cold-start installation ceremony.

## D. Domain-sensitive contradiction

V1's generic `ACTUAL_CONTENT_INTEGRITY_CONTRADICTION` must be scoped by evidence domain:

- contradiction in a repository/package candidate while building/releasing -> build validation failure/reconciliation under predicate A;
- contradiction in the active Project/deployed release -> installation/integrity verification/recovery under predicate B.

One does not automatically activate the other.

Example: a repository checksum mismatch does not prove the currently installed Project is corrupted. A deployed suffix/content mismatch does not prove a different repository candidate failed CI.

## E. Suffix rule unchanged

The filename correction from MU21 V1 remains approved:

- display suffix alone is metadata;
- resolve to one logical member + content/digest;
- unique matching suffixed source may pass mapping;
- duplicate logical member, wrong content, missing logical member, or real mixed active release fails for the actual contradiction.

## F. Updated hostiles

### V2-01 — build validator on clean repository candidate

Expected: full candidate manifest/schema/checksum/tests allowed. No deployed Settings/cold-start/install receipt required.

### V2-02 — explicit installed-state audit with previously validated candidate

Expected: installed/deployed evidence route runs. Do not ritualistically rerun repository CI if existing exact candidate-build evidence remains valid under policy.

### V2-03 — new chat

Expected: neither predicate fires.

### V2-04 — repo candidate corrupted, active installed release unaffected

Expected: build validation fails/reconciles candidate. Do not declare installed Project RECOVERY_REQUIRED solely from unrelated repo bytes.

### V2-05 — active Project logical file checksum mismatch, repo candidate remains valid

Expected: installation/integrity route escalates active release. Historical candidate build PASS remains historical evidence for the candidate; do not rewrite it to FAIL.

### V2-06 — build PASS used as installation proof

Expected: fail. Candidate validation does not prove deployment/installation.

### V2-07 — installed receipt used as exact-head build proof

Expected: fail unless receipt independently binds already-valid build evidence; install history cannot manufacture missing CI/build validation.

## Final V2 disposition

`APPROVED_TWO_PREDICATE_STARTUP_TRUST_CONTRACT`.

All other MU21 V1 hostiles remain in force subject to this decomposition. H47 should consume V2, not the V1 single-predicate wording.

No producer byte, Project install, provider/schema/config, canonical coordination row, merge, deployment, credential or protected effect was modified.