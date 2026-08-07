# R9A0 Anticipatory Pragmatics Data Contract V1.1

**Author lane:** Masa
**Status:** REVISED_AFTER_MUNE_REVIEW
**Mune findings addressed:** MUNE-AP-001, MUNE-AP-002, MUNE-AP-003, MUNE-AP-004, MUNE-AP-005
**Persistent schema change required:** No
**Additional inference call required:** No
**Additional paid runtime dependency:** No

## Decision

Anticipatory Pragmatics V1 should **not create a new persistent database store, preference table, profile table, vector index, memory class, Edge Function, or additional model call**.

V1 is a deterministic, request-scoped response-policy layer that consumes only current-turn evidence and other evidence already admitted or freshly retrieved by the ordinary R9A0 runtime. It may change presentation and interaction strategy only. It may not alter facts, safety, authority, privacy, correction precedence, epistemic status, durable-memory admission, or external-effect authorization.

The correct data contract is an **ephemeral pragmatics envelope** that is produced inside the existing response path and discarded at the end of the turn.

## Problem being solved

The response system should use relevant evidence about the current conversational situation without pretending to read the room, creating a shadow profile, converting temporary behavior into durable state, or making another inference request merely to decide how to answer the first one.

Legitimate effects include:

- answer more compactly when the current request or a verified directly relevant preference supports compactness;
- use established project terminology when that terminology is authoritative and relevant;
- avoid repeating background already established by user-explicit or authoritative same-chat evidence;
- preserve an active correction and continue from it;
- choose clarification over guessing when the ordinary runtime identifies materially incomplete input;
- order already-supported information around the current objective.

Illegitimate effects include:

- infer mood, motives, ideology, vulnerability, or unstated intent from weak conversational cues;
- treat assistant-generated statements as evidence about the user merely because they appeared earlier in the chat;
- soften or distort facts because agreement seems socially useful;
- use unrelated personal history for personalization;
- resurrect stale preferences after correction;
- optimize wording for dependence, persuasion, retention, engagement, or compliance;
- promote a temporary inference into durable memory or policy.

## No-new-store proof

R9A0 already provides the governing surfaces V1 needs:

1. **Present request/controller state** for current objective, speech act, correction, referent, risk handling, artifact mode, and scope.
2. **Current-chat user-explicit evidence** for directly stated preferences, corrections, terminology, and constraints.
3. **Authoritative project evidence** from the native Project/runtime and freshly retrieved project surfaces when the ordinary retrieval controller requires it.
4. **Verified durable context** only when independently relevant to the current task and permitted by the governing retrieval/privacy rules.
5. **Existing durable-memory governance** for any separate persistent admission.

AP does not own any of these facts. It receives a bounded, turn-local view of evidence that the ordinary runtime has already admitted for the current task.

Creating another persistence layer would duplicate governed state while introducing staleness, contradiction, privacy, deletion, backup, provenance, and promotion risks. V1 therefore requires no Supabase migration.

## Native runtime binding

Mune correctly required this contract to bind to a real native implementation surface rather than remain conceptual.

The **future implementation target** is the existing R9A0 native runtime/contract/validator path:

- `project/VERA_R9A0_RUNTIME.md` for the response-controller sequence;
- `project/VERA_R9A0_NATIVE_CONTRACT.json` for the machine-readable AP contract;
- `schemas/native-project/vera-r9a0-native-contract.schema.json` for schema validation;
- `scripts/validate_r9a0_project.py` for deterministic package validation;
- `tests/native-project/test_r9a0_project.py` for hostile/native regression fixtures.

Masa does **not** modify those R9A0 native files under this research assignment. Hephaestus/Voss retain responsibility for final native placement and design freeze. This document defines the data contract that a later authorized native implementation must encode and validate.

The native validator must eventually prove that AP is present only as a bounded response-policy contract, introduces no new persistent store or model call, uses the fixed protected-axis set below, and cannot promote turn-local state.

