# GitHub App Production Checklist

Masamune is intentionally not connected to a GitHub App registration in the
repository. The registration owns credentials and must remain outside source
control.

## Registration

Create a GitHub App named `Masamune` (or another available name) under the
operator's GitHub account or organization.

Set the webhook URL to:

```text
https://fawkirqroyniueeqspif.supabase.co/functions/v1/masamune-webhook
```

Set repository permissions to:

- Metadata: read
- Contents: read
- Issues: write
- Pull requests: write

Subscribe to:

- Pull request
- Issue comment
- Issues

Do not grant Actions, deployments, secrets, administration, packages, or
repository-content write access for V0.

## Credentials

After registration, obtain:

- GitHub App ID;
- generated private-key PEM;
- webhook secret.

Put them into the Supabase Edge Function secret store as:

```text
MASAMUNE_GITHUB_APP_ID
MASAMUNE_GITHUB_PRIVATE_KEY
MASAMUNE_GITHUB_WEBHOOK_SECRET
```

Do not paste credentials into GitHub issues, pull requests, repository files,
or this chat.

## Model credentials

Put the provider keys into the same secret store:

```text
MASAMUNE_MASA_API_KEY
MASAMUNE_MUNE_API_KEY
```

The zero-cost runtime will reject a provider/model configuration that does not
match its enforced free-tier allowlist.

## Installation

Install the GitHub App only on repositories whose owners have authorized
Masamune. Start with one disposable/test repository.

Open a test pull request and verify:

1. GitHub sends the webhook;
2. HMAC authentication succeeds;
3. the exact subject/head is captured;
4. the two blind lanes execute;
5. Mune challenges Masa;
6. evidence auditing runs;
7. the skeptic gate runs;
8. one marker-bearing comment appears;
9. the comment survives readback verification;
10. replaying the same webhook does not create a duplicate;
11. no private repository is analyzed while the zero-cost default is active;
12. the daily budget counter increments exactly once for the review ID.

## Hostile review

> Why start with a disposable repository instead of Masamune itself?

Because the first real-system probe should isolate credential, webhook, provider,
and publication failures from defects in Masamune's own repository.

> Why not grant repository write access so Masamune can fix what it finds?

Because V0's effect authority is deliberately limited to review comments. Repair
PR creation is a separate future authority boundary.

> Why is the GitHub App not automatically created by the repository?

GitHub App registration creates credentials and ownership outside repository
source. The repository can document and preconfigure the registration, but it
should not smuggle credentials into source control.

> What proves the service is production-ready after one successful test?

Nothing. A successful smoke test proves that one path worked. Production
qualification requires replay tests, failure injection, quota exhaustion tests,
prompt-injection cases, secret-redaction cases, and independently authored
benchmark holdouts.