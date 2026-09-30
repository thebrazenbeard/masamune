> **License:** Source-visible, not open source. Original material is proprietary.
> Commercial use, redistribution, hosted-service use, and commercial derivative
> products require written permission. See [LICENSE](LICENSE) and
> [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

# Masamune

**Adversarial debugging and continuous defect discovery for GitHub repositories.**

Masamune is a GitHub App service built around two deliberately different review
lanes:

- **Masa** hunts for root causes, latent defects, unsafe assumptions, weak
  contracts, regression risks, and improvement opportunities.
- **Mune** performs a blind first pass, then attacks Masa's findings and rejects,
  narrows, confirms, or leaves them unresolved.

The product goal is not another AI that says "looks good." It is to reduce false
confidence by binding every run to an exact Git subject and forcing proposed
findings through a second adversarial lane before promotion.

## Current status

**V0 implementation / not yet a hosted production service.**

This repository now contains an executable FastAPI GitHub App backend with:

- GitHub App JWT + installation-token authentication;
- HMAC-SHA256 webhook verification;
- durable webhook delivery/idempotency ledger in SQLite;
- exact PR/issue/default-branch subject binding;
- bounded source-context acquisition;
- automatic PR review on open/reopen/synchronize/ready-for-review;
- `/masamune investigate [#issue]`;
- `/masamune sweep`;
- optional issue-label trigger via the `masamune` label;
- blind Masa/Mune first passes with provider/model diversity enforcement;
- Mune challenge pass;
- deterministic reconciliation into confirmed/narrowed/unresolved/rejected;
- marker-based comment idempotency plus post-write readback;
- repository-local `.masamune.yml` policy;
- unit tests and CI.

It does **not** yet execute untrusted repository code, create repair PRs, provide
a hosted queue, bill customers, or claim that a clean review proves a repository
is defect-free.

## How a review works

```text
GitHub event / command
        |
        v
exact repository subject
        |
        v
bounded source + diff context
        |
        +-----------------------+
        |                       |
        v                       v
      MASA                    MUNE
 defect / cause hunt       blind review
        |                       |
        +-----------+-----------+
                    |
                    v
             MUNE challenge
                    |
                    v
        deterministic reconciliation
                    |
                    v
      GitHub discussion + durable receipt
```

The blind passes run concurrently from the same declared source evidence. Mune
does not see Masa's first-pass output until the challenge phase. When
`MASAMUNE_REQUIRE_INDEPENDENCE=true`, Masa and Mune must use different provider
IDs and different model IDs. This is reviewer-diversity evidence, not proof of
statistical or factual independence.

## GitHub commands

On an issue or pull-request discussion:

```text
/masamune investigate
/masamune investigate #417
/masamune sweep
```

Pull requests can also be reviewed automatically when they are opened or
updated.

## Repository policy

Copy [`.masamune.example.yml`](.masamune.example.yml) to `.masamune.yml` in
a repository that has the app installed.

```yaml
masamune:
  enabled: true
  review_pull_requests: true
  allow_external_pull_requests: false
  allow_issue_commands: true
  allow_sweep: true
  post_unresolved: false
  max_files: 40
  max_file_bytes: 30000
  max_context_bytes: 180000
```

Unknown policy keys fail closed.

## Local development

Requires Python 3.12+.

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m ruff check src tests
```

Configure the environment from [`.env.example`](.env.example), then:

```bash
python -m masamune
```

The service exposes:

- `GET /health`
- `POST /webhook/github`

GitHub App setup is documented in
[docs/GITHUB_APP_SETUP.md](docs/GITHUB_APP_SETUP.md).

## Security boundary

Repository source, issue text, PR text, and diffs are treated as **untrusted
evidence**, not instructions to Masa or Mune.

V0 does not execute repository code. GitHub writes are limited to review
comments. Every comment includes an exact deterministic review marker; before a
write, Masamune checks for that marker, and after a write it checks again to
verify visibility.

A model finding is not promoted merely because two models agree. See
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Historical Masa / Mune state

The prior debugger-team operating records under `state/continuation/` remain
preserved as provenance. `PROTOCOL_V2_CURRENT.md` remains a repository-local
execution/governance source. The V0 service is a new executable layer built from
that debugging discipline rather than a claim that the historical agents
persist inside this process.

## Product direction

The intended progression is:

```text
detect -> investigate -> adversarially verify -> regression design
       -> sandboxed validation -> candidate repair -> draft PR
```

Continuous repository failure-memory, repair PRs, isolated test execution,
organization controls, and hosted billing are tracked in
[docs/ROADMAP.md](docs/ROADMAP.md).
