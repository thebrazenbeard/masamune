# Mune MU7 Addendum — Live PostgreSQL 17 Parity Gate

**Parent assignment:** `VOSS-20260808-MU7` / root `3465`  
**Parent review:** `reviews/edge-transport-capability-audit-mu7-v1.md`  
**Class:** read-only provider/repository precision addendum  
**Mutation performed:** none  
**Disposition:** `LIVE_PG17_ACCEPTANCE_REQUIRED`

## 1. Exact target-version precision

Fresh SQL readback from both relevant Supabase projects reports:

```text
server_version     = 17.6
server_version_num = 170006
```

R9A0 build ground `agvhmutlrolbaijzlbqk` additionally reports:

```text
PostgreSQL 17.6 on aarch64-unknown-linux-gnu
```

Live Vera `klmbpaigzeguvnpccqzz` reports:

```text
PostgreSQL 17.6 on x86_64-pc-linux-gnu
```

Therefore the database engine semantics relevant to MU7/V3 are **PostgreSQL 17.6 / server_version_num 170006**.

Canonical coordination 3493 currently phrases the live provider as `17.6.1`. I do not have SQL evidence for a PostgreSQL `17.6.1` server version string. If `17.6.1` came from a Supabase platform/release label rather than PostgreSQL's server version, retain it only as that separately named platform datum. For database-semantic qualification, bind `server_version_num=170006` / `server_version=17.6`.

This is a precision correction, not a material reversal of 3493's parity finding.

## 2. Independent exact-source CI verification

Fresh GitHub reads confirm **both** relevant R9A0 workflow versions use disposable PostgreSQL 15:

### Current native base

- repository: `thebrazenbeard/vera-R9A0`
- exact ref: `6a568d35c142dc37ea41a0209cdb1f295949f767`
- path: `.github/workflows/r9a0-database-validation.yml`
- blob: `85c4e3fbe017199253c506510336f2846eb183df`
- service image: `postgres:15`
- stronger workflow: exact merge-parent verification, 4 migrations, 4 SQL suites, deterministic two-session harness, 22-file manifest.

### Current main used in topology reconciliation

- exact ref: `b00f3482786dc80003261fdfacb73cc31ae9dd35`
- same path
- blob: `3fb492e74feb9897503e8a5c29e86ae0a2ca627f`
- service image: `postgres:15`
- older/weaker workflow.

Thus the current native workflow is materially stronger than main while sharing the same target-major mismatch.

## 3. What existing PR2 evidence proves

Existing merge-candidate CI remains valid evidence for:

- the exact candidate/base it bound at run time;
- the declared disposable PostgreSQL 15 service;
- the migrations/tests/concurrency/manifest checks that actually executed there.

It is **not** proof that:

- PostgreSQL 17 role membership option behavior has been exercised;
- V3's future creator-owner `SET`/`INHERIT`/`ADMIN` negative matrix has passed on the target provider major;
- PG17 default-privilege/routine behavior has been exercised by the future privilege packet;
- PG17 SECURITY DEFINER/role/current-user hostiles have passed under provider-faithful topology;
- Supabase platform-specific `authenticator` memberships/provider roles/default schemas behave identically to a vanilla postgres:15 container.

Green PG15 CI is therefore compatibility evidence, not hosted-provider parity evidence.

## 4. PG17 membership semantics that MU7 must bind

PostgreSQL 17 primary documentation already exposes membership options independently:

- `INHERIT`
- `SET`
- `ADMIN`

`SET ROLE` requires a `SET TRUE` membership chain. `WITH INHERIT FALSE, SET FALSE` prevents ordinary use of the granted role's privileges through either inheritance or SET ROLE.

A sharper PG17 hostile is the combination of `CREATEROLE` plus `ADMIN OPTION`: PostgreSQL documents that an ADMIN holder with CREATEROLE can grant the role onward, including back to itself with different membership options. Therefore final runtime posture must prove:

- `r9a0_edge_ingest` has `NOCREATEROLE`;
- no direct or transitive ADMIN option on `r9a0_edge_api_owner` or any broader role;
- no `SET` path into owner/admin roles;
- no inherited USAGE path that broadens execution;
- exact migration-time creator membership is removed or remains explicitly bounded after creation.

Role-level `NOINHERIT` is not the proof.

Primary sources:

- PostgreSQL 17 Role Membership: https://www.postgresql.org/docs/17/role-membership.html
- PostgreSQL 17 SET ROLE: https://www.postgresql.org/docs/17/sql-set-role.html
- PostgreSQL 17 Role Attributes: https://www.postgresql.org/docs/17/role-attributes.html

## 5. PG17 V3 privilege/security semantics must be tested on target-major

The exact V3 design relies on:

- global actual-creator default privilege closure for routines;
- dedicated creator/owner identity;
- same-transaction current-routine PUBLIC EXECUTE revocation/exact grant;
- SECURITY DEFINER trusted search path and fully qualified sensitive objects;
- effective membership/ownership/PUBLIC/provider privilege checks.

Those design choices are supported by PostgreSQL primary documentation, but deployment acceptance must execute them on a PG17/provider-faithful surface. Documentation review is not executable provider proof.

## 6. Recommended CI/parity contract

Do not simply replace `postgres:15` and erase older compatibility evidence.

Recommended future split:

### `TARGET_PROVIDER_MAJOR`

Required gating job using PostgreSQL 17, ideally matching the hosted provider's target major and required extensions/role bootstrap as closely as practical.

This job is mandatory for hosted-apply readiness and every privilege/security invariant that depends on target-major behavior.

### `SUPPORTED_COMPATIBILITY_MAJOR`

Optional separate PostgreSQL 15 job only if R9A0 intentionally supports PG15 as a product compatibility target.

It must not be the sole required provider-readiness job.

### Hosted/provider readback

Even PG17 Docker is not equivalent to Supabase. Before hosted activation, separately read back:

- actual server version/number;
- platform roles/memberships/options;
- extensions/provider schemas/default privileges relevant to the packet;
- exact wrapper owner/security/search_path/ACL;
- effective runtime role capabilities;
- provider transport/runtime capability inventory.

This preserves the distinction:

`TARGET_MAJOR_CI != HOSTED_PROVIDER_ATTESTATION`.

## 7. Interaction with MU7 transport ranking

The parity gap does not change MU7's transport ranking.

- isolated guarded publisher + dedicated narrow Postgres LOGIN remains the preferred current hard-boundary direction;
- custom Data API role remains conditional;
- current managed Edge remains capability-broader than V3 under current documented defaults.

It does change the acceptance wording:

**every candidate transport must pass `LIVE_PG17_ACCEPTANCE` against the exact implementation head before deployment.**

The eventual test matrix should treat future-major compatibility separately rather than importing PG18 language into a PG17 target by habit.

## Verdict

`LIVE_PG17_ACCEPTANCE_REQUIRED`

The current R9A0 DB workflow is strong evidence for its declared PostgreSQL 15 disposable target, but it does not qualify PostgreSQL 17/provider semantics. Exact provider SQL readback currently reports PostgreSQL 17.6 (`170006`) on both Vera and R9A0 build-ground projects.

No workflow, repository producer branch, database object, role, grant, credential, provider setting or deployment was modified.