# Zero-Cost Deployment Profile

Status date: **2026-09-30**

Masamune's first hosted qualification target is deliberately constrained to a
monthly infrastructure/model budget of **$0**. The implementation fails closed
when its free allowance is unavailable; there is no paid fallback.

## Selected stack

### Runtime + durable state: Supabase Free

The hosted path uses a Supabase Edge Function plus Postgres tables for delivery
idempotency, exact review receipts, daily usage caps, and the singleton
model-execution lease.

Current Supabase Free-plan documentation lists:

- 500,000 Edge Function invocations in the included quota;
- 500 MB database size per free project;
- 256 MB Edge Function memory;
- 150 seconds maximum Edge Function wall-clock duration on Free.

References:

- https://supabase.com/docs/guides/platform/billing-on-supabase
- https://supabase.com/docs/guides/functions/limits
- https://supabase.com/docs/guides/functions/background-tasks

The edge function returns the GitHub webhook acknowledgement before doing the
review and uses `EdgeRuntime.waitUntil(...)` for bounded background work.

### Masa: Groq Free

Default:

```text
provider: groq
model: qwen/qwen3.8-27b
base URL: https://api.groq.com/openai/v1
```

At the status date, Groq's published Free Plan limits for this model are:

```text
30 RPM
1,000 RPD
8,000 TPM
200,000 TPD
```

Reference:

- https://console.groq.com/docs/rate-limits

Masamune uses a **singleton execution lease** so two reviews do not burst the
Groq token-per-minute allowance concurrently. Masa's automatic JSON-repair call
is disabled in the zero-cost edge profile so one malformed response cannot
silently double Groq token demand.

### Mune: Google Gemini Free

Default:

```text
provider: google
model: gemini-3.8-flash
base URL: https://generativelanguage.googleapis.com/v1beta/openai
```

Google currently lists Gemini 3.8 Flash input and output as free of charge
on the Gemini Developer API Free Tier. Google also documents Gemini 3.8 Flash as
the current stable Flash model and provides an OpenAI-compatible chat-completions
endpoint. The zero-cost profile sets Mune's temperature to the model default
(1.0) rather than forcing the 0 temperature used by older deterministic-style
models.

This replaces the earlier Gemini 2.5 Flash-Lite default because Google's current
model documentation notes that 2.5 models have restricted access for some new
projects and recommends newer models for new projects.

References:

- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/openai

Google also states that Free Tier content is used to improve Google products.
For that reason, **private repository analysis remains disabled by default**.
An operator must explicitly enable private-source routing after deciding the
provider/data terms are acceptable.

## Hard zero-cost ceilings

The hosted edge profile defaults to an **enforced zero-cost provider allowlist**.
When `MASAMUNE_ZERO_COST_ENFORCED=true`, startup rejects any provider/model
routing other than the documented free-tier Masa/Mune pair and also rejects
private-repository routing.

The hosted edge profile defaults to:

```text
max selected files/review:      10
max bytes/file or patch:       8,000
max aggregate context:        20,000 bytes
max model output:              2,000 tokens
model request timeout:         45 seconds
global reviews/day:            10
reviews/repository/day:         3
concurrent model reviews:       1
```

The daily review limit is claimed atomically in Postgres and is idempotent by
exact review ID. Review identity binds the exact bounded context digest, exact
Git subject, reviewer provider/model pair, and a review-protocol version.
Existing exact receipts are reused instead of spending free inference again.

The execution lane is also leased in Postgres with expiry, so a crashed worker
cannot permanently hold it.

If the daily allowance is exhausted, Masamune posts a bounded notice and runs
**no paid inference**. If the model execution lane is already occupied, the
delivery fails without initiating another model call.

## Why the limits are deliberately conservative

Masamune performs:

1. a Masa blind analysis;
2. a Mune blind analysis in parallel;
3. a Mune challenge pass against Masa.

The provider pair is intentionally different. That gives provider/model
diversity and preserves the blind-first-pass boundary; it is not proof that the
model outputs are statistically independent.

The 45-second provider timeout also keeps the normal two-stage inference path
comfortably below Supabase Free's current 150-second worker wall-clock limit,
leaving time for GitHub retrieval and publication.

## No-cost is an operational condition, not a permanent pricing claim

Provider free tiers, model availability, rate limits, and Supabase quotas may
change.

Masamune therefore treats the zero-cost profile as a **checked deployment
constraint**, not as a promise that third-party services will remain free.
Before deployment or provider changes, re-check the official provider pricing
and limits.

A future paid Masamune service can use the same evidence/reconciliation model,
but paid inference or infrastructure must never be activated implicitly by this
profile.


Current provider references:
- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/openai
- https://ai.google.dev/gemini-api/docs/pricing
