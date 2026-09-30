# GitHub App Setup

Masamune V0 is intended to run as a GitHub App installed on explicitly selected
repositories.

## Create the app

Create a GitHub App owned by the account or organization that will operate the
service.

For the Python/FastAPI backend, set the webhook URL to:

```text
https://YOUR-SERVICE/webhook/github
```

For the zero-cost Supabase Edge deployment, use:

```text
https://YOUR-PROJECT-REF.supabase.co/functions/v1/masamune-webhook
```

The Supabase function must be deployed with platform JWT verification disabled
because GitHub does not send a Supabase JWT. This does **not** make the webhook
unauthenticated: Masamune verifies GitHub's `X-Hub-Signature-256` HMAC against
the raw body before accepting the delivery.

Generate a strong webhook secret and store it as
`MASAMUNE_GITHUB_WEBHOOK_SECRET`.

Generate a GitHub App private key and provide its PEM text through
`MASAMUNE_GITHUB_PRIVATE_KEY`. Environment secret storage is required; do not
commit the key.

Set the numeric app ID in `MASAMUNE_GITHUB_APP_ID`.

## Repository permissions

V0 needs the smallest practical set for the implemented behavior:

- **Metadata:** read (GitHub provides this automatically for installed apps)
- **Contents:** read
- **Issues:** write
- **Pull requests:** write

Masamune currently does not require Actions, deployments, administration,
secrets, environments, packages, or repository-content write access.

Future sandbox/test or repair-PR features must request additional permissions
only when their implementation actually needs them.

## Subscribe to events

Enable:

- **Pull request**
- **Issue comment**
- **Issues**

The service ignores events/actions outside the implemented trigger set.

## Private repositories

V0 defaults to refusing private repositories because source context is sent to
the configured model providers. To enable private-repository analysis, the
service operator must explicitly set:

```text
MASAMUNE_ALLOW_PRIVATE_REPOSITORIES=true
```

That switch is an operator-level data-routing decision. A repository policy file
cannot silently enable private-source export.

## Model configuration

Configure two OpenAI-compatible chat-completions endpoints.

The zero-cost profile defaults to:

```text
Masa: Groq / qwen/qwen3.8-27b
Mune: Google / gemini-2.5-flash-lite
```

See [ZERO_COST_DEPLOYMENT.md](ZERO_COST_DEPLOYMENT.md) for the current free-tier
limits, privacy caveat, and hard Masamune caps.

Masa:

```text
MASAMUNE_MASA_BASE_URL=
MASAMUNE_MASA_API_KEY=
MASAMUNE_MASA_PROVIDER_ID=
MASAMUNE_MASA_MODEL=
```

Mune:

```text
MASAMUNE_MUNE_BASE_URL=
MASAMUNE_MUNE_API_KEY=
MASAMUNE_MUNE_PROVIDER_ID=
MASAMUNE_MUNE_MODEL=
```

When `MASAMUNE_REQUIRE_INDEPENDENCE=true`, provider IDs and model IDs must both
differ. If only one provider is available for development, explicitly disable
that enforcement rather than pretending the lanes are provider-independent.

## Persistent state

For the Python/local backend, set:

```text
MASAMUNE_STATE_DB_PATH=/durable/path/masamune.sqlite3
```

For the Supabase Edge backend, apply
`supabase/migrations/20260930_masamune_v0.sql`. The Edge Function uses the
project's Postgres database for delivery receipts, exact review receipts,
zero-cost daily budget admission, and the singleton expiring execution lease.

The Edge Function reads Supabase's server key from its managed environment and
does not require that key to be copied into the repository.

## Repository installation

Install the GitHub App only on repositories whose owner has authorized review.

Optionally commit `.masamune.yml` to tune review behavior. The app does not
need that file; absence uses conservative defaults.

## Verify

After deployment:

1. request the active runtime's health endpoint and require
   `{"status":"ok"}` (the Edge route reports
   `"billing_mode":"zero-cost-capped"`);
2. deliver a signed GitHub webhook;
3. open a test PR;
4. verify Masamune posts one marker-bearing review comment;
5. redeliver the exact webhook and verify no duplicate comment appears.

Do not call the service production-ready until those external effects have been
observed against the actual installed GitHub App.
