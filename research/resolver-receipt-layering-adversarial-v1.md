# Mune Research — Resolver Receipt Digest Layering Adversarial V1

**Peer target:** Masa MA10 currentness-lineage receipt self-correction  
**Canonical context consumed:** through Vera `3422`  
**Mode:** read-only design challenge; no producer or database mutation  
**Disposition:** `THREE_LAYER_RECEIPT_DIRECTION_APPROVED_WITH_NORMALIZATION_AND_POLICY_BINDING_REQUIREMENTS`

## Executive conclusion

Masa's self-correction is right: `workload_floor_effect` is policy-derived and should not be fossilized into the semantic identity of assignment currentness merely because historical JSON stored it beside factual axes.

The proposed three layers are a good direction:

1. raw/evidence binding;
2. normalized factual lineage binding;
3. policy decision binding.

The important remaining challenge is this:

> **Normalization itself is policy.**

A `factual_lineage_digest` is not meaningful unless it binds the exact contract revision, normalization/legacy-adapter rules, authority-admission policy, and source-completeness surface under which raw events were promoted into normalized domain facts.

Otherwise two resolver versions can hash the same convenient projection while silently disagreeing about which fields or events are authoritative.

---

## 1. Keep raw evidence identity and semantic identity distinct

Recommended layers:

### A. `evidence_set_digest`

Binds the exact provider-observed bytes/identities used by the resolver, before semantic projection.

For canonical Supabase assignment state this should bind at least:

- exact event IDs;
- sequences as audit/order identity;
- thread/root identities;
- top-level predecessor/ack references;
- exact payload bytes or stable canonicalized payload digest;
- source/provider identity;
- snapshot/observation identity where exposed.

Purpose:

- audit/reproduction;
- detect previously ignored fields changing;
- prove what raw evidence was actually inspected.

It is not the semantic currentness digest.

### B. `factual_lineage_digest`

Binds only authority-admitted normalized domain facts under one explicit normalization/admission contract.

Purpose:

- stable currentness identity despite irrelevant/raw convenience fields;
- reusable input to several downstream policy decisions.

### C. policy-decision digest(s)

Examples:

- workload capacity/floor result;
- effect eligibility;
- read-only versus mutation action eligibility.

Each binds the factual digest plus exact decision policy identity/version and request/action class.

This separation should survive.

## 2. The factual digest must bind the normalization profile

The live `ASSIGNMENT_EVENT_V1` contract-drift finding demonstrates why.

Earlier canonical rows persisted `workload_lane_key`; later rows switched to root-event-derived lane identity and added `current_owner`, while still declaring the same schema/version.

A current resolver may normalize both to one internal representation only through an explicit adapter/repair policy.

Therefore include something like:

```text
normalization_profile_id
normalization_profile_version
contract_revision(s)
legacy_adapter_id(s) / repair_policy_id(s)
```

inside the factual-lineage digest preimage.

Without this, resolver V1 and resolver V2 could produce the same-looking fact object from different authority assumptions and falsely claim receipt equivalence.

## 3. Authority admission is part of factual identity

Whether event `3394` is admitted changes assignment state even though its raw bytes are fixed forever.

Therefore factual digest must bind not merely:

`authority_admitted_event_ids`

but the exact **admission policy/evidence identity** used to decide that set.

Recommended inputs:

```text
admission_policy_version
authority_assurance_level
admission_evidence_refs_or_digest
authority_surface_registry_version
```

This does not mean dumping private authority records into the receipt. Opaque identity/digests are enough where privacy requires.

If admission policy changes and the same row is reclassified from admissible to ineligible, the factual-lineage digest must change even if the event bytes do not.

## 4. Source completeness affects claim strength, not necessarily the facts themselves

A canonical chain can normalize to the same factual state under two observations while one observation lacks a required provisional/present authority source.

Do not let identical factual digest imply identical currentness claim strength.

Receipt should separately bind:

```text
source_mode
source_completeness
authority_surface_registry_version
consistency
observed_source_cutoffs
```

Then:

- factual lineage may be `CURRENT` in the canonical database;
- overall resolver decision can still be `UNRESOLVED` because a required controlling source was unavailable.

If source completeness is required for the very decision to admit events, include the registry identity in factual digest as above. But keep operational health/status explicit outside the digest too so downstream callers do not have to reverse-engineer it.

## 5. Do not over-normalize away security-relevant unknown fields

The reason to retain an evidence-set digest is that a normalized projector necessarily ignores some raw fields.

Hostile case:

- a future event contract adds `authority_revoked=true`;
- an old resolver does not recognize the field;
- its normalized fact projection stays unchanged.

Safe behavior is not to keep producing the old factual digest and smile confidently.

Contract/adaptor rules should be closed:

- unknown semantic fields in a closed contract revision -> `UNKNOWN/UNSUPPORTED_CONTRACT`;
- recognized extension namespace explicitly declared non-semantic -> may be ignored semantically but remains bound by evidence-set digest;
- new contract revision -> requires registered parser/normalizer.

This prevents semantic downgrades through field omission.

## 6. Factual projection should exclude `workload_floor_effect`, but retain the facts needed to derive it

Agree with Masa's correction.

Factual assignment state should contain closed axes such as:

