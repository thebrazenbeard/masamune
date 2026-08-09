# Mune MU17 — Native Contract Schema Hostile Matrix

**Assignment:** provisional `MU17 / NATIVE_CONTRACT_SCHEMA_HOSTILE`, Voss Slack 2026-08-09 10:27 EDT  
**Primary bugs:** TRIAGED MEDIUM `819654d7-c967-476e-a753-f37003de17d9` + `85182817-4be6-44ee-92be-bc84c33fa6c8`  
**Current Contract:** blob `a3a4a614ff9f9afffb4a9a640a8f976bc2a4a7aa`  
**Current schema:** blob `2c2cef8689d75c06e8cf3b508fd4b2d79e1acc83`  
**Companion engine review:** MU19 `STDLIB_CLOSED_PROFILE_V1` hostile matrix  
**Disposition:** `CURRENT_SCHEMA_CHANGES_REQUIRED; SUCCESSOR_NEGATIVE_MATRIX_FROZEN; EXACT_SUCCESSOR_FIELD_VOCABULARY_AWAITS_H46/B17/MA23_V3`

## Executive verdict

The current Native Contract schema is structurally inadequate even before temporal semantics are considered. It closes the top level and `legacy_memory`, but `ci`, `installation`, `native_instructions`, `retrieval`, `supabase`, and `voice` are effectively open semantic bags.

The opposite “repair” is also wrong: recursively close those objects by freezing today's current model/route/provider/database/PASS answers as immutable consts.

The successor schema must do two things at once:

1. reject structural/policy drift inside every governed object;
2. refuse to turn volatile current state into package truth merely because const validation is convenient.

This review freezes the **negative fixture matrix**, not the final successor field names. H46/B17/MA23 V3 still own exact field vocabulary/retyping.

## 1. Current exact defects

Current schema top-level required set is closed, but six semantic objects are only `{type: object}`. Therefore under a real general JSON-Schema engine, examples such as the following remain schema-valid today:

- `ci.local_only_acceptance_prohibited = false`;
- `ci.workflow_path = "attacker.yml"`;
- `installation.atomic_unique_file_set_required = false`;
- `installation.receipt_precedence = "IGNORE_RECEIPTS"`;
- arbitrary `supabase` fields/omissions;
- `retrieval = {}`;
- `voice = {}`;
- arbitrary nested injection under any of those six objects.

Current validator also does not yet execute the schema at all, tracked by `819654d7...`.

Thus schema application alone does not repair `85182817...`; closure and enforcement are one acceptance stage.

## 2. Exact negative fixture matrix — stable structural/policy fields

Each case below must fail either `SCHEMA_PROFILE` or the machine-owned invariant layer once the exact successor field map is frozen.

### C01 — active surface drift

Mutations:

- add `BASIC_MEMORY`;
- remove `SUPABASE`/`GITHUB`/`GOOGLE_DRIVE`/native-files surface without a separately admitted architecture change;
- reorder if successor chooses const-ordered representation and order is intentionally identity-bearing.

Expected: fail. Basic Memory cannot become an active route through a Contract edit.

### C02 — CI exact-head gate weakened

`ci.exact_head_success_required = false`.

Expected: fail.

### C03 — CI local-only acceptance enabled

`ci.local_only_acceptance_prohibited = false`.

Expected: fail.

### C04 — CI workflow route moved

`ci.workflow_path = "attacker.yml"` or another unadmitted path.

Expected: fail against machine-owned path invariant / successor exact field schema.

Do not confuse this with future integration workflow transport; changing the Contract path still requires an admitted byte-level policy change.

### C05 — CI nested field omitted

Remove one stable normative CI gate while keeping object syntactically valid.

Expected: fail. Closed V1 objects have no optional normative omission by default.

### C06 — retrieval abstention weakened

Set any stable retrieval safety/evidence rule false, including unresolved abstention, evidence locator requirement, false recovery prohibition, or history-sensitive refresh requirement where retained.

Expected: fail.

### C07 — retrieval injection

Add `retrieval.assume_current_when_missing = true` or arbitrary unknown nested key.

Expected: fail unknown field.

### C08 — Basic Memory dependency restored

`legacy_memory.active_dependency = true` or a fallback/reconnect rule that makes Basic Memory an automatic runtime route.

