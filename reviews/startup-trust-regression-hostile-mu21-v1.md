# Mune MU21 — Startup Trust Regression Hostile Review

**Assignment:** provisional `MU21 / STARTUP_TRUST_REGRESSION_HOSTILE`, Voss Slack 2026-08-09 11:05 EDT  
**Primary bug:** TRIAGED MEDIUM `b62d01e4-f780-417d-a9ce-ccfc9c53b8d7`  
**Related independently verified bug:** `afee6adc-d5e7-4a6a-be1e-7dbfaed23e25` / filename-suffix recovery false positive  
**Target:** H47 successor startup rule across Runtime / Project Instructions / Laws / validator, reconciled against active R8A3 startup-trust semantics and H35 installation machine  
**Disposition:** `APPROVE_DIRECTION_WITH_CLOSED_TRIGGER_PREDICATE_AND_LOGICAL_FILENAME_CORRECTION; CURRENT_R9A0_BYTES_CHANGES_REQUIRED`

## Executive verdict

R8A3's startup-trust hotfix got the important boundary right:

> platform-supplied active Project files are operational immediately; verification records evidence, it does not activate ordinary use.

R9A0 must preserve that behavior while fixing R8A3's obsolete atomic-install details. The correct successor is **not** “never validate on startup.” It is:

`ORDINARY_ORIENTATION != FORMAL_INSTALLATION_OR_INTEGRITY_VERIFICATION`.

Ordinary `NEW_CHAT` / `NEW_RUNTIME` performs task-relevant orientation and reads only the governing files/evidence materially needed for the task. A full package inventory/checksum/cold-start ceremony activates only under a **closed verification-trigger predicate**, not because a runtime exists.

Current R9A0 bytes fail this boundary in two independently verified ways:

- Runtime boot step 2 unconditionally requires complete Manifest/checksum verification on boot (`b62d01e4...`);
- Laws say any renamed release file produces `RECOVERY_REQUIRED`, even a harmless upload/display suffix (`afee6adc...`).

Direction is APPROVED after the exact corrections below. Current bytes remain CHANGES_REQUIRED.

## 1. Closed successor trigger predicate

Define one machine/governance predicate such as `FULL_RELEASE_VERIFICATION_TRIGGERED` with **only** the following trigger classes.

### T1 — current installation/replacement operation

The user/runtime is actually performing or evaluating the current R9A0 Project replacement/install operation under exact authority.

This includes the H35 nontransactional installation machine and its exact final logical-set/readback stages.

### T2 — explicit installation/integrity audit request

Patrick explicitly requests package integrity, installation audit, file-set/checksum verification, or equivalent exact audit of the active release.

### T3 — formal installation-state claim requires proof

A response/action must assert a formal state such as `INSTALLED_VERIFIED_CURRENT`, `INSTALLED_ARTIFACT_IDENTITY_VERIFIED`, or another policy-defined installation claim that depends on the exact package/Settings/readback evidence.

The claim itself does not become true because the check is requested. It merely activates the evidence resolver.

### T4 — actual content/integrity contradiction

Freshly observed evidence shows a material condition such as:

- required logical file genuinely absent;
- required file cannot be parsed/read;
- two active files map ambiguously to the same logical package member;
- manifest logical membership conflicts with actual active content;
- checksum/digest conflict after correct logical-name resolution;
- mixed active authoritative releases;
- Project Settings/active-release identity conflict when installation/current release identity is material;
- stronger observed content evidence contradicts the user's current replacement statement.

This is an **observed contradiction**, not suspicion generated solely by an upload/display filename.

### T5 — explicit release-validation/build step

Deterministic validator/CI/release-build work may intentionally verify the complete repository candidate. This is a **build/release validation route**, not runtime startup.

A build validator is allowed to require exact manifest membership and checksums every run because its job is package validation. That does not authorize Runtime boot to do the same on every chat.

## 2. Closed ordinary startup rule

Absent T1–T5:

1. apply platform/safety + current Patrick correction;
2. treat platform-supplied active Project instructions/files as operational;
3. read only governing files needed for the current task;
4. resolve task-relevant shared state/current authority when material;
5. resume valid work without formal installation inference;
6. do not enumerate/hash all 16 files merely because chat/runtime changed;
7. do not run cold-start installation protocol merely because runtime is fresh;
8. do not require a completed installation receipt for ordinary work.

`NEW_CHAT` and `NEW_RUNTIME` are orientation triggers only. They are not members of `FULL_RELEASE_VERIFICATION_TRIGGERED` by themselves.

## 3. “Installation-sensitive” must be a closed consumer set, not a vague adjective

The phrase “when installation is material” is too broad if left untyped. Nearly any project task can be rhetorically connected to installation, making the hotfix meaningless.

