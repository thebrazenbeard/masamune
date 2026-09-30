# Masamune Threat Model

Status: V0.1.

Masamune processes attacker-influenced GitHub material and sends selected
repository material to third-party model providers. The service therefore treats
the repository and the models as untrusted participants in the trust boundary.

## Assets

- GitHub App installation credentials;
- repository source and issue/PR contents;
- model-provider API credentials;
- review receipts and provider/model metadata;
- GitHub comment publication authority;
- free-tier inference budget;
- customer trust in the review output.

## Threats and controls

### Prompt injection in repository content

Threat: a README, source comment, issue, PR description, or patch attempts to
override the review instructions or induce an unauthorized action.

Controls:

- repository content is explicitly classified as untrusted evidence;
- model lanes have no GitHub credentials;
- model output does not directly select tools or effects;
- issue commands require repository write/maintain/admin permission;
- external pull-request auto-review is opt-in;
- invisible Unicode controls are surfaced to the model as visible markers;
- deterministic evidence and skeptic gates run after inference.

Residual risk: a model may still be semantically manipulated into producing a
bad review. The V0 effect surface is therefore limited to comments and the
service never executes target repository code.

### Secret disclosure

Threat: source context contains API keys, tokens, private keys, or other
credentials that should not reach a model provider.

Controls:

- common GitHub tokens, AWS access-key IDs, PEM private keys, and long
  secret/token/password assignments are redacted before model submission;
- provider credentials live in platform secrets, never repository files;
- private repository routing is disabled by default;
- review receipts store bounded model results rather than raw webhook payloads.

Residual risk: pattern redaction cannot identify every possible secret format.
Private-source use requires an explicit operator decision.

### Unauthorized model spend

Threat: public activity or repeated webhook delivery consumes the service's
free provider quota.

Controls:

- signed GitHub webhook verification;
- command authorization;
- deterministic delivery idempotency;
- exact-review receipt reuse;
- atomic global and per-repository daily budget caps;
- one active model execution lease;
- no paid fallback.

### Duplicate publication

Threat: retries or concurrent workers create repeated GitHub comments.

Controls:

- deterministic review marker;
- pre-write marker check;
- post-write readback;
- durable delivery state;
- exact review receipts;
- expiring execution lease.

### False confirmation

Threat: two models agree on an incorrect hypothesis and the service presents it
as fact.

Controls:

- Masa and Mune blind-first-pass separation;
- provider/model diversity requirement;
- Mune challenge pass;
- exact evidence-anchor requirement for confirmation;
- deterministic skeptic gate;
- explicit unresolved state;
- no clean-bill language.

Residual risk: model agreement is not independent factual evidence.

### Context omission

Threat: the actual defect depends on code outside the bounded context.

Controls:

- exact head SHA binding;
- byte/file/context ceilings;
- truncation markers;
- scope note in every report;
- bounded sweep is explicitly described as discovery rather than exhaustive
  analysis.

### Malicious model output

Threat: a model returns malformed JSON, fabricated evidence, mentions, or
markdown intended to manipulate the GitHub discussion.

Controls:

- schema validation;
- zero-cost edge profile disables automatic JSON-repair inference;
- output markdown sanitization;
- mention neutralization;
- deterministic evidence audit;
- no direct model-controlled API calls.

### Provider compromise or data-policy mismatch

Threat: a third-party inference provider receives repository content under terms
that the customer did not expect.

Controls:

- provider IDs and models are explicit in receipts;
- private repositories are disabled by default;
- the zero-cost deployment documents the provider data-policy caveat;
- future hosted plans must expose customer/provider data terms explicitly.

## Hostile review

> The service is safe because the model cannot call GitHub. What if the model
> can still manipulate the only effect it has: the public review comment?

Response: comment content is an effect and is therefore sanitized, marker-bound,
and readback-verified. Future repair actions must require a separate authority
boundary and human approval.

> Secret regexes do not find every secret. Why claim secret protection?

Response: do not claim it. Redaction is defense in depth, and the claim ceiling
is explicitly limited to the patterns implemented.

> What stops an attacker from burning the daily allowance with legitimate-looking
> pull requests?

Response: the current global/repository caps stop unbounded spend but can still
allow quota exhaustion. A future entitlement/rate-control layer is required for
multi-tenant operation.

> If the reviewer misses a bug, how will users know?

Response: every clean or bounded result carries an explicit scope limitation.
Masamune is an assistant for defect discovery, not a proof system.

## Security references

- https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
- https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app