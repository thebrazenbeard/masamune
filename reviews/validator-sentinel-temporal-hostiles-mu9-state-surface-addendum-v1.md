# Mune MU9 Addendum — Immutable Package State Must Not Masquerade as Live State

**Assignment:** `VOSS-20260809-MU9` / root sequence `3644`  
**Parent audit:** `reviews/validator-sentinel-temporal-hostiles-mu9-v1.md` @ `8fd53f7e94d82fec21897140d08443219472f186`  
**Database-base addendum:** `reviews/validator-sentinel-temporal-hostiles-mu9-database-base-addendum-v1.md` @ `c3a6ae853fc8507b2f7a004c378e184accd90479`  
**Class:** read-only temporal-validator architecture  
**Producer/provider mutation:** none

## Verdict

MA16's stronger challenge is directionally correct, with one precision correction: the package does not need to delete `STATE.md`; it needs to stop treating immutable package state as an authoritative live-state surface.

A package state file can safely remain if its semantics are explicitly **generation-bound snapshot/provenance**. It becomes dangerous when fields or prose are indexical, e.g. “current writer”, “current model”, “current installed release”, “accepted for current native base”, or “current confinement status”, because the bytes cannot evolve when the external state changes.

The clean split is:

1. **immutable package snapshot**: facts true at generation/qualification, bound to exact package/head/model/provider observations and preserved forever as provenance;
2. **receipt-overridable installation metadata**: generation `INSTALLATION_UNVERIFIED` is true of the package-at-generation but never competes with a later completed installation receipt/current cold-start readback;
3. **live governed/runtime state**: current assignee/route, delegation validity, model identity, installed release, database-validation currentness, target heads, provider posture and confinement/effect eligibility come only from fresh authority-admitted/provider/platform evidence.

This avoids turning a prose parser into an oracle for facts that necessarily outlive the file that contains them.

## Verified false-positive / false-negative pair

The exact B12 Rebind validator implements document semantics as raw case-insensitive substring presence/absence. Therefore temporal context cannot affect the outcome.

### False positive: stale current state passes

A document can contain:

```text
Historical builder was workstream/build-bob; current builder is workstream/build-alice.
Historical generation metadata was INSTALLATION_UNVERIFIED; current installation is INSTALLED_VERIFIED by receipt R.
```

The required tokens `workstream/build-bob` and `INSTALLATION_UNVERIFIED` are present, so those required sentinel checks pass even though the document explicitly says they are no longer current.

This is the already-reported MEDIUM class, canonical bug `52627ea5-29ab-4c53-b869-4cff71f85005`.

### False negative: correct historical provenance is rejected

The same mechanism applies to forbidden sentinels. For example the exact validator forbids literals including historical routing/release phrases such as `workstream/build-enforcer` or `R8A1 remains active installed Project release` in selected documents.

A semantically correct document could say:

```text
Historical superseded release text said: R8A1 remains active installed Project release.
That statement is historical only; the current installed state is resolved from the later valid receipt/readback.
```

The validator still rejects it solely because the forbidden substring exists. Thus a repair that merely swaps required/forbidden token lists will continue to erase or reject legitimate provenance.

## Lifecycle classes

The smallest useful assertion classes are:

### `NORMATIVE_STABLE`

Policy intended to remain true across normal lifecycle movement. Examples:

- Patrick remains owner of user-only effect gates unless explicitly changed by current governing authority;
- currentness must be resolved before START/RESUME/USE_AUTHORITY;
- Basic Memory Cloud is not an active dependency under the accepted architecture;
- generation metadata does not outrank a later valid receipt.

Validator treatment: validate semantic rule/structure in immutable package bytes.

### `GENERATION_PROVENANCE`

Exact observations or identities of the generated candidate. Examples:

- package/release ID;
- native candidate digest/byte count;
- provider PostgreSQL `17.6 / 170006` **at generation**;
- model/mode used for a specific qualification run;
- database validation receipt bound to DB head `58a6...` and native base `6a568...`.

Validator treatment: preserve exact bytes/digests; never promote them to current state merely because they are present.