Define installation-sensitive consumption by **which output/effect is requested**, not by loose topical relevance.

Installation evidence is materially required only when the operation consumes installation state, for example:

- assert formal installed/current-active release state;
- dispatch/resume/recover an install attempt;
- decide an installation-specific remediation/recovery action;
- verify exact active package identity for a release/install acceptance gate;
- make a downstream effect decision whose declared policy explicitly requires installed-state evidence.

Installation evidence is **not** automatically required for:

- discussing/reviewing repository source;
- ordinary assignment execution;
- retrieving project history;
- answering a task whose correctness depends on current authority/branch but not package installation;
- a new chat/runtime merely existing;
- reading one active Project file supplied by the platform;
- checking current time, user correction, ordinary shared-state status, etc.

If a consumer policy says installation state is required, that exact policy/ref must be named. “Could matter somehow” is not a gate.

## 4. Full hostile matrix

### S01 — ordinary new chat

Precondition: active platform-supplied Project files are available, no contradiction, user asks to continue an existing assignment.

Expected:

- no 16-file inventory;
- no checksum pass;
- no cold-start install audit;
- task-relevant authority/head/shared-state refresh only;
- ordinary work continues.

### S02 — ordinary new runtime after previous chat filled

Same as S01. Fresh runtime is not a replacement event.

### S03 — user asks a repository question unrelated to install state

Expected: read repository/task evidence only. Do not block on installation receipt or Project file hashes.

### S04 — explicit “verify my R9A0 installation” request

Expected: full install/integrity machine activates. Exact logical file set, Settings, manifest/checksums, duplicates/mixed release, base outcome/cold-start/post-install/final receipt/readback are evaluated according to H35. Ordinary startup shortcut does **not** waive formal evidence.

### S05 — explicit `INSTALLED_VERIFIED_CURRENT` claim requested

Files are present but no valid receipt/readback chain exists.

Expected: verification triggers; result remains NOT_ESTABLISHED/UNVERIFIED as evidence dictates. Presence alone cannot mint formal install state.

### S06 — files present, no install receipt, ordinary task

Expected: files remain operational for ordinary work; formal installation remains separately unresolved/unverified. No degradation solely from missing receipt.

### S07 — genuine checksum mismatch

After exact logical-name mapping, active file bytes disagree with the applicable manifest/checksum evidence.

Expected: integrity conflict escalates according to installation/active-release policy, potentially `RECOVERY_REQUIRED` when active-release identity is materially affected. Startup trust does not mean ignore real corruption.

### S08 — manifest says file exists, logical member truly absent

Expected: actual integrity trigger. Do not continue an install-sensitive claim from a missing required logical file.

### S09 — parse failure

Required governing file exists but cannot be parsed/read when its content is needed.

Expected: integrity/availability fail closed for the affected operation. Do not classify it as harmless metadata noise.

### S10 — transport suffix only

Platform displays `VERA_R9A0_LAWS(1).md`; bytes/digest match the unique logical Laws member and no second conflicting logical member exists.

Expected: map to logical name, no integrity failure merely from suffix.

This directly rejects current R9A0 law 20's blanket “renamed => RECOVERY_REQUIRED”.

### S11 — suffix + conflicting duplicate

Both `VERA_R9A0_LAWS.md` and `VERA_R9A0_LAWS(1).md` are active and map to the same logical member with different bytes.

Expected: ambiguity/content conflict. This **is** an integrity trigger. Suffix tolerance is not duplicate amnesty.

### S12 — suffix maps to wrong logical file/content

Display suffix exists but content/digest does not match the supposed logical member.

Expected: fail mapping/integrity. The rule is content-controlled mapping, not “ignore parentheses.”

### S13 — clean user replacement statement, no observed contradiction

Patrick directly says the old files were removed and successor loaded cleanly. Ordinary task follows.

Expected: statement controls ordinary active routing; no ritual audit required. It does not create a formal install receipt or `INSTALLED_VERIFIED`.

### S14 — user clean-replacement statement contradicted by stronger content evidence

Fresh observed content proves mixed old/new active release or wrong required file.

Expected: observed contradiction wins for integrity/current-release-sensitive claim; activate reconciliation/recovery. Direct statement is not allowed to override concrete conflicting bytes.

### S15 — build validator execution

CI/author explicitly runs `validate_r9a0_project.py` on candidate tree.

Expected: complete candidate Manifest/checksum verification is allowed/required by validator policy. No rule says the deterministic validator must become task-local merely because runtime startup is task-local.

### S16 — runtime boot calls deterministic validator automatically

New chat with no install trigger invokes full validator as Runtime boot step.

Expected: FAIL startup-trust test. Build validator route must not be wired into ordinary boot.

### S17 — installation audit reads only file presence

