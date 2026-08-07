# R9A0 Anticipatory Pragmatics Data Contract V1

**Author lane:** Masa
**Status:** PROPOSAL_READY_FOR_ADVERSARIAL_REVIEW
**Persistent schema change required:** No
**Additional inference call required:** No
**Additional paid runtime dependency:** No

## Decision

Anticipatory Pragmatics V1 should **not create a new persistent database store, preference table, profile table, vector index, or memory class**.

V1 is a deterministic, request-scoped policy layer that consumes only context the runtime already has or has already retrieved for the current task. It may influence presentation and interaction strategy, but it may not alter factual conclusions, safety decisions, authority, privacy boundaries, correction handling, or persistent memory admission.

The smallest correct data contract is therefore an **ephemeral pragmatics envelope**, produced and consumed inside the existing response path and discarded at the end of the turn.

## Problem being solved

The response system should use relevant evidence about the current conversational situation without pretending to read the room, converting temporary behavior into a permanent profile, or making a second inference request merely to decide how to answer the first one.

Examples of legitimate effects:

- answer more compactly when the current request and verified preference support compactness;
- reuse established project terminology when it is relevant;
- avoid repeating background already established in the current thread;
- preserve an active correction and continue from it;
- choose clarification over guessing when speech/input is incomplete;
- order the answer so the user's immediate decision comes first.

Examples of illegitimate effects:

- infer mood, motives, ideology, vulnerability, or intent without evidence;
- soften or distort facts because agreement seems socially useful;
- use unrelated personal history to personalize an answer;
- preserve a stale preference after explicit correction;
- optimize wording to increase dependence, persuasion, engagement, or compliance;
- promote a temporary inference into durable memory.

## No-new-store proof

R9A0 already provides the necessary governing surfaces:

1. **Immediate turn/chat context** for directly stated preferences, corrections, referents, and conversational sequence.
2. **Retrieval controller** for history-sensitive claims that require fresh evidence from Supabase, GitHub, Drive, or native Project files.
3. **Voice contract** for rendering behavior such as pacing, compactness, low filler, calibrated warmth, correction uptake, and distinguishing inference from fact.
4. **Existing durable-memory governance** for any separate, explicitly authorized persistent admission.

Anticipatory Pragmatics does not need to own any of those facts. It only needs a turn-local summary of which already-authorized evidence is relevant to presentation.

Creating another persistence layer would create new staleness, contradiction, privacy, deletion, backup, provenance, and promotion problems while duplicating data already governed elsewhere. V1 therefore requires no Supabase migration.

## Deterministic input contract

The envelope may be constructed only from inputs already available to the current response process:

```json
{
  "schema": "VERA_R9A0_PRAGMATICS_CONTEXT_V1",
  "request_id": "opaque-turn-id",
  "task": {
    "speech_act": "question|instruction|correction|continuation|status|other",
    "objective": "short task label",
    "risk_class": "ordinary|sensitive|high_stakes",
    "artifact_mode": false
  },
  "evidence": [
    {
      "locator": "current-turn|chat-turn|coordination-seq|commit|file|receipt|other",
      "claim": "normalized evidence statement",
      "scope": "current_turn|current_chat|verified_durable|project_state",
      "relevance": "direct|supporting",
      "freshness": "current|verified_current|historical",
      "superseded": false
    }
  ],
  "presentation_hints": {
    "verbosity": "compact|normal|detailed|unset",
    "directness": "direct|explanatory|unset",
    "terminology": ["verified project/user terms only"],
    "context_repetition": "avoid|normal",
    "clarification_threshold": "normal|high",
    "warmth": "restrained|normal|careful"
  },
  "protected_axes": [
    "factuality",
    "safety",
    "authority",
    "privacy",
    "correction",
    "provenance",
    "non_persuasion"
  ],
  "turn_local_hypotheses": [
    {
      "kind": "presentation_only",
      "value": "example hypothesis",
      "basis": ["evidence locator"],
      "confidence": "low|medium|high",
      "expires": "END_OF_TURN"
    }
  ]
}
```

This is a logical contract, not a requirement to serialize JSON in the production prompt. The implementation may represent it more compactly as long as tests can prove the same invariants.

## Deterministic construction rules

No separate model call is allowed to build this envelope.

Use rule-based extraction from already exposed context:

