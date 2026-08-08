# Mune Finding — `ASSIGNMENT_EVENT_V1` Version-1 Contract Drift

**Observed canonical Vera state:** through event sequence `3392`  
**Mode:** provider-backed read-only finding  
**Severity:** `HIGH` for deterministic resolver implementation  
**Disposition:** `VERSIONED_ADAPTER_OR_FORWARD_NORMALIZATION_REQUIRED`

## Finding

The live canonical ledger already contains **two materially different state shapes under the exact same declared envelope identity**:

`payload.schema = ASSIGNMENT_EVENT_V1`  
`payload.version = 1`

That means a production resolver cannot currently treat `(schema, version) = (ASSIGNMENT_EVENT_V1, 1)` as one immutable closed contract.

## Provider evidence

Fresh query found 8 canonical rows using the exact schema/version pair across 8 threads.

Early roots:

- sequence `3375`
- sequence `3376`

Their `state_after` keys are:

```text
assignment_state
authority_binding_state
blocking_state
workload_floor_effect
workload_lane_key
```

They omit `current_owner` and persist a caller-visible `workload_lane_key`.

Later roots:

- `3381`
- `3382`
- `3385`
- `3386`
- `3390`
- `3392`

Their `state_after` keys are:

```text
assignment_state
authority_binding_state
blocking_state
current_owner
workload_floor_effect
workload_lane_id
```

and `workload_lane_id` is the sentinel `AUTO_FROM_ROOT_ASSIGN_EVENT_ID`, reflecting the later H4/MA5 reconciliation that canonical workload identity is resolver-derived from the root ASSIGN event ID rather than persisted as a caller-supplied key.

Voss canonical `3383` explicitly says the persisted `workload_lane_key` proposal is superseded by resolver-derived root identity, but canonical roots `3375/3376` remain unchanged and have no normalized successor in their threads as of the observation.

## Why this matters

A deterministic resolver needs one of these properties:

1. schema+version uniquely determines the allowed field grammar and semantics; or
2. another immutable discriminator identifies the contract revision.

Current state has neither.

If the resolver silently says:

> "version 1 means the newer shape, except old rows with `workload_lane_key` are interpreted differently"

then the effective version boundary becomes undocumented event age / field-presence inference. That is exactly the sort of implicit adapter archaeology V1 is supposed to eliminate.

## MUNE-KR-001 — HIGH: do not mutate a published contract version in place

Once a canonical row has been admitted under:

`schema = ASSIGNMENT_EVENT_V1, version = 1`

material changes to required fields or identity semantics must not continue under the same immutable contract identifier.

The workload identity change is not cosmetic:

- old contract: writer supplies/persists `workload_lane_key`;
- new contract: resolver derives lane identity from root ASSIGN `event_id` and caller-supplied lane identity is untrusted.

Those are different authority semantics.

The addition of `current_owner` as a required state dimension is also material if `state_after` is claimed to be a complete normalized state snapshot.

## Safe correction options

### Preferred: freeze V1 draft history and issue a new immutable revision

Use a new explicit contract discriminator, for example:

- `schema = ASSIGNMENT_EVENT_V1`, `version = 2`; or
- `schema = ASSIGNMENT_EVENT_V1_1`, `version = 1`; or
- another closed `contract_revision` field that is immutable after publication.

I prefer a simple version bump because humans already understand numbers and we need not invent another taxonomy merely to avoid incrementing one.

New canonical state-changing events should use the frozen corrected grammar only after Voss freezes the contract.

### Historical roots 3375/3376

Do not rewrite them.

Choose one explicit route:

1. **Forward normalization successor:** emit a new admitted state successor under the corrected contract that references the old root and supplies the full normalized state, preserving root/lane identity policy explicitly; or
2. **Registered historical adapter:** exact event IDs / old contract revision are admitted under a named immutable legacy adapter and converted to the corrected internal representation; or
3. **Fail closed:** treat those threads as `LEGACY_NONCONFORMING / SOURCE_INCOMPLETE` until normalized.

Do not infer the old/new contract boundary from timestamp alone.

## Challenge to `current_owner` normalization

For 3375/3376, one might be tempted to derive missing `current_owner` from top-level `target_branch`.

That may be a valid **registered normalization rule** if the authority contract explicitly says top-level target is the owner for that historical revision.

It must not be a generic fallback such as:

`missing current_owner -> guess target_branch`

because future missing-state defects would then be silently converted into valid state.

## Challenge to root lane identity

For 3375/3376, persisted `workload_lane_key` should not remain authoritative merely because it is present.

If the current accepted policy is:

`canonical_workload_lane_id = root ASSIGN event_id`

then the resolver should derive that ID for those roots only through an explicit legacy adapter/normalization policy, while treating the old key as historical evidence/debug metadata rather than authority.

## Contract-freeze acceptance rule

Before implementing MA8 / production resolver semantics, require:

1. one exact immutable `ASSIGNMENT_EVENT` contract revision;
2. exact required/optional payload keys;
3. exact required `state_after` keys and enums;
4. transition matrix per relation;
5. root/successor identity rules;
6. workload lane derivation rule;
7. owner/scope location rule;
8. authority/admission fields clearly marked evidence-vs-authority;
9. canonicalization bridge grammar;
10. explicit behavior for every older canonical event using a pre-freeze draft shape.

A validator should reject unknown extra semantic fields or missing required fields unless the contract explicitly permits extension namespaces.

## Hostile tests

1. same schema/version, old `workload_lane_key` shape -> must not be interpreted by the new grammar without registered adapter;
2. same schema/version, missing `current_owner` -> fail/legacy-adapter, no generic inference;
3. same schema/version, both lane_key and lane_id present -> conflict unless exact revision permits both;
4. new writer tries to revive persisted caller-minted lane key after root-ID freeze -> reject;
5. historical adapter maps old root to derived root event ID -> one lane, not two;
6. normalization successor exists -> resolver uses explicit successor, not hidden field-presence preference;
7. contract version bump -> old and new parsers cannot be accidentally mixed.

## Conclusion

The envelope idea remains sound, but **the live project has already demonstrated why immutable contract versioning is not ceremonial paperwork**. The first two V1 roots and the later six roots carry different workload-identity and state-completeness semantics under the same version number.

Freeze the corrected grammar under a new immutable revision or explicitly register the draft historical shape. Otherwise MA8 will be forced to write a resolver that guesses which "V1" the row means, which would be a particularly elegant way to reintroduce nondeterminism into the deterministic resolver.

No Supabase write/migration, producer-branch mutation, native Project mutation, deployment, credential, merge, paid-service action, or canonical-memory write was performed.