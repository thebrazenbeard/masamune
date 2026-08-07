# R9A0 Anticipatory Pragmatics Data Contract V2

**Author lane:** Masa
**Status:** CORRECTION_CANDIDATE_READY_FOR_MUNE_REREVIEW
**Supersedes as review target:** `design/R9A0_ANTICIPATORY_PRAGMATICS_DATA_CONTRACT_V1.md` V1/V1.1
**Persistent schema change required:** No
**Additional inference calls:** 0
**Edge Function required:** No
**Paid runtime dependency:** None

## Normative composition

This V2 candidate consists of this controlling delta plus the fully revised V1.1 data contract at the same immutable `masa` head. If wording conflicts, V2 controls.

## Core decision

Mune approved the no-new-store direction and V2 preserves it.

Anticipatory Pragmatics V1/V2 remains a deterministic, turn-local response-policy layer. It consumes only upstream runtime state and already-admitted evidence. It may change presentation, but it may not change substantive truth, safety, authority, privacy, correction precedence, epistemic status, memory admission, persistence classification, or external-effect authorization.

No new Supabase schema, profile table, memory store, vector store, Edge Function, classifier, reranker, sentiment model, or second LLM call is required.

## Mune findings disposition

### MUNE-AP-001: overly broad current-chat precedence

**Resolved.** Current-chat evidence receives precedence only when it is user-explicit or authoritative.

Admissible evidence priority, only when two items govern the same presentation dimension:

1. present explicit user instruction or correction;
2. same-chat user-explicit statement that is still active;
3. current authoritative project/runtime evidence from active native files or freshly retrieved governed state;
4. verified durable user preference or governed state that is directly relevant and sufficiently fresh;
5. historical evidence, which may support historical context but cannot silently drive current personalization.

A prior assistant guess, model-generated personality claim, inferred emotion, repeated assistant wording, or unsourced actor interpretation does not become stronger merely because it is newer in the chat.

### MUNE-AP-002: free-text `turn_local_hypotheses`

**Resolved by removal.** V2 permits no free-text hypothesis channel.

The V2 envelope contains only closed-enum presentation hints with explicit evidence locators. If a future version needs turn-local hypotheses, it must introduce a separately reviewed closed enum with exact semantics, evidence requirements, expiry, and hostile tests.

### MUNE-AP-003: mutable/incomplete protected axes

**Resolved with a fixed implementation constant.** AP cannot edit or supply this set.

The twelve protected axes are:

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

Any AP-induced divergence on any protected axis causes the entire AP hint set to be discarded for that turn.

`EPISTEMIC_STATUS` preserves whether a statement is fact, supported inference, unsupported inference, conflict, historical evidence, or unknown. AP may not convert uncertainty into apparent certainty.

### MUNE-AP-004: conceptual controller not bound to native surfaces

**Resolved at the data-contract layer.** A later authorized implementation must bind AP into the existing R9A0 native contract and validator surfaces:

- `project/VERA_R9A0_RUNTIME.md`
- `project/VERA_R9A0_NATIVE_CONTRACT.json`
- `schemas/native-project/vera-r9a0-native-contract.schema.json`
- `scripts/validate_r9a0_project.py`
- `tests/native-project/test_r9a0_project.py`

Masa's current assignment is research/design only, so these native R9A0 files are not modified here. Hephaestus and Voss retain final native placement/design-freeze responsibility.

A later native contract must machine-assert at least:

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

The exact final JSON shape remains Voss/Hephaestus territory, but these invariants are normative.

### MUNE-AP-005: risk/artifact fields not explicitly upstream read-only

**Resolved.** AP does not classify or modify risk, artifact mode, authority, safety state, objective, or speech act.

Those arrive from the ordinary runtime as read-only upstream values:

```json
{
  "upstream": {
    "speech_act": "runtime-owned",
    "objective": "runtime-owned",
    "risk_class": "runtime-owned",
    "artifact_mode": "runtime-owned",
    "authority_state": "runtime-owned",
    "safety_state": "runtime-owned"
  }
}
```

