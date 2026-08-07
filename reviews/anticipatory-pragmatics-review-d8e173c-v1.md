# Mune Independent Audit: R9A0 Anticipatory Pragmatics V1

Target repository: `thebrazenbeard/masamune`
Target lane: `masa`
Immutable target head: `d8e173c1c13c788c7eb9946bd4af25e44b488dfb`
Target artifact: `design/R9A0_ANTICIPATORY_PRAGMATICS_DATA_CONTRACT_V1.md`
Verdict: **CHANGES_REQUESTED**

## What survives review

I approve the core data decision: **V1 should create no new persistent Supabase store, profile table, vector index, memory class, Edge Function, or additional inference call.** The request-scoped, disposable-policy approach is materially safer than inventing a second memory/profile system.

The proposal also correctly preserves factuality, safety, authority, privacy, correction precedence, provenance, non-persuasion, and separate durable-memory admission as upstream constraints.

The remaining findings are contract-boundary defects that should be fixed before Voss freezes the implementation design.

## Findings

### MUNE-AP-001: `current-chat evidence outranks older durable evidence` is too broad

Construction rule 2 grants precedence to `current-chat evidence` when it addresses the same behavior. Current chat contains more than user-authored facts: it can include assistant guesses, earlier model wording, stale tool summaries, and unverified inference. Elsewhere the proposal correctly says model-generated repetition is not independent evidence, but the precedence rule itself does not encode that distinction.

**Required correction:** precedence belongs to the current user's explicit instruction/correction and to freshly verified authoritative project state, not to arbitrary current-chat material. Add evidence provenance/authority such as `origin = user_explicit | authoritative_tool | governed_durable | assistant_inference | historical`, and make `assistant_inference` ineligible to supersede user or governed evidence.

### MUNE-AP-002: free-text `turn_local_hypotheses` reopens the unsupported-inference path

The envelope permits a free-text presentation-only hypothesis with confidence and evidence basis. That field can become a convenient hiding place for exactly the behavior V1 is supposed to prevent: inferred mood, motive, vulnerability, or preference can be labeled `presentation_only` and still alter the answer's tone or framing.

**Required correction:** remove free-text hypotheses from V1, or constrain them to a closed enumerated set of evidence-derived presentation states that cannot encode mood, motive, ideology, vulnerability, or unstated intent. Confidence is not authority. A hypothesis must not become usable merely because it has a locator.

### MUNE-AP-003: the machine-readable protected-axis list is narrower than the prose invariants

The example `protected_axes` contains factuality, safety, authority, privacy, correction, provenance, and non-persuasion. The prose later additionally protects durable-memory admission, external-write authorization, fact-versus-inference status, and unknown/unresolved disclosure.

If implementation or tests rely on the explicit list, those omitted invariants can become accidental personalization surfaces.

**Required correction:** make the protected set fixed by schema rather than caller/model supplied and include at least `memory_admission`, `external_effect_authorization`, and `epistemic_status/abstention` in addition to the existing axes.

### MUNE-AP-004: deterministic-controller ownership is not yet proven in native ChatGPT architecture

The proposal requires rule-based construction, then consumption of an ephemeral envelope, with no second inference call. That is a valid logical contract, but a native ChatGPT implementation must show where this deterministic controller actually executes. If the same generative model informally constructs and interprets a free-form envelope inside one response, the design has constraints but not a separately enforceable deterministic controller.

**Required correction/dependency:** Hephaestus/Voss must bind the construction rules to an actual native runtime/instruction/validator surface and Enforcer must provide deterministic fixtures that prove equivalence. Until that placement exists, describe the envelope as a logical policy contract rather than claiming an independently executing deterministic component.

### MUNE-AP-005: task-risk fields must be authoritative inputs, not pragmatics-derived judgments

`risk_class` and `artifact_mode` appear in the AP envelope. They affect rendering choices, but risk classification and artifact handling are upstream governance concerns. AP must not be allowed to downgrade or reinterpret them.

**Required correction:** define these fields as read-only inputs supplied by upstream task/safety/artifact controllers. AP may consume them to further restrict presentation, never generate, lower, or override them.

## Twelve-family audit result

The proposal substantively covers all twelve requested hostile families: false room-reading, sycophancy, irrelevant memory, stale preferences, profile bias, persuasion optimization, self-confirming loops, unsupported inference, privacy leakage, protected-axis invariance, provenance completeness, and autonomous persistence. The acceptance targets of zero protected-axis divergence, zero sensitive-context leakage, zero stale-preference use, zero unsupported room-reading, zero autonomous persistence, zero missing provenance, and zero additional inference/API calls are appropriate.

The audit therefore does **not** challenge the no-new-store conclusion. It requests tighter provenance, hypothesis, protected-axis, and runtime-boundary semantics before implementation freeze.

## Required evidence for re-review/final freeze

1. Revised evidence-origin and precedence rules.
2. Removal or closed-enum restriction of `turn_local_hypotheses`.
3. Fixed complete protected-axis schema.
4. Native architecture placement showing how the logical contract is enforced without a second model call.
5. Deterministic tests proving AP cannot alter protected outcomes and cannot treat assistant inference as user evidence.

No persistent schema, migration, Edge Function, additional model call, or production mutation is requested by this review.