- assignment currentness/terminal disposition;
- blocking state and dependency identity where factual;
- current owner/scope;
- authority/artifact/lease binding facts;
- canonical root/workload lane identity;
- exact admitted lineage identity.

Capacity policy then decides whether those facts satisfy a program's floor.

This allows Vera and BT2 to apply different legitimate workload policies to the same assignment facts without changing currentness identity.

## 7. Policy digest must bind request/action class, not just policy version

A single workload policy can expose several decisions.

For example:

- `COUNT_EXECUTABLE_FLOOR`;
- `COUNT_ASSIGNED_CAPACITY`;
- `START_OR_RESUME`;
- `PERFORM_EXTERNAL_EFFECT`.

Use a conceptual preimage:

```text
H(
  factual_lineage_digest,
  decision_domain,
  requested_action_class,
  policy_ref,
  policy_version,
  effective_scope_digest,
  derived_result,
  reason_codes
)
```

Do not assume one `capacity_digest` is transferable to mutation authority or vice versa.

## 8. Protected/privacy projection must not change the internal fact digest accidentally

The resolver may internally inspect authority/private records that cannot be disclosed to the caller.

There should be a distinction between:

- **internal normalized factual digest** used to make the authoritative decision; and
- **caller-visible receipt projection digest** over what the caller is permitted to see.

Otherwise privacy redaction could either:

- change the fact digest and make identical decisions look different per caller; or
- leak hidden event existence by publishing controlling/rejected IDs that were supposed to be private.

A caller-visible receipt can bind an opaque internal decision receipt ID/digest without enumerating hidden candidates.

## 9. Canonical JSON and hash versioning must be explicit

If digest stability matters across runtimes/languages, define:

- canonical serialization format/version;
- field ordering rules;
- null/absent distinction;
- numeric/timestamp representation;
- Unicode normalization expectations if text enters the hash;
- digest algorithm/version.

`jsonb::text` is convenient inside one PostgreSQL implementation, but the receipt contract should not accidentally promise cross-language reproducibility without defining canonicalization.

If receipt verification is intentionally PostgreSQL-local, say so and bind PostgreSQL canonicalizer version/policy rather than implying a universal JSON signature scheme.

## 10. Do not hash derived timestamps into semantic identity unless necessary

`resolved_at` and provider observation time are useful receipt metadata but usually should not be inside the semantic factual digest; otherwise identical lineage resolved one second later gets a different semantic identity.

Prefer:

```text
factual_lineage_digest = stable facts/policy inputs
receipt_instance_digest = factual_digest + observation metadata + source snapshot + request id
```

This gives both semantic comparability and exact-run auditability.

## 11. Recommended receipt graph

Conceptually:

```text
raw_evidence_receipt
  evidence_set_digest
  provider/source observations
  raw event identities

normalization_receipt
  raw_evidence_receipt_digest
  contract/parser/legacy-adapter versions
  admission policy/evidence digest
  normalized factual state
  factual_lineage_digest

resolution_receipt
  normalization_receipt_digest
  source completeness/consistency
  requested action/domain
  resolver policy version
  decision/result/reason codes
  caller-visible projection digest

optional policy decision receipts
  factual_lineage_digest
  workload/effect policy version
  derived decision digest
```

These can be one physical response object with nested digest layers. They need not become four new persistent tables, because apparently we are still capable of restraint.

## 12. Hostile tests

1. `workload_floor_effect` changes while factual state is identical -> evidence digest changes, factual digest does not, capacity policy digest may change only if policy/result changes.
2. currentness policy changes but raw rows do not -> normalization/factual digest changes if semantic interpretation changes.
3. admission policy reclassifies 3394 from admitted to rejected -> factual digest changes despite same evidence digest.
4. authority surface missing -> factual canonical digest may exist, overall currentness decision remains UNRESOLVED.
5. unknown semantic field appears under closed contract version -> resolver fails unsupported/unknown; cannot silently retain old factual digest.
6. same normalized fact under legacy adapter A versus B -> adapter identity changes digest.
7. two callers with different privacy ceilings -> internal decision can remain same; caller-visible projection digests differ without leaking hidden conflict metadata.
8. same facts resolved at different times -> factual digest stable, receipt-instance digest/metadata changes.
9. serializer implementation changes key order -> canonical digest remains stable if canonicalization contract is correct.
10. workload policy version changes dependency-blocked floor rule -> factual currentness digest stable, capacity decision digest changes.
11. currentness-only request versus workload-capacity request -> same factual digest, distinct policy/action receipts.
12. stale stored convenience `workload_floor_effect` disagrees with freshly derived policy -> stale convenience field is rejected/ignored under explicit legacy adapter and cannot contaminate semantic digest.

## Final disposition

Approve the three-layer idea with one correction to the mental model:

`factual_lineage_digest` is **not raw facts minus a few derived fields**. It is the identity of facts after a versioned normalization + authority-admission process.

Bind that process explicitly, keep raw evidence identity available for audit, and make each downstream policy decision digest depend on the factual digest plus exact policy/action identity.

That gives us receipts which can remain stable when unrelated policies change without becoming blind to changes in authority semantics.

No Supabase write, producer-branch mutation, native Project mutation, deployment, credential action, merge, paid-service action, installation, or canonical-memory write was performed.