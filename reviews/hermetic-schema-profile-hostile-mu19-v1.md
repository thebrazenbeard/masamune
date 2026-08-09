# Mune MU19 — Hermetic Schema Profile Hostile Review

**Assignment:** provisional `MU19 / HERMETIC_SCHEMA_PROFILE_HOSTILE`, Voss Slack 2026-08-09 10:42 EDT  
**Target:** dependency-free B12-derived schema-profile mechanism proposed for B23/H44, stripped of stale B12 semantic constants  
**Current producer parser reference:** `scripts/validate_r9a0_project.py` on Bob branch; latest reviewed blob before this artifact `41745ecbf947d110a4f7a03aa67fe3c06426376e`  
**Historical mechanism source:** B12 Rebind 17.6 validator Drive `1wKrp36nkBBqlwL19sxD1HcCbsakMiqvQ`  
**Disposition:** `PROFILE_DIRECTION_APPROVED; LITERAL_B12_ENGINE_REJECTED; CURRENT_PRODUCER_SCHEMA_ENGINE_NOT_YET_IMPLEMENTATION_APPROVED`

## Executive verdict

A dependency-free closed schema profile inside the already-admitted validator path is the right R9A0 mechanism. A third-party JSON-Schema package is unnecessary and would create a new dependency/toolchain problem for no useful semantic gain.

The literal historical B12 engine is **not** safe to copy unchanged. Its useful architecture must be hardened into an explicitly smaller machine contract, not described as “Draft 2020-12 validation” merely because the schema carries that `$schema` URI.

Required pipeline:

`STRICT_JSON_LEXICAL_ADMISSION -> ROOT_OBJECT_ADMISSION -> SCHEMA_PROFILE_DEFINITION_VALIDATION -> CONTRACT_PROFILE_VALIDATION -> MACHINE_OWNED_CROSS_FILE_INVARIANTS`

The candidate schema is never allowed to define away the validator's own mandatory semantic obligations.

## 1. Closed executable profile

### Supported types

Every validation node has exactly one explicit supported type from the admitted V1 set:

- `object`
- `array`
- `string`
- `boolean`
- `integer`
- `null`

No implicit type. Unsupported `type` values fail schema-definition admission.

`integer` is exact JSON integer semantics: Python `int` excluding `bool`. No `number` type exists unless separately implemented/admitted with an explicit finite-number contract.

### Root metadata

`$schema`, `$id`, and `title` are legal only at the schema root and are externally/machine checked where exact identity matters. Nested use fails profile admission.

### Objects

An object node requires all of:

- `type: object`;
- `additionalProperties: false`;
- `properties` as an object;
- `required` as a list of unique strings;
- exact required/property key-set equality for governed V1 objects.

Object-only keywords on scalar/array nodes fail. Every child property recursively satisfies the profile.

If a future contract truly needs optional fields, that is a profile-version decision. V1 must not smuggle optional semantics in by simply leaving a property out of `required` while still describing the object as closed.

### Arrays

V1 arrays are **const-exact only** unless a separate array vocabulary is explicitly implemented and admitted.

No silent implication of `items`, `uniqueItems`, `minItems`, `contains`, or ordering semantics. Unsupported array keywords fail.

A const array is compared with recursive JSON-type-aware equality, not Python equality.

### Scalars / const / enum

Every scalar node has explicit type. `const` and every `enum` member must be type-compatible with that declared JSON type.

Equality is recursive JSON identity:

- `true != 1`;
- `false != 0`;
- nested array/object members preserve JSON type identity;
- object key order is not semantic;
- array order is semantic.

An enum is non-empty and internally type-consistent for the declared node type.

If a governed string needs a lexical rule not represented in this profile, such as a SHA-256 shape, the validator's machine-owned invariant layer enforces it. The schema must not pretend unsupported `pattern` semantics exist.

## 2. Exact hostile matrix

### H1 — bool-as-integer

Schema:
`{type: integer, const: 1}`

Contract value:
`true`

Expected: schema type failure. Python subclassing must not admit bool as integer.

### H2 — nested bool in const array

Schema:
`{type: array, const: [1]}`

Contract:
`[true]`

Historical B12 mechanism can accept this because Python `[True] == [1]`.

Expected: const failure under recursive JSON-type-aware equality.

### H3 — omitted nested type self-weakening

Nested schema keeps:
`properties`, `required`, `additionalProperties:false`

but removes `type: object`.

Historical B12 definition checker does not descend because it only treats a node as object when `type == object`.

Expected: schema-profile definition failure for missing type. Contract validation must never reach the weakened subtree.

### H4 — wrong type with object keywords

Change nested `type: object` to `type: string` while leaving properties/required/additionalProperties.

Expected: schema-profile keyword-applicability failure, not silent ignore.

### H5 — deep unsupported keyword

Inject at arbitrary depth any of:

- `$ref`
- `pattern`
- `anyOf`
- `oneOf`
- `if/then/else`
- `items`
- `format`

