# GitHub App Setup

Masamune V0 is intended to run as a GitHub App installed on explicitly selected
repositories.

## Create the app

Create a GitHub App owned by the account or organization that will operate the
service.

Set the webhook URL to:

```text
https://YOUR-SERVICE/webhook/github
```

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

Set:

```text
MASAMUNE_STATE_DB_PATH=/durable/path/masamune.sqlite3
```

The V0 SQLite ledger must live on persistent storage. Running it only on
ephemeral container storage weakens restart/recovery guarantees.

## Repository installation

Install the GitHub App only on repositories whose owner has authorized review.

Optionally commit `.masamune.yml` to tune review behavior. The app does not
need that file; absence uses conservative defaults.

## Verify

After deployment:

1. request `GET /health` and require `{"status":"ok"}`;
2. deliver a signed GitHub webhook;
3. open a test PR;
4. verify Masamune posts one marker-bearing review comment;
5. redeliver the exact webhook and verify no duplicate comment appears.

Do not call the service production-ready until those external effects have been
observed against the actual installed GitHub App.
