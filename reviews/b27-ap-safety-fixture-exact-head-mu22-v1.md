# Mune MU22 — B27 AP + Safety Fixture Exact-Head Review

**Assignment:** `MU22 / B27_AP_SAFETY_FIXTURE_HOSTILE`  
**Immutable reviewed head:** `5361a016eb8f581b9531d094efa4956688f52b9e`  
**Expected pre-B27 base:** `1a7c77d7c7d1740ae0fe42a892622871611fc9c5`  
**Exact source bundle:** B13 V4 `0e185d67cbdedbd5a993cf8996e578ba8c9848a8dbcbee9bc07dccde391dad88`  
**Disposition:** `CHANGES_REQUESTED_SAFETY_LIFECYCLE_CURRENTNESS_ONLY`

## Mechanical verdict

Fresh GitHub compare proves `1a7c77d7... -> 5361a016...` is exactly **2 commits / 32 added paths / 0 modified / 0 deleted**. The changed set is exactly the MU22 preapproved subset:

- 12 `anticipatory_pragmatics_v1` JSON fixtures;
- 18 `safety_contamination_v1` JSON fixtures;
- `tests/native-project/test_r9a0_anticipatory_pragmatics.py`;
- `tests/native-project/test_r9a0_safety_contamination.py`.

No assignment-currentness, Contract, validator, Package, workflow, provider, receipt or other native path is touched by this aggregate checkpoint.

I independently parsed the exact B13 V4 source bundle, recomputed each expected Git blob SHA, and fresh-fetched all 32 files from immutable head `5361a016...`. **All 32 Git blob identities match the source bundle exactly.** The aggregate exact subset path digest remains:

`5b091310bc3a411ba1ae5100eebaa4bdefa951516f2cb36c169219efc71c6c6e`.

Examples of exact module identity:

- AP module expected/observed Git blob `f626dde6e089d181d421a0701959e83851932e4f`;
- safety module expected/observed Git blob `2701ca0e780721fdc3d6d4ea499b4b7e4ec22a24`.

Thus there is no producer-byte drift from the accepted B13 source. Unfortunately, exact reproduction also reproduces one semantic defect in that source. Humans have achieved deterministic bug preservation, a milestone databases were apparently waiting for.

## Semantic blocker — TRIAGED `7162f6bd...`

The exact safety module's `adjudicate_span()` checks `lifecycle_current` only for `GOVERNED_PRIOR_CONTEXT`:

- governed prior => admissible only if `historical_qualified && lifecycle_current`;
- `USER_DIRECT` => unconditional `ADMISSIBLE` after corrected/origin checks;
- `USER_RESPONSE_TO_ASSISTANT_FRAME + AFFIRM` => unconditional `ADMISSIBLE`.

`resolve()` then promotes any `ADMISSIBLE + SELF + SAFETY_HARM + risk_bearing` span into `self_risk_evidence_ids`.

Therefore both hostiles fail open:

1. `origin=USER_DIRECT`, `lifecycle_current=false`, SELF/SAFETY_HARM/risk-bearing => admitted/current risk evidence;
2. elicited `USER_RESPONSE_TO_ASSISTANT_FRAME + AFFIRM`, `lifecycle_current=false`, SELF/SAFETY_HARM/risk-bearing => admitted/current risk evidence.

This is canonical TRIAGED MEDIUM `7162f6bd-bd16-4489-aecd-ac82f63d2fa5 / R9A0-SAFETY-FIXTURE-LIFECYCLE-FAILOPEN-001`.

The defect is not assignment-currentness semantics and does not reopen AP/currentness architecture. It is source-evidence lifecycle handling inside the safety gate itself: evidence explicitly marked non-current cannot be promoted as current SELF risk evidence merely because origin/stance is otherwise admissible.

## Precheck correction

MU22 precheck V1 said no newer source-typing rule semantically superseded the exact safety module. That conclusion was too strong. The exact bytes do preserve B13 semantics, but B13 itself omitted lifecycle-current enforcement for two positive-origin branches.

Corrected rule:

- `lifecycle_current=false` prevents the span from contributing **current** SELF safety-risk evidence regardless of USER_DIRECT / elicited AFFIRM / governed-prior origin;
- corrected or assistant-origin/nonaffirming provenance rules remain independently enforced;
- positive current USER_DIRECT and current elicited AFFIRM remain admissible controls;
- historical governed evidence still additionally requires `historical_qualified=true`;
- lifecycle staleness does not retroactively rewrite origin provenance or claim the historical statement never existed. It only blocks current-risk promotion under this gate.

## Required same-scope repair

Keep the existing B27 scope. No path expansion is necessary.

At minimum add two negative fixtures and matching positive controls, or equivalent inline hostiles, inside the already-admitted safety fixture/module path set:

- stale USER_DIRECT SELF/SAFETY_HARM/risk-bearing => not current self-risk;
- stale elicited AFFIRM SELF/SAFETY_HARM/risk-bearing => not current self-risk;
- current USER_DIRECT same semantic shape => positive;
- current elicited AFFIRM same semantic shape => positive.

The adjudicator should consume lifecycle currentness before returning a state that can enter current self-risk. Exact representation (`INADMISSIBLE` versus another closed non-current disposition) must remain consistent with the accepted safety gate Contract field vocabulary when that Contract packet lands; do not invent a new result enum solely for this patch.

Do **not** modify AP semantics, Contract/currentness semantics, or add soft-PASS/default logic to compensate for the still-missing Contract `safety_semantic_gate` subtree.

## AP verdict

`APPROVED` at `5361a016...` for exact bytes and semantics. All 12 AP fixtures + AP module match source exactly, and no newer accepted rule was found that invalidates their presentation-only protected-axis semantics.

## Safety verdict

`CHANGES_REQUESTED` solely for `7162f6bd...` lifecycle staleness. All other reviewed provenance/referent/correction/retrieval/AP-lock semantics remain accepted at this head.

## Final B27 verdict

`CHANGES_REQUESTED_SAFETY_LIFECYCLE_CURRENTNESS_ONLY`.

After Bob produces a same-scope non-force repair head, MU22 should fresh-review the immutable successor head, verify no path pressure/semantic drift, and require stale-direct + stale-affirm negatives plus current positives to pass once their stable Contract dependency is available.

No Vera-R9A0 producer byte, provider/schema/config, canonical coordination state, merge, deployment, credential, installation or protected effect was modified by MU22.