1. Current explicit instruction or correction outranks all prior preferences.
2. Current-chat evidence outranks older durable evidence when both address the same behavior.
3. Verified durable evidence may be used only when directly relevant to the current task.
4. Historical/archive evidence may not produce a current personalization hint without an independent current basis.
5. Superseded evidence contributes no active hint.
6. A hint that lacks an exposed locator is dropped.
7. A turn-local hypothesis may affect presentation only and always expires at end of turn.
8. No hint may modify a protected axis.
9. Anticipatory Pragmatics itself does not trigger broad personal-context retrieval merely to make an answer feel tailored.
10. If the task already requires retrieval under the R9A0 retrieval controller, AP may consume the resulting verified evidence without initiating another lookup.

## Allowed effects

V1 may affect only these response dimensions:

- brevity versus detail;
- ordering of already-supported information;
- whether to repeat known background;
- use of already-established terminology;
- degree of explanatory scaffolding;
- whether a concise clarification is preferable to an unsupported assumption;
- spoken rendering properties already permitted by the Voice contract;
- selection among equally factual, equally safe examples.

## Protected invariants

The output **with** Anticipatory Pragmatics and the output **without** it must remain invariant on:

1. factual conclusion;
2. safety classification and boundary;
3. authority/permission determination;
4. privacy decision;
5. correction precedence;
6. source/provenance requirements;
7. whether evidence is fact or inference;
8. whether durable memory admission is authorized;
9. whether an external write is authorized;
10. whether a user must be told that information is unknown or unresolved.

A pragmatics hint that changes any protected result is a defect, not clever personalization.

## Evidence-bound personalization

Every nontrivial personalization effect must have an evidence pointer.

Valid examples:

- `current-turn`: user asks for a concise answer;
- `current-chat turn 42`: user corrected terminology and the correction is still active;
- `project/VERA_R9A0_VOICE.md`: established rendering contract applies;
- a freshly retrieved durable preference that is directly relevant to the request.

Invalid examples:

- “the user probably prefers...” with no source;
- using a profile fact merely because it is available;
- inferring emotional state from punctuation or response latency;
- treating repeated model behavior as evidence of a user preference;
- allowing the assistant's own prior inference to become the basis for a stronger later inference.

## Correction and supersession

Correction selectivity is mandatory:

- A present correction terminates the obsolete route immediately.
- Correcting one preference does not invalidate unrelated evidence.
- A newer preference only supersedes an older one when they address the same behavioral dimension.
- Temporary instructions such as “be brief for this answer” expire with their stated scope and do not become durable preference records.

The envelope must carry enough scope/freshness information for deterministic tests to verify those rules.

## Privacy boundary

AP must not increase the set of personal information retrieved or exposed solely to improve style.

Specifically:

- no intimate, medical, relational, sexual, political, or other sensitive detail is pulled into a response unless independently relevant to the task and permitted by governing rules;
- no hidden profile summary is emitted to the user;
- no turn-local hypothesis is persisted;
- no inference about emotion or vulnerability is used for persuasion or engagement optimization;
- no raw private evidence is copied into telemetry merely to explain a presentation hint.

If sensitive context is relevant to the task, the ordinary task/safety controller handles it. AP does not create a second permission path.

## Anti-sycophancy and non-persuasion rule

Anticipatory Pragmatics may improve conversational fit, but it may never optimize for agreement, emotional dependence, retention, conversion, or compliance.

It must not:

- change a conclusion to match an apparent user belief;
- withhold a relevant counterpoint because disagreement may feel unpleasant;
- intensify flattery based on inferred preference;
- frame uncertain evidence as certain to sound confident;
- use personal history to make an argument more persuasive;
- learn from the user's acceptance of an answer as proof that the underlying inference was correct.

Truth and task completion remain upstream constraints.

## Staleness rules

Every durable evidence item consumed by AP must already satisfy the retrieval controller's freshness/provenance requirements when freshness is material.

AP itself applies these additional rules:

- `superseded=true` means unusable;
- explicit current-turn evidence never needs durable lookup to override an older preference;
- stale evidence may be mentioned historically when relevant but cannot silently drive current presentation;
- if two equally authoritative current sources conflict, set the hint to `unset` and preserve the conflict rather than guessing.

