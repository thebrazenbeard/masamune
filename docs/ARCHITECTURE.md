# Masamune V0 Architecture

## Purpose

Masamune V0 turns the historical Masa/Mune debugger discipline into an
executable GitHub App backend. The first product slice is intentionally narrow:
inspect exact GitHub subjects, acquire bounded source evidence, run two
differentiated model lanes, challenge proposed findings, reconcile the result,
and publish a readback-verified GitHub comment.

## Trust boundaries

### GitHub

GitHub is the source of repository identity, installation identity, pull
requests, issues, exact commit SHAs, source bytes, and the discussion surface.

Webhook bodies are accepted only after HMAC-SHA256 verification. Installation
tokens are minted from the GitHub App private key and are not persisted.

### Repository content

Repository content is hostile/untrusted input. Source files, comments, issue
bodies, PR descriptions, and patches can contain prompt-injection text. Model
system prompts explicitly classify all repository material as evidence rather
than instructions.

V0 does not execute target repository code. Obvious high-risk secret forms
(PEM private keys, common GitHub tokens, AWS access-key IDs, and long
secret/password/token assignments) are redacted before model submission. This is
defense in depth, not a guarantee that arbitrary secrets can be detected.

Private repositories are refused by default unless the service operator
explicitly enables private-source routing.

### Models

Masa and Mune are advisory computation lanes. Neither model has direct GitHub
credentials or effect authority.

Masa searches for causal defects and improvements. Mune first performs a blind
review, then receives Masa's committed report and attempts to disprove it.

With independence enforcement enabled, the lanes must have different provider
IDs and different model IDs. They still share the declared repository evidence,
so this is provider/model diversity and blind-first-pass separation, not proof
of statistical independence.

### Effects

The only V0 repository effect is an issue/PR discussion comment.

The effect path is:

1. derive deterministic review ID from the protocol version, repository,
   subject type/number, base/head SHAs, Masa/Mune provider+model IDs, and a
   SHA-256 digest of the exact bounded context;
2. search existing comments for that marker;
3. if an exact review receipt already exists, reuse it without another model
   call; otherwise run the review;
4. durably store the result and enter `READY_TO_PUBLISH`;
5. re-check marker immediately before POST;
6. write the comment;
7. re-read comments and require the marker to be observable;
8. mark the delivery `COMPLETED`.

A retry from `FAILED` or `READY_TO_PUBLISH` is allowed. Marker readback
prevents blind duplicate publication.

## Event flow

```text
GitHub webhook
  -> signature verification
  -> durable delivery claim
  -> installation authentication
  -> repository policy
  -> exact subject/context builder
  -> [Masa blind scan || Mune blind scan]
  -> Mune challenge
  -> deterministic evidence audit
  -> deterministic skeptic gate
  -> reconciliation
  -> durable review receipt
  -> GitHub comment
  -> readback verification
```

## Subject modes

### Pull request

Events: `opened`, `reopened`, `synchronize`, `ready_for_review`.

The context includes exact base/head SHAs, PR title/body, bounded changed-file
patches, and bounded head source when GitHub exposes it through the installation.

Draft PRs are ignored until ready-for-review unless the ready event itself is
being handled.

### Command authorization

Issue-comment commands and label-triggered investigations require the triggering
GitHub user to have `write`, `maintain`, or `admin` repository permission.
This prevents arbitrary public commenters from spending model budget.

Automatic pull-request review defaults to trusted author associations only
(`OWNER`, `MEMBER`, `COLLABORATOR`). Repository owners may explicitly set
`allow_external_pull_requests: true`.

### Issue investigation

Trigger:

```text
/masamune investigate
/masamune investigate #123
```

Masamune binds the issue text to the current default-branch commit, walks the
tree, ranks likely relevant code paths using issue terms and risk-surface
tokens, and includes only the bounded selected source.

### Sweep

Trigger:

```text
/masamune sweep
```

The sweep binds current default-branch state, ranks code paths toward high-risk
surfaces such as auth, state, retries, queues, transactions, migrations,
tokens, and concurrency, and inspects a bounded diverse subset.

This is discovery, not exhaustive static analysis.

## Evidence audit

Every model finding receives a deterministic evidence receipt bound to the
exact bounded-context digest. The auditor distinguishes `EXACT_FILE_LINE`,
`EXACT_FILE`, `CONTEXT_ONLY`, and `MODEL_ASSERTION`.

A diff hunk is deliberately not treated as a source-line anchor. This matters
because GitHub's review APIs use diff coordinates for inline comments, while a
finding's `line` field refers to the head blob source. Those coordinate systems
must not be conflated.

## Skeptic gate

The skeptic is currently deterministic rather than another model call. It checks
challenge coverage, finding-ID integrity, evidence-receipt presence, weak anchors
on high-severity findings, and reviewer provider/model collisions.

This intentionally improves the zero-cost path without consuming another free
model request. A future third model lane is an explicit policy change, not a
hidden behavior.

## Reconciliation

Masa findings are promoted only after Mune supplies a challenge record.

- `REJECT` -> hidden from promoted findings, ID preserved in rejected list.
- `CONFIRM` -> promoted only when Masa confidence is at least 0.65 and Mune
  supplies concrete evidence.
- `NARROW` -> promoted under the narrower claim with Mune evidence attached.
- `UNRESOLVED` or missing challenge -> unresolved.
- blind-only Mune findings -> unresolved; they have not survived an additional
  independent challenge.

Two models agreeing is not itself evidence. Evidence quality and challenge
coverage are separate deterministic gates.

## Durable state

The Python/local backend uses SQLite for webhook delivery identity, lifecycle
state, exact review subject, and reconciled report JSON.

The zero-cost hosted path uses Supabase Postgres for the same evidence plus:

- UTC global daily review counters;
- per-repository daily review counters;
- idempotent budget claims keyed by exact review ID;
- a singleton model-execution lease with expiry.

The execution lease is a free-tier concurrency control, not a general
distributed work queue. It prevents concurrent reviews from bursting model
token-per-minute allowances. A crashed holder eventually loses the lease by
expiry.

The raw webhook payload and full source context are not durably stored by either
V0 ledger.

## Current limitations

- no durable distributed work queue or general multi-worker fencing beyond the
  singleton zero-cost model-execution lease;
- a busy zero-cost execution lane fails the delivery rather than queueing it;
- no sandboxed repository test execution;
- no semantic code graph or symbol-aware retrieval yet;
- no historical per-repository failure graph;
- no automated repair branch/PR creation;
- no GitHub Checks annotations;
- no organization dashboard;
- no billing or Marketplace integration;
- OpenAI-compatible chat-completions adapters only;
- source context is byte/file bounded and can miss distant dependencies;
- hosted V0 depends on third-party free-tier availability and fails rather than
  switching to paid service.

The exact zero-cost deployment ceilings and provider choices are documented in
[ZERO_COST_DEPLOYMENT.md](ZERO_COST_DEPLOYMENT.md).

Those limits are claim ceilings, not hidden roadmap accomplishments.
