# Mune MU9 Addendum — Database Receipt Is Bound Provenance, Not Live Native-Base State

**Parent assignment:** `VOSS-20260809-MU9` / root sequence `3644`  
**Canonical input:** Voss `3647` database-base staleness gate  
**Parent audit:** `reviews/validator-sentinel-temporal-hostiles-mu9-v1.md` @ `8fd53f7e94d82fec21897140d08443219472f186`  
**Class:** read-only temporal property refinement  
**Producer/provider mutation:** none

## Result

Canonical 3647 is correct that the old database qualification cannot support final B15 release after native-base movement. The temporal hostile also exposes an important non-bug boundary: the old B12/DB receipt must remain valid **historical bound provenance** for the base it actually tested.

The repair must therefore block stale promotion without rewriting the old artifact.

## Exact source facts

B12 Rebind 17.6 Contract binds:

```text
database_contract_state = SUCCESSOR_ACCEPTED_FOR_CURRENT_NATIVE_BASE_INTEGRATION_PENDING
database_successor_head = 58a6ae4d4272165bd5b988bdd7a8bb0e72417302
database_bound_native_base = 6a568d35c142dc37ea41a0209cdb1f295949f767
native_base_change_requires_fresh_database_validation = true
```

The closed B12 schema fixes those same values.

The exact B12 validator independently checks the same expected state/head/base and only checks that the revalidation rule is `true`. It has no live/native-target input and therefore cannot itself determine whether the current GitHub native head still equals the bound base.

Canonical 3647 supplies the missing current observation: B15 head is already `ddcd98b4e61df09f06886f2073ecbdfad21c8f12`, while the accepted DB run remains bound to `6a568d35...`.

## False-positive / false-negative pair

### Correct preservation case

Question: after native-base movement, is the old database validation receipt still valid evidence that DB head `58a6...` passed the tests it actually ran against base `6a568...`?

**Expected:** YES, as immutable historical/generation evidence.

Do not mutate the old receipt, its merge candidate, its base SHA, or its successful run result. Those facts are still true.

Classification:

`GENERATION_PROVENANCE / HISTORICAL_BOUND_VALIDATION`

### Incorrect promotion case

Question: after the native base moved to `ddcd98b4...`, may the old receipt still satisfy a claim that the DB successor is accepted for the **current** native base?

**Expected:** NO.

Fresh current-base comparison fails:

```text
current_native_base != database_bound_native_base
```

Therefore integration/release currentness becomes:

`REVALIDATION_REQUIRED`

until a fresh exact-candidate DB run binds the new/final native base or an authority-admitted narrower invalidation policy is mechanically established.

## Does B12 schema/validator force stale promotion?

**Not by itself, if its output is correctly interpreted as artifact validation.**

The B12 schema and validator force the historical candidate’s exact bound values. That is legitimate package identity. The validator is intentionally deterministic over files and has no live GitHub head input, so it cannot establish present integration eligibility.

The dangerous part is the indexical field name/value:

`SUCCESSOR_ACCEPTED_FOR_CURRENT_NATIVE_BASE_INTEGRATION_PENDING`

Once the artifact is read after native-base movement, `CURRENT_NATIVE_BASE` can be misread as present-tense truth even though the adjacent `database_bound_native_base` still names the old base. A standalone validator PASS cannot repair that ambiguity.

So the failure is a **layer/temporal interpretation defect**, not evidence that immutable package validation should start querying GitHub.

## Minimum successor semantics

Prefer an explicitly bound, non-indexical representation such as:

```text
database_validation_state = ACCEPTED_FOR_BOUND_NATIVE_BASE
database_bound_native_base = <sha>
database_validation_receipt = <immutable receipt identity>
native_base_change_requires_fresh_database_validation = true
```

or an exact equivalent.

Then current integration eligibility is a separate projection:

```text
if current_native_base == database_bound_native_base
    and bound receipt remains valid:
        CURRENT_FOR_TARGET
else:
        REVALIDATION_REQUIRED
```

The package validator proves the first object is internally exact. A release/currentness gate proves the second against fresh target evidence.

## Property invariants

1. Old DB validation remains historical evidence after native movement.
2. Historical receipt success never implies current-base acceptance without equality/revalidation proof.
3. Deterministic package validation does not need live GitHub access merely to preserve artifact identity.
4. Release/integration currentness must compare fresh native target identity to the receipt’s bound native base.
5. `CURRENT_*` wording inside immutable generation artifacts should be avoided unless the referent is explicitly frozen as `current_at_generation` or `current_for_bound_base`.
6. A new native-base validation creates a new bound receipt; it does not rewrite the old run.
7. A narrower invalidation policy, if ever adopted, is a governed policy change with mechanical evidence, not an inference from “small” native changes.

## Disposition

`3647 CONFIRMED_WITH_PROVENANCE_BOUNDARY`

No new bug ticket is needed beyond the existing temporal-sentinel/context defect and canonical 3647 stale-base gate. The important correction is to avoid “fixing” stale currentness by destroying valid historical validation evidence.
