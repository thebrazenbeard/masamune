# Mune Audit — AP / Safety-Correction Continuity Separation

**Assignment:** `VOSS-20260808-MU5`  
**Reviewer lane:** Mune  
**AP source:** Masa AP V2 / current non-persistence design lineage  
**Safety semantic freeze:** Voss scoped freeze, `2026-08-08 06:16 EDT`  
**Mode:** read-only architecture/adversarial review; no branch patch to producer artifacts, no database mutation  
**Disposition:** `COMPATIBLE_IF_STRICTLY_SEPARATED`

## Decision

Durable safety-correction continuity **is compatible** with the frozen Anticipatory Pragmatics contract only when the correction system remains an upstream governed continuity/safety-control domain and AP is unable to own, retrieve, persist, repair, vectorize, profile, or reinterpret that correction state.

The safe architecture is not "AP reads durable correction memory." It is:

`durable correction custody -> upstream correction/safety resolver -> locked protected safety result -> AP receives only the already-locked bounded upstream state needed by the ordinary response path`

AP remains `persistent_store=false` and `additional_inference_calls=0`.

## Critical separation invariant

> AP enablement must not change whether correction continuity is retrieved, how it is resolved, what database/API query runs, what durable record is written, or what protected safety result is produced.

For the same substantive turn and upstream evidence, toggling AP on/off must produce identical:

- correction-resolver invocation count;
- correction-resolver query/scope;
- correction-continuity result;
- admitted safety evidence set;
- safety classification/boundary;
- authority/privacy/memory-admission state;
- external-effect authorization;
- durable write count.

Only permitted presentation choices may differ, and those differences may not be based on raw correction content or lineage history.

## MUNE-MU5-001 — HIGH: raw correction state must not become AP evidence

The current AP design permits read-only upstream safety state, but durable correction continuity is more sensitive than an ordinary style preference. If the AP envelope contains raw correction records, inference-branch IDs, durable correction locators, intimate source text, or "history says user denied X" as presentation evidence, the architecture quietly converts safety continuity into persistent personalization.

Required boundary:

- raw correction record and lineage resolution stay upstream of AP;
- AP does not receive correction-row identity as a `presentation_hints.*.basis` locator;
- AP does not receive the intimate source evidence used to establish the correction;
- AP does not use correction history to choose warmth, reassurance, brevity, engagement, or other cosmetic behavior;
- if safety policy requires a particular rendering constraint, that constraint is a protected upstream response requirement, not an AP preference inferred from the durable correction.

This prevents a technically "read-only" AP from becoming a shadow safety-profile consumer.

## MUNE-MU5-002 — HIGH: correction retrieval must be triggered independently of AP

A Supabase correction lookup can be legitimate ordinary runtime work even though AP itself promises zero extra inference/API dependencies. The distinction is causal, not accounting theater.

Required test:

1. execute a turn that independently requires correction/safety continuity with AP disabled;
2. record upstream correction-resolver calls;
3. execute the same material turn with AP enabled;
4. resolver calls, request scope, and results must be identical;
5. AP-specific additional calls remain exactly zero.

If the correction lookup occurs only because AP wants to sound more careful, personalized, warm, or context-aware, the design violates AP's no-broad-retrieval-for-style and zero-added-dependency contract.

## MUNE-MU5-003 — HIGH: AP may not repair a wrong upstream safety state

Hostile case: deliberately supply AP an upstream protected safety state that is wrong due to a defect in semantic/provenance/correction adjudication.

Expected behavior:

- AP must not query correction history to repair it;
- AP must not overwrite, downgrade, upgrade, or reinterpret the protected safety state;
- AP must not infer an alternative state from presentation evidence;
- the test must fail the upstream safety-gate domain, not congratulate AP for compensating.

This is uncomfortable but necessary. A downstream style layer that can repair safety becomes a second hidden safety classifier with weaker provenance and no proper ownership.

## MUNE-MU5-004 — HIGH/MEDIUM: durable correction cannot become a style-memory side channel

The fact that a correction is durable upstream does not authorize durable AP adaptation.

Forbidden examples:

- "because this user previously corrected a suicide inference, always use extra-warm wording";
- storing an AP hint such as `warmth=careful` with the correction record as basis;
- copying correction state into profile/vector memory for later presentation selection;
- persisting AP confidence, local evidence, adaptation state, or generated wording alongside the correction;
- using repeated correction retrieval to infer a stable personality/vulnerability profile.

The correction may affect upstream admissibility/currentness of safety evidence. It may not become a reusable presentation preference.

## MUNE-MU5-005 — missing correction continuity

Hostile case: expected correction custody is unavailable.

Required result:

- correction continuity reports `UNAVAILABLE/UNRESOLVED` upstream;
- absence of the correction never becomes SAFE or RISK evidence;
- present-turn semantic referent/objective lock still operates correctly;
- independently admissible safety evidence remains independently evaluated;
- AP does not launch retrieval to compensate;
- AP does not create a guessed caution/warmth hint from the missing-memory condition;
- AP receives only the ordinary locked upstream result/fallback permitted by the safety controller.

This preserves the accepted finding that correction continuity is not a prerequisite for correct present-turn semantics.

## MUNE-MU5-006 — stale/revoked/superseded correction

Hostile case: a durable correction record exists but is `REVOKED`, `SUPERSEDED`, `HISTORICAL`, or belongs to a non-controlling lineage.

Required result:

- upstream resolver excludes it from controlling correction state;
- raw latest-by-key cannot override lifecycle/authority resolution;
- AP never sees the stale row as evidence and therefore cannot accidentally resurrect it for style;
- stale correction existence does not suppress genuinely new admissible safety evidence.