### `RECEIPT_OVERRIDABLE`

Generation fact that remains historically true but whose corresponding current state is resolved from later receipts/readback. Primary example:

- `INSTALLATION_UNVERIFIED` at generation.

Validator treatment: ensure the package labels it as generation state and includes the precedence rule; do not require current installation state to equal it.

### `VOLATILE_RUNTIME_OBSERVED`

Facts that cannot be made permanently current inside immutable package bytes. Examples:

- current model identity;
- current assignee/build route;
- whether Voss delegation is currently active;
- current installed release;
- current native/repository head;
- current database-validation eligibility for the active native base;
- current provider version when runtime parity matters;
- current confinement/effect-eligibility result.

Validator treatment: the immutable package may state **how to resolve** these facts and may preserve generation observations, but must not require a particular current value.

## Challenge to the “STATE.md should cease being live” proposal

I would not remove the state artifact entirely. That loses useful immutable provenance and makes installation/recovery auditing harder.

Instead define the file's contract explicitly, for example conceptually:

`PACKAGE_STATE_SNAPSHOT_AT_GENERATION`

and prohibit unqualified indexical fields such as `current_*` unless the value is itself a stable policy constant. A field named `database_contract_state=SUCCESSOR_ACCEPTED_FOR_CURRENT_NATIVE_BASE_INTEGRATION_PENDING` is especially problematic because `current` is evaluated at read time while the bound base is immutable. Prefer bound wording such as:

`database_validation_disposition_for_bound_native_base = ACCEPTED_FOR_BASE`

with exact `database_bound_native_base`, receipt/run identity and lifecycle. A separate live resolver decides whether that bound receipt is `VALID`, `REVALIDATE_REQUIRED`, or `HISTORICAL_ONLY` for the presently active native base.

Likewise, `Bob is the current native build/review route` should become a stable routing rule (“resolve current route from fresh authority-admitted assignment state”) plus optional generation provenance (“route observed at generation: Bob”).

`GPT-5.6 Thinking is the underlying model` should become runtime/platform-observed semantics, with exact model/mode retained only in qualification/generation receipts.

## Voss delegation hostile

Stable policy:

`Voss owns routing while delegated.`

Volatile assertion:

`Voss currently has delegated routing authority.`

A package may safely encode the first. It cannot prove the second after a future Patrick revocation. Any validator that treats the presence of `Voss owns routing` as sufficient evidence of current delegation creates the same temporal bug in authority form.

For START/RESUME/USE_AUTHORITY, current delegation/assignment must be re-resolved from current authority-admitted state, not inferred from package prose.

## Minimum validator invariant set

1. Validate immutable **structure and provenance bindings** in package bytes.
2. Every lifecycle-sensitive assertion has an explicit class; no unclassified indexical “current” fact is accepted as package truth.
3. Required/forbidden validation is semantic/typed, not whole-document substring presence.
4. Historical quotation, superseded values and rejected claims cannot satisfy current-state requirements.
5. Historical quotation/superseded values are not rejected merely because they contain an obsolete token.
6. `GENERATION_PROVENANCE` remains immutable and exact after state moves.
7. `RECEIPT_OVERRIDABLE` generation facts remain historical while current state comes from the newest valid receipt/readback.
8. `VOLATILE_RUNTIME_OBSERVED` values are resolved outside immutable package bytes when materially used.
9. Cross-artifact acceptance never promotes a bound receipt to a new target/base without an explicit current comparison/invalidation policy.
10. Validator PASS means the package correctly encodes these rules and provenance. It does **not** mean external current state equals generation state.

## Current disposition

`CHANGES_REQUIRED_TEMPORAL_ASSERTION_CLASSIFICATION_AND_LIVE_STATE_SPLIT`

No new bug ticket is needed for this addendum: the substring/context failure is the same canonical defect class already receipted as `52627ea5-29ab-4c53-b869-4cff71f85005`; canonical 3647/3652 separately cover the database-base stale-promotion manifestation.

No B15 successor bytes, producer-branch mutation, database/schema/provider/config change, installation, deployment or authority mutation was performed.