Expected: typed unsupported-keyword failure at the exact path. Nothing is ignored because it happens to be deep.

### H6 — nested root metadata

Put `$schema`, `$id`, or `title` under a property node.

Expected: root-metadata-scope failure.

### H7 — duplicate / malformed required list

Hostiles:

- `required: ["x", "x"]`;
- `required: ["x", ["y"]]`;
- non-string required member;
- missing required list.

Expected: typed schema-definition failure before any `set(required)` call. No duplicate collapse and no unhashable-TypeError path.

### H8 — schema + Contract co-shrink

Delete a mandatory normative field from both `properties/required` and Contract.

Schema and Contract agree with each other.

Expected: machine-owned invariant failure. Candidate schema cannot jointly erase H33/H35/currentness/retrieval/installation obligations and self-certify the result.

### H9 — array substitution / reorder

For const array `["A","B","C"]`:

- reorder to `["B","A","C"]`;
- substitute one item;
- append/remove item.

Expected: const failure. If order is intentionally non-semantic, encode the invariant elsewhere rather than pretending const arrays are sets.

### H10 — const/enum declared-type mismatch

Examples:

- `{type: string, const: 5}`;
- `{type: integer, enum: [1, true]}`;
- empty enum.

Expected: schema-definition invalid before Contract evaluation.

### H11 — lexical duplicate JSON keys

Raw Manifest/Contract/schema bytes contain duplicate object keys at top level or nested depth.

Expected: strict lexical loader rejects before schema parsing. Last-write-wins normalization is forbidden.

Current canonical parser bug `71c1d2cd-3276-49a2-ad63-a30373ccb2f3` tracks the active defect; Bob has already begun strict-loader repair.

### H12 — non-finite JSON constants

Raw JSON contains `NaN`, `Infinity`, or `-Infinity`.

Expected: lexical failure before schema/type/const logic. Do not rely on Python's permissive default parser.

### H13 — non-object governed root

Manifest, Contract, or schema is syntactically valid JSON but root is `[]`, `null`, string, number, or boolean.

Expected: deterministic typed FAIL before semantic dereference. Current producer fail-hard is tracked as LOW `efb06484-f4db-42fe-9158-6a24c3c83255`.

### H14 — wrong nested container type

Top-level Contract is an object but `legacy_memory`, `retrieval`, `installation`, `supabase`, or `ci` is list/string/null.

Expected: profile/type failure before chained manual `.get()` operations. Same `efb06484...` malformed-structure class, no new bug count.

### H15 — stale volatile current fact hard-consted as “closure”

Schema adds exact const for a current model, assignee, provider PASS, database integration currentness, active release, confinement verdict, or similar volatile projection.

Contract validates today and becomes false later while package bytes remain unchanged.

Expected: field-classification/invariant failure. Volatile runtime/current projections do not belong as immutable candidate consts. Preserve only stable lifecycle rules or explicitly generation-bound provenance.

### H16 — unsupported lexical/semantic rule implied but not executed

Schema or documentation claims SHA pattern/format/item semantics the profile does not implement.

Expected: either add an explicitly admitted executable rule or keep the property under machine-owned invariants. A `$schema` declaration is provenance, not magical implementation.

## 3. Machine-owned invariant layer

At minimum the validator/tests independently own, outside candidate schema authority:

- exact mandatory Contract + Manifest stable field map/version;
- field temporal class: stable vs generation provenance vs receipt-overridable vs external current;
- exact logical package member set and logical control paths;
- H33 database-gate predicate vocabulary without current PASS answers;
- H35 release/install phase separation, attempt/route identity and receipt-history rules;
- accepted currentness/lane/admission architecture once MA23 closes;
- prohibited axis collapses such as standing authority vs target/capability/current PASS;
- stable no-Basic-Memory-active-route requirement;
- stable exact-head/local-only CI policy;
- generation/current provenance labeling rules.

This layer is why `Contract + schema` cannot jointly mutate themselves into a weaker contract and still PASS.

## 4. Relationship to current Bob checkpoint

Current Bob mechanical work is correctly repairing lexical duplicate/nonfinite JSON, checksum duplication, exact manifest membership/path confinement and some Manifest parity. That work does not yet establish full schema-engine approval.

The profile engine may now be implemented dependency-free in existing validator/tests because Voss approved the H44 direction. Exact successor schema field constants should still wait for B17 + MA23/MU15 + H46 field-classification closure. No path75 and no ambient package install are required.

## Final disposition

`PROFILE_DIRECTION_APPROVED` under the exact V1 meta-contract above.

`LITERAL_B12_ENGINE_REJECTED` because supported-keyword self-weakening and Python equality remain real.

`CURRENT_PRODUCER_IMPLEMENTATION_NOT_YET_APPROVED_AS_SCHEMA_ENGINE` until Bob implements the profile and the hostile suite passes on exact bytes.

No Vera-R9A0 producer byte, provider/schema/config, canonical coordination row, merge, deployment, credential, installation or protected effect was modified by MU19.