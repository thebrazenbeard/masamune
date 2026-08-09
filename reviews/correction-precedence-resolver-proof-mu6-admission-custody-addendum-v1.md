# Mune MU6 Addendum — Admission-Route Custody Is Independent from Internal Consistency

**Parent assignment:** `VOSS-20260808-MU6` / root `3464`, amendment `3665`  
**Parent final:** `reviews/correction-precedence-resolver-proof-mu6-final-v2.md`  
**Class:** read-only source/admission hostile  
**Provider/schema mutation:** none

## Finding

A structurally self-consistent evidence chain is not automatically an admitted/current chain when the write route that created it cannot be independently established.

Fresh Vera readback of `public.vera_portable_bootstrap_current` shows two rows projected as `DURABLY_BOUND`, including exact request, binding, and confirmation identities. The active CRITICAL bug `a72ef1f1-f750-4b85-bb93-9edf33d5338a` independently establishes that `service_role` held broad direct DML on the four portable-bootstrap base tables in parallel with the intended narrow RPCs, with no BEFORE INSERT admission trigger, no table-enforced transition graph, no table-enforced request-key recomputation, and no table-enforced binding-digest/freshness constraints.

For the six concrete request/binding/confirmation UUIDs from the two current `DURABLY_BOUND` chains, fresh searches found no matching custody record in:

- `public.vera_coordination_events`;
- `public.vera_save_state_events`;
- `public.vera_context_events_v3`;
- accessible public Slack search for the sampled request identity.

This absence does **not** prove direct-DML forgery. It proves the reviewed evidence is insufficient to distinguish an admitted RPC-created chain from a chain that could have been synthesized through the over-broad base-table route.

## Correct lifecycle

The resolver must separate:

1. `INTERNAL_CHAIN_CONSISTENCY` — values, digests, predecessor relations, timestamps and local formulas agree;
2. `ADMISSION_ROUTE_CUSTODY` — an independently trustworthy source proves the chain entered through an authorized/admitted write path;
3. `CURRENTNESS` — the admitted governed lineage resolves to a current controller;
4. `CALLER_PRIVACY_PROJECTION` — disclosure is minimized after internal adjudication.

Internal consistency may be `PASS` while admission-route custody is `UNAVAILABLE`.

In that state the evidence must **not** be silently promoted to `ADMITTED`, `CURRENT`, or an authority/effect-enabling state. It also must **not** be called `FORGED`, `REJECTED`, or malicious absent positive evidence.

Recommended bounded lifecycle:

`UNRESOLVED_ADMISSION_CUSTODY / REISSUE_REQUIRED`

A separately preserved historical status such as `INTERNALLY_CONSISTENT_LEGACY_CHAIN` is acceptable for provenance, but it cannot satisfy a current protected admission/currentness gate.

If later independent immutable provider/operator evidence proves the exact intended RPC custody for a specific chain, that chain may be revalidated under the applicable policy. Otherwise a fresh protected chain should be issued.

## Composition with MU6 final

This is not a portable-bootstrap special case. It is the general MU6 rule already implied by `missing admission proof != rejection`:

`RAW_OBSERVATION -> SOURCE/ROUTE CUSTODY -> ADMISSION -> TRUSTED FULL GRAPH CURRENTNESS -> PRIVACY PROJECTION`

The previous MU6 invariants therefore gain two explicit additions:

- **internal semantic/digest consistency is not admission evidence**;
- **missing route custody yields unresolved/reissue-required, not accepted-current and not rejected-forged**.

This composes with the existing source-completeness rule: if the policy requires custody evidence that is absent, currentness cannot be reported as complete even when every stored row agrees with every other stored row.

## Verdict impact

Parent verdict remains:

`PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT_AND_PRIVACY_ORDER_CORRECTION`

with this additional admission-custody requirement.

No duplicate bug was filed because `a72ef1f1-f750-4b85-bb93-9edf33d5338a` already tracks the underlying portable-bootstrap route-bypass defect.

No production row, schema, permission, provider configuration, protected branch, credential, installation, deployment, or canonical memory was modified.