If AP changes any upstream field, the implementation fails validation.

## V2 ephemeral envelope

The AP-owned portion is limited to admitted evidence and presentation hints:

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
    "verbosity": {"value":"compact|normal|detailed|unset","basis":["locator"]},
    "directness": {"value":"direct|explanatory|unset","basis":["locator"]},
    "context_repetition": {"value":"avoid|normal|unset","basis":["locator"]},
    "clarification_posture": {"value":"normal|prefer_clarification|unset","basis":["locator"]},
    "warmth": {"value":"restrained|normal|careful|unset","basis":["locator"]},
    "terminology": [{"value":"verified term","basis":["locator"]}]
  }
}
```

Every non-`unset` hint requires at least one admissible evidence locator. Equal-authority conflict yields `unset`, not guessed personalization.

## Deterministic runtime sequence

1. ordinary R9A0 controller locks request, referent, correction, objective, scope, risk, artifact, authority, and safety state;
2. ordinary retrieval runs only if independently required;
3. AP receives upstream values as read-only plus already-admitted evidence;
4. AP constructs only closed-enum presentation hints with provenance pointers;
5. protected-axis state is compared before/after hint application;
6. any protected-axis divergence discards all AP hints;
7. one response generation occurs;
8. AP envelope/hints expire at end of turn;
9. nothing is persisted unless an entirely separate authorized workflow requires a receipt.

## Required hostile tests

V2 requires deterministic fixtures proving:

- explicit current user correction defeats stale preference only on the same dimension;
- prior assistant statement does not outrank older verified user evidence merely because it is newer in chat;
- assistant repetition cannot refresh evidence age;
- irrelevant sensitive context does not affect output;
- unsupported mood/motive inference does not appear;
- apparent user belief does not alter factual conclusion;
- free-text hypothesis injection is rejected;
- AP cannot alter `risk_class`, `artifact_mode`, `authority_state`, or `safety_state`;
- AP cannot alter memory admission or external-effect authorization;
- AP cannot change fact/inference/unknown epistemic status;
- AP toggle preserves all twelve protected axes;
- every active hint has admissible provenance;
- turn-local state disappears after the turn;
- no new persistence, vector, Edge, classifier, or second-model dependency is introduced;
- native contract/schema/validator/tests assert zero persistence and zero additional inference calls.

## Acceptance metrics

Required V2 acceptance results:

- protected-axis divergence: `0`;
- irrelevant sensitive-context leakage: `0`;
- stale/superseded preference use: `0`;
- assistant-generated material promoted as user evidence: `0`;
- unsupported room-reading claims: `0`;
- autonomous persistence events: `0`;
- active hints without admissible provenance: `0`;
- accepted free-text hypothesis fields: `0`;
- upstream risk/artifact/authority/safety mutations by AP: `0`;
- additional AP inference/API calls: `0`;
- added AP runtime cost: `$0`.

## Failure fallback

When evidence is incomplete, stale, conflicting, or unsupported:

1. drop the questionable hint;
2. preserve ordinary R9A0 behavior;
3. clarify only when ordinary task completion materially requires it;
4. do not retrieve a broad personal profile for cosmetic tailoring;
5. do not fabricate a likely preference;
6. do not weaken upstream risk/safety/authority state;
7. do not persist an uncertain AP interpretation.

## Current implementation decision

V2 is a **data-contract candidate only**. No R9A0 native implementation write is authorized by this assignment.

The no-new-store decision remains approved at the design level, subject to Mune V2 rereview, Hephaestus native-architecture work, Bob's deterministic harness packet, Vera external audit, and Voss final design freeze.

## Provenance

- Source Masa candidate head: `d8e173c1c13c788c7eb9946bd4af25e44b488dfb`
- Mune audit sequence: `3264`
- Mune review commit: `865b2108f9ac98a918f4956ae948f91c881d1c90`
- Revised V1.1 commit: `a79b1dea515569254fd49a885564c554481027e4`
- Voss correction assignment: `3268`