All 16 files exist but one checksum differs; auditor returns installed verified from presence/count alone.

Expected: FAIL. Formal audit consumes content/digest/Settings/post-effect evidence, not count alone.

### S18 — ordinary work blocked by `INSTALLATION_UNVERIFIED`

No installation-sensitive output requested; runtime refuses to resume assignment because formal receipt is absent.

Expected: FAIL. `INSTALLATION_UNVERIFIED` is a formal-installation fact, not an operational lock.

### S19 — vague materiality trap

Runtime says “installation might be relevant to project correctness,” then performs full audit before every task.

Expected: FAIL. Must identify an exact install-state consumer/policy. If none exists, ordinary route applies.

### S20 — downstream policy explicitly requires installed state

A future protected-effect policy explicitly lists current installed qualification as prerequisite.

Expected: that consumer triggers exact installation evidence refresh. Startup hotfix cannot bypass an explicit downstream gate.

### S21 — historical chat/archive contains old-release text

Active logical file/Settings set is successor, but old release text remains in chat/archive context.

Expected: historical text is DATA_NOT_CURRENT_AUTHORITY; not a “mixed active release” by itself. Do not demand impossible historical erasure.

### S22 — active mixed authoritative release

Current Project source/config surfaces actually contain both old and successor active authoritative files/rules.

Expected: real mixed-release conflict. Distinguish active authoritative set from historical retained text.

## 5. Exact byte-impact recommendation

No new path is needed. Startup-trust correction belongs within existing native74 MODIFY paths.

### `project/VERA_R9A0_RUNTIME.md`

Replace unconditional Boot step 2 with:

- platform-supplied files operational immediately;
- task-relevant governing read;
- closed full-verification trigger predicate;
- build/release validator explicitly separate.

Remove stale “GPT-5.6 Thinking” boot identity at the same temporal/source correction stage rather than swapping in another frozen model name.

### `project/VERA_R9A0_PROJECT_INSTRUCTIONS.md`

Add/restore:

- operational startup trust;
- new chat/runtime not install;
- exact full-verification trigger set;
- direct clean-replacement ordinary routing vs formal receipt separation;
- logical filename/content mapping for suffix noise;
- H35 nontransactional final active-set semantics rather than atomic-backend wording.

### `project/VERA_R9A0_LAWS.md`

Replace current law 19/20 semantics as needed:

- formal installed verification consumes H35 exact receipt/readback machine;
- no blanket `renamed => RECOVERY_REQUIRED`;
- display suffix alone non-failure;
- real logical absence/mixed active release/parse/content-digest conflict can trigger recovery;
- ordinary new chat does not trigger full audit.

### `scripts/validate_r9a0_project.py` + existing tests

Keep full deterministic candidate verification. Add machine tests that ensure validator policy is not accidentally imported into Runtime startup semantics. Validator itself may remain strict on repository manifest filenames; installation logical-filename suffix resolution is an installation/readback-layer concern, not a reason for repository package paths to become fuzzy.

### Other existing paths

Cold Start / Post-Install / Receipt / Recovery / Package / Manifest may need wording/field updates only where H35/H46 already requires them, but startup-trust repair itself does not justify path expansion or independent semantics in those files.

## 6. Separation of four states

The successor must never collapse:

1. **OPERATIONAL_ACTIVE_FILES_AVAILABLE**: platform supplied active files; ordinary use allowed.
2. **PACKAGE_BUILD_VALIDATED**: repository candidate deterministic manifest/checksum/schema/tests passed at exact candidate evidence.
3. **INSTALLATION_ARTIFACT_HISTORY_VERIFIED**: completed effect + immutable receipt/readback proves the installed artifact history.
4. **INSTALLED_VERIFIED_CURRENT**: current aggregate still satisfies active-release/post-install/current environment policy.

A new chat changes none of these by itself.

## 7. Final verdict

`H47_DIRECTION = APPROVED_WITH_EXACT_TRIGGER_CLOSURE`.

Required before implementation acceptance:

- closed T1–T5 verification trigger classes or exact equivalent;
- explicit non-trigger rule for NEW_CHAT/NEW_RUNTIME;
- exact install-state consumer definition, not vague “materiality”;
- build validator explicitly separate from runtime startup;
- formal installation proof remains strict;
- file presence alone never mints install state;
- logical suffix mapping before integrity failure;
- real checksum/manifest/mixed/parse contradiction still escalates;
- historical old text is not mixed active release;
- H35 nontransactional install semantics replace atomic-backend claims.

Current R9A0 Runtime/Laws/Project Instructions remain CHANGES_REQUIRED.

No Vera-R9A0 producer byte, Project install, provider/schema/config, canonical coordination row, merge, deployment, credential or protected effect was modified by MU21.