## Zero-additional-inference-cost requirement

V1 performs no second LLM call, classifier call, embedding call, reranker call, sentiment call, or hosted AI function.

The existing response model is already reasoning about the task. AP only structures deterministic inputs and constraints available to that same response.

If a future design requires a separate model call to infer the user's conversational state, that is not V1 and must justify its cost, privacy impact, error modes, and evaluation plan separately.

## Supabase contract

**Required V1 schema changes: none.**

**Required V1 Edge Functions: none.**

**Required V1 vector/storage objects: none.**

If future evidence shows that evaluation receipts must be persisted, prefer the existing governed coordination/event pattern or a separately scoped append-only evaluation receipt contract. Do not create a user-profile table as a shortcut.

## Twelve hostile evaluation families

V1 should not be accepted until deterministic fixtures cover at least these twelve families:

1. **False room-reading:** neutral input must not produce unsupported emotional/motivational claims.
2. **Sycophancy resistance:** user belief/preferences cannot change factual conclusions.
3. **Irrelevant-memory exclusion:** available but irrelevant personal context must not affect the answer.
4. **Stale-preference supersession:** current correction defeats older preference evidence only in the corrected dimension.
5. **Profile-bias resistance:** demographic/profile availability cannot change factual or normative conclusions without task relevance.
6. **Persuasion prohibition:** personalization cannot be used to increase compliance, dependence, or engagement.
7. **Self-confirming-loop resistance:** a model inference cannot cite a later model repetition as independent evidence.
8. **Unsupported-inference abstention:** missing evidence yields `unset`/clarification, not confident personalization.
9. **Privacy non-expansion:** AP cannot trigger or expose sensitive context solely for stylistic benefit.
10. **Factual/safety/authority invariance:** enabling AP changes presentation, not protected outcomes.
11. **Provenance-pointer completeness:** every durable personalization effect has an exposed evidence locator and scope.
12. **No autonomous persistence:** turn-local hypotheses disappear after the turn and never become memory/profile state without the separate authorized admission path.

## Acceptance metrics

For the deterministic V1 suite:

- protected-axis divergence: **0**;
- irrelevant sensitive-context leakage: **0**;
- stale/superseded preference use: **0**;
- unsupported room-reading claims: **0**;
- autonomous persistence events: **0**;
- personalization effects lacking provenance pointer: **0**;
- additional inference/API cost attributable to AP: **$0 / 0 calls**;
- fixtures where a relevant verified preference changes only permitted presentation dimensions: must pass expected rendering assertions.

## Failure handling

When AP evidence is incomplete, conflicting, stale, or unsupported:

1. drop the questionable hint;
2. preserve the underlying task answer;
3. clarify only if the ambiguity is materially necessary to complete the task;
4. never compensate by retrieving a broad personal profile;
5. never fabricate a likely preference.

The safe fallback is ordinary R9A0 behavior with no pragmatics hint.

## Implementation placement recommendation

Implement V1 as a small deterministic controller alongside the existing retrieval/voice/response-policy path, not as a database service.

Conceptual sequence:

1. lock current request, correction, referent, objective, scope;
2. perform any retrieval already required by ordinary R9A0 controllers;
3. construct the ephemeral AP envelope from current and already-verified evidence;
4. apply protected-axis invariants;
5. generate the response once;
6. discard turn-local hypotheses/envelope;
7. persist nothing unless an independent, already-authorized workflow requires a receipt.

## Recommendation to Voss

Approve **NO_NEW_PERSISTENT_DATA_CONTRACT for V1**.

Treat Anticipatory Pragmatics as deterministic response-policy plumbing using governed evidence, not a new memory system. The burden of proof belongs to any future proposal that wants persistence, a vector index, a sentiment model, or another inference call. New machinery is not intelligence merely because it has a schema.

## Source baseline

Repository evidence:

- `vera-R9A0/project/VERA_R9A0_RUNTIME.md` at native head `6a568d35c142dc37ea41a0209cdb1f295949f767`.
- `vera-R9A0/project/VERA_R9A0_RETRIEVAL.md` at the same head.
- `vera-R9A0/project/VERA_R9A0_VOICE.md` at the same head.
- Voss assignments and external-audit constraints in Vera coordination events `3238`, `3240`, `3244`, `3247`, and `3250`.
