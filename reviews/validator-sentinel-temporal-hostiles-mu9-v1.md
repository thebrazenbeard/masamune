# Mune MU9 — Validator Sentinel Temporal Hostiles V1

**Assignment:** `VOSS-20260809-MU9` / canonical root sequence `3644`  
**Class:** read-only adversarial validator audit  
**Producer mutation:** none  
**Reviewed exact sources:** B11 committed Settings at `ddcd98b4e61df09f06886f2073ecbdfad21c8f12`; B12 Rebind 17.6 Contract/schema/validator from Bob review packet 3551  
**Verdict:** `CHANGES_REQUIRED_TEMPORAL_ASSERTION_CLASSIFICATION`

## Executive result

The B12 Rebind validator mixes two very different jobs:

1. exact package/candidate provenance validation, where fixed hashes, generation-time provider facts and candidate-bound heads are legitimate; and
2. document “semantic” sentinel validation, where raw substring presence is being used as a proxy for lifecycle-sensitive meaning.

The first is largely sound. The second is not.

Exact `validate_document_semantics()` lowercases each document and checks only whether every required phrase occurs somewhere and every forbidden phrase does not occur. It does not know whether a required token is presented as current truth, historical provenance, a rejected statement, a generation snapshot, or an explicitly superseded value.

That creates a verified temporal false-negative class: a document can make materially stale current-state claims and still satisfy the validator merely because the expected tokens are present.

Canonical Vera `bug_ops` receipt: `52627ea5-29ab-4c53-b869-4cff71f85005`.

## Exact source observations

### B11 Settings

Committed blob `c757111d8e1c555d7a3a3a0bf0191c840f8071c7` contains two volatile present-tense claims:

- `GPT-5.6 Thinking is the underlying model.`
- `Bob is the current native build/review route...`

The first is already stale against the current runtime identity `GPT-5.6 Sol`. The second is currently true under B15 but becomes false on a valid closure/reroute.

The same Settings correctly treats installation generation metadata differently:

- generation-time `INSTALLATION_UNVERIFIED` never overrides a later valid receipt.

That distinction is the right model.

### B12 Contract / schema

The Rebind 17.6 Contract and closed schema correctly encode several facts as package/generation provenance rather than universal current truth:

- `installation.generation_state = INSTALLATION_UNVERIFIED`;
- `installation.receipt_precedence = COMPLETED_RECEIPT_AND_READBACK_OVERRIDE_GENERATION_METADATA_FOR_CURRENT_STATE`;
- `supabase.provider_postgres_version_at_generation = 17.6`;
- `supabase.provider_postgres_version_num_at_generation = 170006`;
- `supabase.hosted_provider_parity_status_at_generation = NOT_PROVEN`;
- exact native Settings bytes/hash/count;
- exact database successor head / native-base binding for this candidate;
- qualification binds exact candidate, Settings, Project, model/mode, source and tool identity.

Those are legitimate immutable artifact facts. A later provider upgrade, branch movement, installation receipt or runtime-model change does not make the historical generation record false.

### B12 validator

Exact Drive candidate `1wKrp36nkBBqlwL19sxD1HcCbsakMiqvQ`, SHA-256 `f3dc2d6fdf6da60fd18ce35138b4a098897d293abeeedd510ce8c28a4abd4908`:

- hard-codes exact B11 hash/count and exact B12 Contract/schema hashes;
- requires literal `Bob is the current native build/review route` in native Settings;
- requires `workstream/build-bob` in Project Instructions, Laws, Governance and State;
- requires temporal tokens such as `R8A3`, `INSTALLATION_UNVERIFIED`, database head/native base, `17.6`, `170006`, `NOT_PROVEN`, `PROCEDURAL`, and `MATRIX_RECORDED` in various long-lived documents;
- implements document sentinels as case-insensitive substring presence/absence only.

## Verified minimal hostile

Using the exact required State sentinel set and the validator’s exact substring algorithm, this synthetic post-install/reroute/provider-changed document produces zero sentinel errors:

```text
Current writer: workstream/build-bob.
Current installed release is R8A3.
Current installation state: INSTALLATION_UNVERIFIED.
Current database head: 58a6ae4d4272165bd5b988bdd7a8bb0e72417302.
Current native base: 6a568d35c142dc37ea41a0209cdb1f295949f767.
Current provider PostgreSQL is 17.6 / 170006.
Current hosted parity: NOT_PROVEN.
Current authority assurance: PROCEDURAL.
Current confinement: MATRIX_RECORDED.
Basic Memory Cloud is disconnected paid legacy.
```

All required tokens are present and no current forbidden token is present, so the semantic sentinel pass accepts it even if every “Current ...” assertion except Basic Memory status has been superseded by later valid evidence.

This is not a hypothetical parser preference. It follows directly from the exact validator implementation.

## Temporal hostile matrix

### 1. Runtime model changes

**Before:** qualification/model at package generation may be GPT-5.6 Thinking.  
**After:** platform runtime becomes GPT-5.6 Sol.

- Historical qualification receipt remains valid evidence for the run it describes.
- Model-dependent behavioral qualification may become stale and require rerun under policy.
- Long-lived Settings must not continue asserting the old model as present runtime truth.
- Deterministic package validation must not pretend to discover current model identity from frozen bytes.

Classification:

- exact qualification model/mode: `GENERATION_PROVENANCE`;
- current runtime model: `VOLATILE_RUNTIME_OBSERVED`.

### 2. Bob closes/reroutes

**Before:** B15 current owner/route is Bob.  
**After:** Voss admits closure or reroute.

Exact B12 validator currently forces a false current claim through `REQUIRED_NATIVE` and requires Bob route tokens across long-lived docs.