Expected: fail.

### C09 — archive provenance silently changed

Change generation/audit archive identifier or digest without rebinding the declared provenance record.

Expected: fail exact generation-provenance identity or machine-owned digest shape rule.

### C10 — native-instruction path drift

Change the governed native Settings path to another file.

Expected: fail exact logical path invariant.

### C11 — native-instruction limit drift

Raise the admitted character ceiling or remove the limit.

Expected: fail once H46/B17 freezes the exact successor limit. Do not inherit the current `8000` by inertia if the accepted B11 budget has a different final policy.

### C12 — Voice stable behavior weakened

For every Voice behavior H46 classifies `NORMATIVE_STABLE`, flip true->false, omit it, or inject a contradictory behavior rule.

Expected: fail.

Examples include correction supersession, no fabricated privacy rationale, fact/inference separation, incomplete-input clarification and truncation handling if those remain in the successor Contract field map.

## 3. Installation negative fixtures — reject semantic regression without freezing backend fiction

### I01 — receipt precedence disabled

Replace the stable lifecycle rule that completed receipt/readback overrides generation metadata for current installed state with `IGNORE_RECEIPTS` or equivalent.

Expected: fail.

### I02 — generation state promoted to current installed truth

Package generation metadata says `INSTALLED_VERIFIED` absent effect receipt/readback.

Expected: fail or be structurally impossible. Generation metadata is not current installation truth.

### I03 — obsolete atomic-backend claim retained as normative truth

Successor schema preserves a field whose semantics mean “ChatGPT Project replacement occurs atomically as a backend transaction” and consts it true.

Expected: fail field-classification/machine invariant. Preserve the stable safety property as exact final active logical file/Settings set + no mixed authoritative release under the quiesced nontransactional install machine. Do not schema-validate a platform capability H35 does not establish.

### I04 — pre-release / in-situ qualification collapse

Schema flattens post-install `IN_SITU_PROJECT_QUALIFICATION_CURRENT` into the pre-release evidence set or lets pre-release eligibility depend on it.

Expected: machine invariant failure. H35 phase separation is normative.

### I05 — attempt/route lifecycle weakened

Successor install-lifecycle fields allow route mutation within one attempt, reusable attempt identity, or final receipt without the immutable dispatch-time authority binding required by `9094453e...`/MU18.

Expected: fail.

## 4. Supabase / database field-classification hostiles

This is where schema closure most easily becomes temporal corruption.

### S01 — current database state hard-consted

Successor immutable Contract contains a field equivalent to:

`database_contract_state = CURRENT_PASS`

or freezes a current DB head/base as if it were evergreen currentness.

Expected: field-classification failure. Package stores stable DB-gate predicate/lifecycle requirements; exact current integration/qualification/admission evidence is external.

Historical DB heads/runs may remain explicitly **generation/historical provenance** if H46 keeps them, but their field names and consumers must say so.

### S02 — current security verdict hard-consted

Successor schema freezes `external_security_state = APPROVED/CLEAR` as timeless current security truth.

Expected: fail. Keep stable security evidence requirements and explicitly generation-bound approval provenance where needed; current effect/confinement/security eligibility is external.

### S03 — temporary provider target treated as permanent authority

Current `supabase.temporary_project = agvh...` survives as an unqualified timeless current target.

Expected: retype as generation/build-ground provenance or drop according to H46. A temp build target is not a permanent effect authority.

### S04 — production prohibition conflates construction scope and future authority

Current `production_prohibited = klmb...` survives as an ambiguous timeless prohibition.

Expected: fail/rewrite. Stable R9A0 construction-target exclusion and exact future production-effect authority are separate semantics. No schema field grants future production authority.

### S05 — producer/reviewer identity becomes current routing

Current historical Mune approval sequence, rejected head, governance notice, migration or similar evidence is reinterpreted as current actor/route authority.

Expected: fail temporal class. Keep only explicitly generation/audit provenance if still useful.

### S06 — H33 DB gate predicate vocabulary weakened

Remove one of the stable predicates:

- provider compatibility qualification current;
- DB integration binding current;
- DB successor admission current.

Or replace DB-local admission with whole-release admission inside the Package/Contract DB sub-gate.

Expected: machine-owned invariant failure.

