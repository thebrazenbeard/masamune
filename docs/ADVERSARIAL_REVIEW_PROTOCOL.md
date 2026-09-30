# Masamune Adversarial Review Protocol

Status: V0.1 design contract.

Masamune is an adversarial reviewer, so the review process itself must be
reviewable. This document defines the hostile-review loop used to challenge
Masamune's own findings and architecture.

## Prime rule

A model output is a hypothesis, not evidence.

Repository files, issue text, pull-request text, diffs, model outputs, and model
agreement are separate evidence classes. A finding may be useful without being
confirmed, and a confirmed finding still does not prove the repository is
defect-free.

## Review loop

Every substantive Masamune change should pass this sequence:

1. State the proposed behavior or architectural change.
2. State the strongest reason it might be wrong.
3. Write the hostile objection explicitly.
4. Identify what observation would falsify the objection.
5. Modify the design only when the objection exposes a real weakness.
6. Record the remaining claim ceiling.

The repository should preserve meaningful disagreements rather than rewriting
them into false consensus.

## Required hostile questions

### Evidence

> What exact source material supports this finding, and can a reviewer locate it
> without trusting the model's prose?

If the answer is "the model noticed it," the finding remains a hypothesis.

### Independence

> Why should two models agreeing count as independent evidence when they read
> the same repository and may share training data, assumptions, and failure
> modes?

Masamune therefore calls the first Masa and Mune passes blind to each other.
Provider/model diversity is recorded, but never described as statistical
independence.

### Context

> What happens when the bug depends on a file Masamune did not retrieve?

The system must expose bounded scope and lower the claim ceiling. It must not
pretend a bounded sample is an exhaustive repository analysis.

### Prompt injection

> What if the repository author intentionally writes instructions aimed at
> manipulating the reviewer?

Repository content is data, not authority. Model outputs are also untrusted
before deterministic validation. This is a mitigation boundary, not a proof of
prompt-injection immunity.

### False positives

> What happens when a plausible-looking finding is actually intentional
> behavior?

Mune must attempt to reject or narrow Masa's claim. A future repository-specific
negative-memory system may record repeated intentional patterns, but that memory
must never silently suppress new evidence.

### False negatives

> What if Masamune finds nothing because the relevant code was outside the
> bounded context?

A clean result must explicitly state that absence of a finding is not evidence
of absence.

### Self-confirming repairs

> If the same model proposes a repair and then evaluates its own repair, why
> should its approval be trusted?

Repair generation and repair qualification must remain separate stages. Human
merge authority remains outside the model.

## Promotion rules

The V0 promotion ceiling is deliberately conservative:

- PROPOSED: model generated a finding.
- CHALLENGED: the finding entered adversarial challenge.
- CONFIRMED: challenge supplied concrete supporting evidence and deterministic
  evidence auditing found an exact source file anchor.
- NARROWED: the finding survives only after its claim is reduced.
- UNRESOLVED: evidence is insufficient to decide.
- REJECTED: the challenge found a concrete reason the proposed finding does not
  hold.

No stage means "the repository is secure."

## Independent review

An internal hostile review is not an independent review.

When a later Masamune release claims independent validation, it must identify:

- reviewer/model identity;
- provider/runtime;
- exact repository head;
- exact protocol version;
- exact bounded-context digest;
- material disagreement;
- whether the reviewer had access to the first review output.

## Zero-cost constraint

The adversarial process must not silently increase the provider budget.

For the zero-cost hosted profile, deterministic evidence auditing is preferred
over an additional model call when the same safety property can be established
without inference.

A future third model lane may be enabled only as an explicitly metered policy,
not as an implicit fallback.

## External security grounding

This design treats repository content as untrusted input and keeps model output
away from effect authority. These principles are consistent with current
OWASP guidance on prompt injection and excessive agency:

- https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
- https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html