Classification:

- Bob/Enforcer history: `GENERATION_PROVENANCE` / historical provenance;
- current assignee/build route: `VOLATILE_RUNTIME_OBSERVED` from fresh authority-admitted assignment state.

A validator may preserve Bob as provenance but must not require the proposition “Bob is current.”

### 3. R8A3 -> R9A0 installation

The package may legitimately preserve that R8A3 was predecessor/current-at-generation context. After a valid R9A0 installation receipt, runtime current installation changes.

Do **not** rewrite historical package provenance to claim it was always installed. Do **not** let a required `R8A3` token imply R8A3 is still current.

Classification:

- predecessor/base release at generation: `GENERATION_PROVENANCE`;
- currently installed release: `RECEIPT_OVERRIDABLE` current state resolved from valid installation receipt/readback.

### 4. `INSTALLATION_UNVERIFIED` -> valid receipt

This is already modeled correctly in B12 Contract.

`installation.generation_state = INSTALLATION_UNVERIFIED` should remain immutable package provenance after install. Current installation truth is derived from completed receipt + readback and may become `INSTALLED_VERIFIED` without changing the package field.

The bug is not that the token exists. The bug is that a context-free document sentinel cannot tell generation metadata from a stale current-state assertion.

### 5. Database/native candidate movement

**Before final candidate freeze:** movement of the bound native base/database candidate requires rebind/revalidation.  
**After immutable package generation/install:** later branch/head movement does not retroactively alter the package’s historical binding.

Classification:

- package-bound database successor head/native base: `GENERATION_PROVENANCE` / immutable candidate identity;
- current GitHub/provider target head for a new effect or integration decision: `VOLATILE_RUNTIME_OBSERVED` and target-side CAS/readback.

The validator should keep exact package hashes/heads; consumers must not interpret them as “latest/current provider head.”

### 6. Confinement verdict changes

`MATRIX_RECORDED` may accurately describe a generation-time evidence posture. H29 currently proves `FAIL_NOT_ELIGIBLE`; a future broker may later improve confinement.

Classification:

- package/generation confinement evidence snapshot: `GENERATION_PROVENANCE` if explicitly labeled and receipt-bound;
- current effect-confinement/activation eligibility: `VOLATILE_RUNTIME_OBSERVED` from current H14/H19/H29 evidence.

A bare required `MATRIX_RECORDED` occurrence proves neither.

### 7. Provider PostgreSQL version changes

B12’s `_at_generation` fields are correctly scoped:

- `17.6 / 170006` may remain immutable package provenance;
- current provider engine version must come from fresh provider SQL when material.

A future PG18 provider does not falsify the historical B12 generation record. It may stale deployment/provider-parity evidence and require revalidation.

## False positive vs false negative behavior

### Verified false negative

A materially stale current-state document can pass because required temporal words appear somewhere. Historical, rejected and current uses are indistinguishable to the substring validator.

### Verified route false positive

A semantically correct successor that removes the literal current-Bob proposition will fail `REQUIRED_NATIVE` until the validator is rebound, even when fresh governed state correctly assigns someone else. This is the already-identified Bob-route propagation defect.

### Do not overcorrect

Do **not** remove every old literal merely because it can become non-current. `INSTALLATION_UNVERIFIED`, provider 17.6/170006, database candidate heads, predecessor release IDs and qualification model identity can be valid immutable generation provenance.

The repair is lifecycle classification, not historical amnesia.

## Smallest validator invariant set

Every lifecycle-sensitive assertion enforced by the package/validator must have one explicit class:

```text
NORMATIVE_STABLE
GENERATION_PROVENANCE
RECEIPT_OVERRIDABLE
VOLATILE_RUNTIME_OBSERVED
```

Rules:

1. `NORMATIVE_STABLE`: package validator may exact-enforce invariant value/semantics.
2. `GENERATION_PROVENANCE`: exact-enforce immutable package-bound value plus a machine-visible provenance label; never use it as live-state truth.
3. `RECEIPT_OVERRIDABLE`: exact-enforce the generation/default value and the precedence rule; current value comes from a later valid receipt/readback.
4. `VOLATILE_RUNTIME_OBSERVED`: package validator must not require one frozen current value. A runtime/post-install/currentness gate must observe it from the governing source when material.
5. Document duplication of structured provenance must use machine-visible labeled context or bounded structured sections, not arbitrary substring presence.
6. Historical/rejected text cannot satisfy a current-state assertion merely by containing the token.
7. Current-state changes do not rewrite immutable generation history.
8. Qualification receipts remain historical evidence; staleness/revalidation is a separate evidence-lifecycle result.
9. Branch/provider/model/assignee changes are evaluated at the boundary where their currentness matters, not inferred from package generation bytes.
10. Temporal property tests must include at least: preinstall -> installed, Bob -> other assignee, model A -> model B, candidate/base movement, confinement fail -> pass/pass -> fail, provider major/version movement, and stale historical token surviving in document text.

## Challenge to the current repair direction

Bob/MA16 are right to remove volatile current Bob/model claims from long-lived normative configuration, but a broad cleanup that deletes all old release/head/version/install/confinement literals would be equally wrong.

The clean split is:

- keep exact artifact provenance exact;
- keep receipt precedence explicit;
- move only genuinely current facts to fresh governed/runtime observations;
- make validator checks prove lifecycle/context, not word presence.

## Verdict

`CHANGES_REQUIRED_TEMPORAL_ASSERTION_CLASSIFICATION`

The exact package-binding machinery should remain strict. The context-free semantic sentinel layer should not.

No producer branch, B12 candidate, Supabase schema, provider configuration, installation state, credential, permission or protected target was modified by this audit.