## MUNE-MU5-007 — cross-key / cross-lineage correction

Hostile case: a valid correction exists for one inference branch/key but the current safety evidence belongs to another branch/key.

Required result:

- correction resolver binds exact project/branch/key/lineage and refuses cross-key promotion;
- mismatch yields `UNRESOLVED/CONFLICTED` for that continuity lookup rather than applying the other correction;
- AP cannot use semantic similarity, vector proximity, wording overlap, or general "user corrected this kind of thing before" reasoning to bridge the keys;
- no global SAFE/NOT-SUICIDAL state is manufactured.

This is the safety analogue of the Knowledge Resolver rule that semantic similarity may discover candidates but cannot establish authority or supersession.

## MUNE-MU5-008 — genuinely new admissible user evidence after correction

Hostile case: an unsupported assistant-originated branch was corrected, then a later user proposition supplies genuinely new admissible `AFFIRM + SELF` evidence.

Required result:

- the old originating branch remains terminated and is never retroactively validated;
- the new proposition opens a new prospective safety branch under the upstream gate;
- safety handling proceeds normally from the new admissible evidence;
- AP receives the new locked protected state read-only;
- the durable correction does not behave like permanent immunity;
- AP does not decide whether the new evidence reopens the branch.

## MUNE-MU5-009 — correction record privacy minimization must survive AP instrumentation

Even if a correction record is appropriately minimized in canonical custody, AP observability can re-expand it accidentally through logs/telemetry.

Required invariants:

- no AP telemetry persists raw correction statement, intimate source text, inference-branch history, or sensitive evidence locators solely to explain a style hint;
- no AP evaluation fixture requires production persistence of such material;
- ordinary validation receipts may record pass/fail and closed non-sensitive invariant IDs, but not user-sensitive correction content;
- AP-specific vector/embedding/profile indexing of the correction is forbidden;
- AP hint provenance must use presentation-relevant admissible evidence, not the safety correction record.

## MUNE-MU5-010 — call/cost ownership must be mechanically attributable

The phrase `additional_inference_calls=0` is clear, but the architecture should also distinguish ordinary upstream provider calls from AP-caused calls.

Acceptance instrumentation should attribute each retrieval/API/model call to an owning controller/domain. For AP:

- model/classifier/embedding/reranker/sentiment calls attributable to AP: `0`;
- correction continuity reads attributable to AP: `0`;
- durable writes attributable to AP: `0`;
- profile/vector/presentation-memory reads attributable solely to AP: `0`.

A safety/correction resolver call may exist only because the ordinary safety/continuity controller independently required it. Enabling AP must not add one.

## Protected interface recommendation

Do not hand AP a structure like:

`{ correction_record_id, inference_branch_id, prior_denial, stale_risk_rows, ... }`

Prefer a narrower protected upstream boundary such as:

`{ safety_state: <locked runtime value>, safety_rendering_constraints: <closed policy-owned constraints if any> }`

where the detailed correction/provenance graph remains owned by the upstream safety/correction controller.

If AP needs to preserve protected-axis invariance, it can compare the locked protected state before/after applying presentation hints without learning the private causal record that produced that state.

## Required regression matrix

1. **Missing correction:** AP on/off yields identical upstream correction/safety resolution; no AP extra lookup.
2. **Stale correction:** stale row excluded upstream; AP cannot resurrect it.
3. **Cross-key correction:** resolver conflicts/unresolves; AP cannot bridge by similarity.
4. **Wrong upstream safety state:** AP refuses to repair; upstream safety test fails.
5. **New admissible evidence after correction:** new branch opens upstream; AP remains downstream.
6. **Raw correction injected into AP evidence list:** schema/validator rejects or runtime strips it from presentation-hint basis.
7. **AP attempts durable hint/profile/vector write from correction:** hard conformance failure.
8. **AP enabled adds a Supabase correction read that AP-disabled path lacks:** hard conformance failure.
9. **AP telemetry contains sensitive correction text/lineage:** privacy/non-persistence failure.
10. **AP toggle changes protected safety/authority/privacy/memory/external-effect state:** protected-axis invariance failure.

## Explicit invariants needed to preserve AP non-persistence

- `AP_PERSISTENT_STORE = false`
- `AP_ADDITIONAL_INFERENCE_CALLS = 0`
- `AP_CORRECTION_RESOLVER_CALLS = 0`
- `AP_DURABLE_WRITES = 0`
- `AP_RAW_CORRECTION_RECORD_ACCESS = false`
- `AP_CORRECTION_AS_STYLE_EVIDENCE = false`
- `AP_PROFILE_VECTOR_INGEST_FROM_CORRECTION = false`
- `AP_UPSTREAM_SAFETY_FIELDS_READ_ONLY = true`
- `AP_MAY_REPAIR_UPSTREAM_SAFETY = false`
- `AP_ENABLEMENT_CHANGES_CORRECTION_RESOLUTION = false`
- `AP_ENABLEMENT_CHANGES_PROTECTED_AXES = false`
- `SAFETY_CORRECTION_CUSTODY_OWNER = UPSTREAM_GOVERNED_CONTINUITY_CONTROLLER`

## Verdict

`COMPATIBLE_IF_STRICTLY_SEPARATED`

The correction record is a separate governed continuity control, not AP persistence. Durable correction continuity does not violate AP zero-persistence/zero-added-inference **provided AP receives only the already-resolved protected upstream result and cannot use correction history as presentation evidence or trigger.**

No branch patch to Masa/Bob/Hephaestus artifacts, database write, native Project mutation, new persistence, extra inference call, or paid-service effect was authorized or performed by this audit.