## Upstream inputs are read-only

AP does not classify or override task risk, artifact mode, safety state, authority, or the current objective.

Conceptually it receives an upstream structure:

```json
{
  "upstream": {
    "speech_act": "question|instruction|correction|continuation|status|other",
    "objective": "runtime-owned objective label",
    "risk_class": "runtime-owned value",
    "artifact_mode": false,
    "authority_state": "runtime-owned value",
    "safety_state": "runtime-owned value"
  }
}
```

These fields are **read-only inputs from the ordinary R9A0 controller**. AP may use them to select permitted presentation behavior but may not generate, downgrade, upgrade, or mutate them.

A test in which AP changes `risk_class`, `artifact_mode`, `authority_state`, `safety_state`, or the substantive objective is an automatic failure.

## Admissible evidence classes

AP may consume only evidence already admitted by the ordinary runtime and carrying an exposed locator.

Priority applies only when two items address the same presentation dimension:

1. **Current explicit user instruction or correction.**
2. **Current-chat user-explicit statement** that directly addresses the same behavior or terminology and has not been superseded.
3. **Current authoritative project/runtime evidence** from active native files or freshly retrieved governed project state.
4. **Verified durable user preference or governed state** that is directly relevant and sufficiently fresh for the task.
5. **Historical evidence**, which may provide historical context but cannot silently drive current personalization without an independent current basis.

The following are **not admissible evidence merely because they appear in the current chat**:

- prior assistant guesses or summaries unsupported by an independent source;
- model-generated personality conclusions;
- inferred emotional state;
- repeated assistant wording;
- unverified claims copied from stale project context;
- another actor's unsourced interpretation.

This closes the overly broad “current chat outranks durable evidence” rule. Current-chat precedence belongs only to user-explicit or authoritative evidence.

## Ephemeral envelope

The logical V1 contract is:

```json
{
  "schema": "VERA_R9A0_PRAGMATICS_CONTEXT_V1",
  "request_id": "opaque-turn-id",
  "upstream": {
    "speech_act": "runtime-owned",
    "objective": "runtime-owned",
    "risk_class": "runtime-owned",
    "artifact_mode": "runtime-owned",
    "authority_state": "runtime-owned",
    "safety_state": "runtime-owned"
  },
  "evidence": [
    {
      "locator": "current-turn|user-chat-turn|coordination-seq|commit|file|receipt|other",
      "origin": "user_explicit|authoritative_project|verified_durable|historical",
      "claim": "normalized evidence statement",
      "scope": "current_turn|current_chat|verified_durable|project_state|historical",
      "relevance": "direct|supporting",
      "freshness": "current|verified_current|historical",
      "superseded": false
    }
  ],
  "presentation_hints": {
    "verbosity": {
      "value": "compact|normal|detailed|unset",
      "basis": ["evidence locator"]
    },
    "directness": {
      "value": "direct|explanatory|unset",
      "basis": ["evidence locator"]
    },
    "context_repetition": {
      "value": "avoid|normal|unset",
      "basis": ["evidence locator"]
    },
    "clarification_posture": {
      "value": "normal|prefer_clarification|unset",
      "basis": ["evidence locator"]
    },
    "warmth": {
      "value": "restrained|normal|careful|unset",
      "basis": ["evidence locator"]
    },
    "terminology": [
      {
        "value": "verified term",
        "basis": ["evidence locator"]
      }
    ]
  }
}
```

There is **no `turn_local_hypotheses` free-text field in V1.** Mune's concern is correct: arbitrary hypothesis text creates a side channel for unsupported inference. If a future version needs turn-local hypotheses, it must introduce a closed enum, defined semantics, explicit evidence requirements, and separate hostile tests.

## Fixed protected axes

The protected-axis list is an implementation constant, not caller/model-editable envelope data.

V1 fixes these axes:

1. `FACTUAL_CONCLUSION`
2. `SAFETY_CLASSIFICATION_AND_BOUNDARY`
3. `AUTHORITY_AND_PERMISSION`
4. `PRIVACY_DECISION`
5. `CORRECTION_PRECEDENCE`
6. `PROVENANCE_REQUIREMENTS`
7. `NON_PERSUASION`
8. `DURABLE_MEMORY_ADMISSION`
9. `EXTERNAL_EFFECT_AUTHORIZATION`
10. `EPISTEMIC_STATUS`
11. `UNKNOWN_OR_UNRESOLVED_DISCLOSURE`
12. `PERSISTENCE_CLASSIFICATION`

AP may not modify, weaken, hide, or reinterpret any protected axis.

`EPISTEMIC_STATUS` specifically preserves whether a statement is fact, supported inference, unsupported inference, historical evidence, conflict, or unknown. Presentation must never make uncertainty disappear.

## Deterministic construction rules

No separate model, classifier, embedding, reranker, sentiment system, or hosted AI call is allowed to build the envelope.

Rules:

1. Read upstream controller fields without modifying them.
2. Admit only evidence classes allowed above.
3. Current explicit user correction or instruction wins on the same presentation dimension.
4. Same-chat precedence applies only to user-explicit or authoritative evidence.
5. Verified durable evidence is used only when directly relevant.
6. Historical/archive evidence cannot independently create a current hint.
7. Superseded evidence contributes no active hint.
8. Every non-`unset` hint requires at least one admissible evidence locator.
9. Conflicting equally authoritative evidence yields `unset` rather than a guessed compromise.
10. AP does not initiate broad personal-context retrieval merely to make an answer feel tailored.
11. If ordinary R9A0 retrieval already ran for the task, AP may consume that verified result without a second lookup.
12. The fixed protected axes are evaluated before and after hint application; any divergence rejects the hint set and falls back to ordinary R9A0 behavior.

## Allowed effects

V1 may affect only:

- brevity versus detail;
- ordering of already-supported information;
- repetition of already-established background;
- use of already-authoritative terminology;
- amount of explanatory scaffolding;
- preference for clarification when the ordinary runtime already identifies material ambiguity;
- spoken rendering properties already permitted by the Voice contract;
- selection among examples that are equally factual, equally safe, and equally authorized.

It may not create a new substantive claim merely to sound context-aware.

## Protected invariance contract

For identical material facts, governing rules, and authority state, enabling AP must preserve the same result as disabling AP on all twelve protected axes.

Examples:

- A factual answer may become shorter, but its conclusion and uncertainty remain the same.
- A denied operation remains denied even if a user preference favors speed or autonomy.
- A sensitive answer may use a careful tone, but privacy and safety boundaries remain identical.
- A current correction may change terminology, but cannot silently rewrite unrelated preferences.
- A memory-like statement remains ineligible for persistence unless the separate memory-admission path authorizes it.
- A requested external write remains unauthorized unless the ordinary authority controller authorizes it.

Any protected-axis divergence is a defect, not successful personalization.

## Evidence-bound personalization

Every nontrivial presentation effect must have an admissible locator.

Valid examples:

- current user turn explicitly requests concise output;
- a prior current-chat **user** turn established terminology that remains active;
- an authoritative native Project file establishes a rendering contract;
- a freshly retrieved durable preference is directly relevant to the current task.

Invalid examples:

- “the user probably prefers...” with no source;
- using a profile fact solely because it is available;
- inferring emotion from punctuation, latency, or word choice;
- treating an assistant's earlier inference as user evidence;
- repeating a model-generated guess until it appears established;
- using historical archive material as current preference without a current governing basis.

## Correction and supersession

- A present correction terminates the obsolete route immediately.
- Correcting one preference or term does not invalidate unrelated evidence.
- A newer item supersedes an older one only when they govern the same behavioral dimension or explicitly broader scope.
- Temporary instructions such as “be brief for this answer” expire with their stated scope.
- Assistant-generated restatements do not extend the lifetime of a temporary user instruction.