The immutable Contract may define these predicate requirements; it must not store their current PASS answers.

## 5. Currentness / authority axis hostiles for successor fields

Exact names wait on H46/MA23 V3, but these semantic mutations must be represented as machine negatives once those fields exist.

### A01 — standing authority absorbs `TARGET_MOVED`

Encode provider target movement as an authority state.

Expected: fail axis invariant. Target binding is separate from standing authority.

### A02 — standing authority absorbs `CONSUMED`

Encode one-use capability/lease/action consumption as standing assignment authority.

Expected: fail. Consumption is an execution/effect companion.

### A03 — factual executability omitted

Schema retains currentness + policy workload result but has no separate factual executability axis.

Expected: machine-owned invariant failure.

### A04 — universal effect Boolean restored

Add `effect_eligible` / `assignment_effect_precondition_pass` as a canonical universal currentness fact.

Expected: fail. Purpose-specific consumers derive eligibility from fresh factual axes + required execution/effect companions.

### A05 — workload policy embedded as assignment truth

Currentness object stores `COUNTS_EXECUTABLE` without an explicit workload policy ref/version/decision binding.

Expected: fail. Workload is a separate policy projection.

### A06 — lane terminal and subject disposition collapse

Schema allows `SUPERSEDED` or `REROUTED_AWAY` to terminalize the stable root lane.

Expected: fail. Stable lane terminal is COMPLETE/CANCEL/TERMINAL_BLOCK; subject/version disposition is separate.

### A07 — evidence relation consumes state

Schema/model makes ACK/REVIEW/evidence a controlling state predecessor or requires one relation slot total.

Expected: fail MA23/MU6 relation invariant.

### A08 — source completeness omitted from currentness envelope

Schema allows current state to be asserted without required source-completeness/consistency/scope proof.

Expected: fail.

## 6. Volatile/current fields that must not be “fixed” by consting them

The negative suite should explicitly reject insertion of immutable Contract fields that assert current values for:

- current model identity;
- current assignee/writer/build route;
- current database integration PASS/head/base;
- current provider qualification/admission PASS;
- current active installed release;
- current confinement/effect eligibility;
- current security clear state;
- current installation receipt result;
- current temporary/provider environment facts unless explicitly labeled `*_AT_GENERATION`/historical provenance.

A validator that rejects nested unknowns but accepts these as new const fields has simply traded an open schema bug for a time bomb with better indentation.

## 7. Voice `unavailable` hostile

Current Contract contains a fixed `voice.unavailable` array mixing observed platform capability limitations with epistemic rules.

Successor test:

- preserve a stale observed platform unavailability as immutable normative capability truth;
- or remove the epistemic rule that root cause cannot be claimed without trace because the platform later changes.

Expected: field-classification split. Stable epistemic behavior stays normative; observed capability unavailability becomes generation/qualification evidence or external observation, not timeless const.

## 8. Schema/Contract coordinated weakening

For every mandatory stable field after H46 freezes the map:

1. remove field from Contract;
2. remove it from schema `properties/required`;
3. keep schema and Contract otherwise internally consistent.

Expected: validator's machine-owned mandatory-field map/invariant fails.

This is required because no candidate-controlled schema can prove that its own deleted rule used to be mandatory.

## 9. Exact structural negatives per governed object

For every final object subtree, generate mechanically:

- unknown nested key;
- required field omission;
- wrong JSON type;
- enum/const mutation;
- object replaced with list/string/null;
- duplicate raw JSON key before schema parse;
- schema child type removed;
- schema child type changed while retaining old keywords;
- schema + Contract co-shrink.

This should be table-driven rather than one bespoke test per field where possible.

## 10. Acceptance verdict

### Current bytes

`CHANGES_REQUIRED`.

Current schema cannot reject most of this matrix and current validator has not yet admitted/executed the H44 profile.

### Hardened profile direction

`APPROVED` as the enforcement mechanism under MU19/H44.

### Exact successor schema

`NOT_YET_APPROVED` until H46/B17 supplies the exact Contract+Manifest field classification and MA23 V3 freezes the remaining coordination adapter. Then instantiate this matrix against exact successor bytes and require all negatives to fail for the intended reason.

No producer byte, provider/schema/config, canonical coordination state, merge, deployment, credential, install effect or Project mutation was performed by MU17.