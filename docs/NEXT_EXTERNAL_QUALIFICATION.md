# Next External Qualification

Masamune's hosted runtime is deployed. The remaining operator work is credential and
GitHub-App provisioning; no source changes or secret commits are required.

## 1. Create the GitHub App

In GitHub, create a new GitHub App under the account or organization that will
own the installation.

Use this webhook URL:

```text
https://fawkirqroyniueeqspif.supabase.co/functions/v1/masamune-webhook
```

Permissions:

- Metadata: Read
- Contents: Read
- Issues: Read and write
- Pull requests: Read and write

Events:

- Pull request
- Issue comment
- Issues

Do not grant Actions, deployments, administration, secrets, packages, or
repository-content write access.

Generate:

- App ID
- private-key PEM
- webhook secret

Keep all three outside Git and outside chat.

## 2. Create the two free-tier model keys

Masa:

- Provider: Groq
- Model: `qwen/qwen3.8-27b`
- Base URL: `https://api.groq.com/openai/v1`

Mune:

- Provider: Google
- Model: `gemini-3.8-flash`
- Base URL: `https://generativelanguage.googleapis.com/v1beta/openai`

For Google, keep the project on the Gemini Free Tier. Do not attach paid billing
for this qualification run. For Groq, keep the account on the Free tier; do not
upgrade to Developer.

## 3. Add the five secrets to Supabase

Project:

```text
fawkirqroyniueeqspif
```

Function:

```text
masamune-webhook
```

Add these through Supabase's managed Edge Function secrets/environment UI:

```text
MASAMUNE_GITHUB_APP_ID
MASAMUNE_GITHUB_PRIVATE_KEY
MASAMUNE_GITHUB_WEBHOOK_SECRET
MASAMUNE_MASA_API_KEY
MASAMUNE_MUNE_API_KEY
```

Do not put the values in this repository.

The code already supplies the non-secret zero-cost configuration and rejects
non-allowlisted provider/model routing while zero-cost enforcement is enabled.

## 4. Install the GitHub App

Install Masamune on one disposable/test repository first.

Do not start with Masamune itself. The first probe should isolate GitHub
authentication, webhook delivery, provider access, model behavior, and GitHub
publication from defects in Masamune itself.

Keep private repositories disabled. The hosted default is:

```text
MASAMUNE_ALLOW_PRIVATE_REPOSITORIES=false
```

## 5. Run the qualification probe

Open a small test pull request in the disposable repository.

Expected path:

```text
GitHub webhook
  -> HMAC verification
  -> exact PR/head capture
  -> Masa blind review
  -> Mune blind review
  -> Mune challenge
  -> evidence audit
  -> deterministic Skeptic gate
  -> one marker-bearing GitHub comment
  -> publication readback
  -> durable receipt
```

Then redeliver/replay the same webhook and verify that no duplicate review
comment or second model execution occurs.

Also verify that the Supabase project remains on the Free plan and that both
provider accounts remain on their Free tiers.

## Current implementation constraints

V0 does not execute target-repository code and does not create repair PRs.
Its GitHub write authority is limited to review comments.

The current hosted caps are:

- 10 reviews/day globally
- 3 reviews/day/repository
- 1 concurrent model review
- 10 selected files/review
- 8,000 bytes/file or patch
- 20,000 bytes aggregate context
- 2,000 output tokens

Gemini 3.8 Flash is currently the configured Mune model. Google's current
documentation lists it as a stable model and documents a Free Tier; its current
migration guidance says to omit temperature/top-p/top-k parameters, so the edge
client does that for the Google lane.

## Qualification evidence to capture

Record:

1. GitHub delivery ID
2. exact PR head SHA
3. Masa provider/model
4. Mune provider/model
5. review ID
6. resulting GitHub comment URL
7. duplicate-delivery result
8. Supabase invocation/log result
9. provider usage/quota result
10. whether the project/account remained on Free tier

A successful first smoke test is not production qualification. Replay,
quota-exhaustion, failure-injection, prompt-injection, secret-redaction, and
independently authored holdout tests remain future qualification work.
