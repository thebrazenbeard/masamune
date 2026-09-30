# Security Policy

Masamune handles repository source, GitHub installation credentials, webhook
events, and model-provider credentials. Security issues should be treated as
potentially sensitive even when the repository itself is public.

## Reporting

Prefer GitHub private vulnerability reporting/security advisories for this
repository when available.

Do not publish working exploit details, private repository content, credentials,
webhook secrets, GitHub App private keys, or model-provider keys in a public
issue.

If private reporting is unavailable, contact the repository maintainer through
GitHub first and disclose only enough information publicly to establish that a
private channel is needed.

## V0 security boundaries

- target repository code is read but not executed;
- GitHub webhooks require HMAC-SHA256 verification;
- GitHub App installation tokens are minted on demand and not persisted;
- model workers never receive GitHub credentials;
- GitHub comments are marker-deduplicated and verified by readback;
- command-triggered model spend requires write/maintain/admin permission;
- external-contributor PR analysis is opt-in;
- private-repository model routing is disabled unless the operator explicitly
  enables it;
- obvious secret forms are redacted before model submission;
- repository source and discussion text are treated as untrusted prompt input.

Secret redaction is defense in depth, not a complete secret detector.

## Unsupported security claims

A passing Masamune review does not establish that a repository is secure.

V0 does not yet provide sandboxed target-code execution, a distributed durable
worker queue, customer-isolated multi-tenant secret custody, or formal
verification.
