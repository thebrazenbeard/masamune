# Data Handling — V0

This document describes the implemented V0 data flow. It is not a substitute
for production privacy terms.

## Data read from GitHub

Depending on trigger and repository policy, Masamune may read:

- repository metadata;
- exact commit/tree identities;
- pull-request title/body and changed-file metadata/patches;
- issue title/body;
- selected source files;
- discussion comments for deterministic review-marker readback;
- collaborator permission for command authorization;
- optional `.masamune.yml`.

Collection is bounded by file count and UTF-8 byte ceilings.

## Data sent to model providers

The configured Masa and Mune providers receive the bounded review context:
source/diff excerpts plus subject metadata needed for analysis.

Mune's challenge request additionally receives the already-generated blind Mune
report and Masa report.

GitHub credentials, webhook secrets, and installation tokens are not included
in model prompts.

Before prompt submission, Masamune redacts several obvious secret forms,
including PEM private-key blocks, common GitHub token forms, AWS access-key IDs,
and long assignments whose names look like API keys/tokens/secrets/passwords.
No regex layer can guarantee discovery of arbitrary secrets.

## Private repositories

Private-repository analysis is globally disabled by default.

The service operator must explicitly set
`MASAMUNE_ALLOW_PRIVATE_REPOSITORIES=true` before private source can be routed
to configured model providers. A repository-controlled config file cannot
override that operator boundary.

A production multi-tenant service needs explicit customer/provider data terms
and per-customer retention controls before this should be offered commercially.

## Durable local state

V0 SQLite persistence stores:

- GitHub delivery ID;
- event name and payload digest;
- processing lifecycle state;
- timestamps and bounded error text;
- exact reviewed repository/subject/head identity;
- reconciled review report JSON.

The raw webhook payload and full source context are not persisted by the V0
ledger.

## GitHub writes

V0 writes only issue/PR discussion comments.

Before publishing, Masamune searches for its deterministic review marker. After
publishing, it reads back the discussion and requires that marker to be
observable before marking the delivery complete.

## Retention

V0 has no automated retention/deletion scheduler. The SQLite database persists
until the operator deletes or rotates it.

Production service work must add explicit retention windows, customer deletion,
backup handling, encryption-at-rest requirements, and tenant isolation before
claiming a complete privacy lifecycle.