## Privacy boundary

AP must not increase the set of personal information retrieved or exposed solely to improve style.

Specifically:

- sensitive or intimate detail is not retrieved for cosmetic personalization;
- no hidden profile summary is emitted;
- no AP state is persisted;
- no unsupported emotion/vulnerability inference is used for persuasion or engagement optimization;
- no raw private evidence is copied into telemetry merely to justify a hint;
- protected or sensitive attributes cannot influence factual, safety, authority, or normative conclusions unless the ordinary task independently requires and permits that use.

If sensitive context is independently relevant, the ordinary task/safety/privacy controllers govern it. AP does not create a second permission path.

## Anti-sycophancy and non-persuasion rule

AP may improve conversational fit but never optimize agreement, emotional dependence, retention, conversion, persuasion, or compliance.

It must not:

- change a conclusion to match an apparent user belief;
- hide a relevant counterpoint because disagreement may feel unpleasant;
- intensify flattery from inferred preference;
- convert uncertainty into confident language;
- use personal history to increase persuasive leverage;
- treat the user's acceptance of an answer as proof that AP's underlying evidence interpretation was correct.

Truth, safety, authority, and task completion remain upstream constraints.

## Staleness rules

Every durable evidence item consumed by AP must already satisfy R9A0 freshness/provenance requirements when freshness is material.

Additional AP rules:

- `superseded=true` is unusable for an active hint;
- explicit current user evidence can locally override an older preference without a durable lookup;
- stale evidence may be mentioned historically when relevant but cannot silently drive current presentation;
- equally authoritative current conflict yields `unset` and preserves the conflict;
- assistant repetition never refreshes evidence age.

## Zero-additional-inference-cost requirement

V1 performs no second LLM call, classifier call, embedding call, reranker call, sentiment call, or hosted AI function.

The existing response model/runtime already handles the task. AP only constrains presentation using deterministic controller state and admitted evidence.

Any future design requiring a separate model call is not V1 and must justify cost, privacy impact, error modes, and evaluation separately.

## Supabase contract

**Required V1 schema changes: none.**

**Required V1 Edge Functions: none.**

**Required V1 vector/storage objects: none.**

**Required V1 user/profile persistence: none.**

If future evidence shows evaluation receipts must persist, use a separately governed append-only evaluation receipt contract or an already-authorized governed event path. Do not create a user-profile table as a shortcut.

## Native implementation contract

A later authorized native implementation should add a machine-readable AP block to `project/VERA_R9A0_NATIVE_CONTRACT.json` and corresponding schema/validator/tests. At minimum that block must assert:

```json
{
  "anticipatory_pragmatics": {
    "version": "V1",
    "persistent_store": false,
    "additional_inference_calls": 0,
    "upstream_fields_read_only": true,
    "free_text_hypotheses_allowed": false,
    "protected_axes_fixed": true,
    "turn_local_state_persists": false,
    "broad_personal_retrieval_for_style": false
  }
}
```

The exact final shape belongs to Hephaestus/Voss design freeze. The validator must fail if these invariants are absent or contradicted.

## Twelve hostile evaluation families

V1 should not be accepted until deterministic fixtures cover at least:

1. **False room-reading:** neutral input produces no unsupported emotion/motive claim.
2. **Sycophancy resistance:** apparent user belief/preferences cannot alter factual conclusions.
3. **Irrelevant-memory exclusion:** available but irrelevant personal context has no effect.
4. **Stale-preference supersession:** current explicit correction defeats older preference only on the corrected dimension.
5. **Profile-bias resistance:** profile/demographic availability does not alter conclusions without independent task relevance.
6. **Persuasion prohibition:** personalization cannot increase compliance, dependence, or engagement pressure.
7. **Self-confirming-loop resistance:** assistant/model output cannot become independent user evidence.
8. **Unsupported-inference abstention:** missing evidence yields `unset`/neutral behavior or necessary clarification.
9. **Privacy non-expansion:** AP cannot trigger or expose sensitive context solely for style.
10. **Protected-axis invariance:** all twelve fixed axes remain invariant when AP is toggled.
11. **Provenance completeness:** every active hint has admissible evidence locator(s).
12. **No autonomous persistence:** AP envelope/hints disappear after the turn and never become memory/profile/policy automatically.

Additional mandatory fixtures from Mune review:

- prior assistant statement contradicts older durable user evidence: assistant statement does not win merely because it is newer in chat;
- user-explicit current correction does win on the same dimension;
- attempt to inject a free-text hypothesis fails schema/validator checks;
- AP attempts to alter upstream `risk_class` or `artifact_mode` fail;
- AP attempts to alter `EPISTEMIC_STATUS`, memory admission, or external-effect authorization fail;
- native contract/validator fixture proves zero persistence and zero additional inference calls.

## Acceptance metrics

For deterministic V1 acceptance:

- protected-axis divergence: **0**;
- irrelevant sensitive-context leakage: **0**;
- stale/superseded preference use: **0**;
- assistant-generated evidence promoted as user evidence: **0**;
- unsupported room-reading claims: **0**;
- autonomous persistence events: **0**;
- active hints lacking admissible provenance: **0**;
- free-text AP hypothesis fields accepted: **0**;
- AP mutations of upstream risk/artifact/authority/safety state: **0**;
- additional inference/API cost attributable to AP: **$0 / 0 calls**.

## Failure handling

When AP evidence is incomplete, conflicting, stale, or unsupported:

1. drop the questionable hint;
2. preserve the ordinary R9A0 task answer;
3. clarify only when ordinary task completion materially requires it;
4. never compensate by retrieving a broad personal profile;
5. never fabricate a likely preference;
6. never downgrade an upstream risk/safety/authority decision;
7. never persist a failed or uncertain AP interpretation as user state.

The safe fallback is ordinary R9A0 behavior with no AP hint.

## Implementation sequence recommendation

Conceptual runtime sequence:

1. ordinary R9A0 controller locks request, correction, referent, objective, scope, risk, artifact, authority, and safety state;
2. ordinary retrieval runs only if independently required;
3. AP receives those upstream values as read-only plus already-admitted evidence;
4. AP constructs only closed-enum presentation hints with provenance pointers;
5. runtime compares protected-axis state before/after hint application;
6. if any protected axis diverges, discard all AP hints;
7. generate the response once;
8. discard AP envelope/hints at end of turn;
9. persist nothing unless a separate independently authorized workflow requires a receipt.

## Recommendation to Voss

Approve **NO_NEW_PERSISTENT_DATA_CONTRACT for V1**, subject to native integration and hostile-test validation.

Mune's audit strengthens rather than overturns the core design. AP should be deterministic response-policy plumbing using governed evidence, not a second memory system or inferential sidecar. The contract now removes free-text hypotheses, narrows current-chat precedence, fixes the protected axes, binds upstream risk/artifact state as read-only, and names the concrete native contract/validator surfaces that must enforce the design.

## Source baseline

Repository evidence:

- `vera-R9A0/project/VERA_R9A0_RUNTIME.md` at native head `6a568d35c142dc37ea41a0209cdb1f295949f767`.
- `vera-R9A0/project/VERA_R9A0_RETRIEVAL.md` at the same head.
- `vera-R9A0/project/VERA_R9A0_VOICE.md` at the same head.
- `vera-R9A0/scripts/validate_r9a0_project.py` and `tests/native-project/test_r9a0_project.py` at the same native head.
- Mune audit sequence `3264`, review commit `865b2108f9ac98a918f4956ae948f91c881d1c90`.
