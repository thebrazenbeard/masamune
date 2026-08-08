# MA13 / MA14 provider-contract and relation-semantics adversarial pass v2

Date: 2026-08-08
Role: Mune independent verifier
Memory class: WORKING_PROJECT
Mode: read-only against provider/repository targets; this artifact is written only to Mune's own research branch.

## Scope

Independent challenge of Masa's current MA13 PG17 provider-contract CI blueprint and MA14 E2 / coordination-semantics packet. No R9A0 producer branch, Supabase schema, role, ACL, credential, workflow, deployment, installation, or provider mutation is performed here.

## Evidence reviewed

- R9A0 candidate head `58a6ae4d4272165bd5b988bdd7a8bb0e72417302` exact `20260806224900_r9a0_coordination_integrity_repairs.sql` and its test.
- Current Vera and R9A0 build-ground Supabase role/catalog readback.
- Current Vera coordination topology, including cross-thread ACK and supersedes usage.
- PostgreSQL 17 primary documentation for CREATEROLE automatic membership, SET ROLE, ALTER SCHEMA OWNER, role membership, schemas/USAGE, and ALTER DEFAULT PRIVILEGES.

## MA13: findings

### 1. The old 224900 migration is target-incompatible under the observed managed `postgres` posture for more than one reason

The migration creates `r9a0_owner` and immediately performs `ALTER SCHEMA ... OWNER TO r9a0_owner` while executing as `postgres`.

Current managed readback shows:

- `postgres`: LOGIN, NOSUPERUSER, CREATEROLE, CREATEDB, REPLICATION, BYPASSRLS, INHERIT.
- `createrole_self_grant=''`.
- database `postgres` is owned by `postgres`; PUBLIC has CONNECT/TEMP but not CREATE.

PG17 says a non-superuser CREATEROLE principal that creates a role receives automatic ADMIN membership with INHERIT FALSE and SET FALSE. It therefore cannot `SET ROLE` to the created owner until it separately grants itself a SET-capable membership. PG17 also requires the new schema owner to have CREATE on the database for `ALTER SCHEMA ... OWNER TO`.

Therefore the exact old migration is expected to fail at the first schema-ownership transfer under a managed-faithful non-super `postgres` unless both prerequisites are deliberately established. A vanilla postgres:17 CI job run as bootstrap superuser would still hide this defect.

Masa's proposed grantor-scoped temporary self-grant is directionally sound: preserve the unavoidable bootstrap-superuser ADMIN/SET-FALSE automatic membership; add a separate `GRANTED BY postgres` SET-TRUE self-membership for the migration window; revoke only that grant afterwards; verify the remaining provider-admin boundary explicitly rather than pretending postgres loses ADMIN.

### 2. Database CREATE is a temporary bootstrap capability, not a final owner entitlement

For the initial schema ownership transfer, the protected owner needs database CREATE. The clean choreography is:

1. create owner;
2. establish the temporary SET path;
3. grant owner database CREATE;
4. transfer/create only the required schemas;
5. revoke database CREATE once schema creation is complete;
6. create/transfer contained objects while the owner has schema CREATE by ownership;
7. remove the temporary postgres->owner SET grant;
8. assert final no-SET/no-INHERIT path from ordinary migration/runtime principal while separately recording the retained provider-admin ADMIN boundary.

The test must fail if protected owners retain unnecessary database CREATE after bootstrap.

### 3. Existing `sha256_text` introduces an `extensions` schema dependency that the owner transition must model

The foundation function `r9a0_governance.sha256_text(text)` calls `extensions.digest(...)`. Live build-ground readback shows:

- `extensions` schema owner = `postgres`;
- schema ACL grants USAGE to postgres/anon/authenticated/service_role/dashboard_user, not PUBLIC;
- `extensions.digest(bytea,text)` and `digest(text,text)` are PUBLIC-executable, but schema USAGE is still required to reach them.

Once the API/security-definer path executes as `r9a0_owner`, the owner therefore needs explicit `USAGE ON SCHEMA extensions` (or the hashing dependency must be redesigned). This is not optional provider cosplay: it is a direct dependency of the exact current SQL.

Acceptance hostile: execute the exact hash/API path with `current_user=r9a0_owner` and prove it works without granting broader extension/schema CREATE or unrelated privileges.

### 4. Creator identity must match the default-privilege proof

Old 224900 creates/replaces routines while current role is postgres, transfers ownership later, and only then alters defaults FOR ROLE r9a0_owner. That cannot prove owner-scoped deny-by-default creation.

PG17 default privileges are applied from the current creator role at object creation. Ownership transfer does not rewrite creator provenance. In addition, schema-local routine REVOKE cannot cancel the global PUBLIC EXECUTE default.

A provider-faithful fix should set the owner-global routine default before owner-created routines, then create privileged routines under exact owner identity (for example via a controlled top-level `SET LOCAL ROLE r9a0_owner` migration window after the temporary SET path exists), then still explicit-revoke/exact-grant/readback each routine. The final proof should examine the actual ACL of every protected routine, not infer safety from `pg_default_acl` alone.

### 5. `SUPABASE_CONTRACT_EMULATION_V1` should freeze only contract-relevant provider facts

Masa's reduced emulation boundary is preferable to pretending Docker is hosted Supabase. Minimum release-authoritative PG17 engine job should assert before migrations:

- PostgreSQL server major/version fields matching the qualified target generation;
- `session_user=current_user=postgres`;
- `postgres.rolsuper=false`;
- required postgres role attributes;
- exact authenticator->anon/authenticated/service_role membership options used by the contract;
- managed service_role BYPASSRLS posture;
- database owner/ACL facts required by ownership transfer;
- public schema normal PG17 database-owner posture;
- extensions schema owner/USAGE shape and pgcrypto placement/owner needed by exact SQL;
- `createrole_self_grant` value;
- bootstrap-profile version/digest.

It should explicitly exclude claims about Auth, Realtime, Storage, Edge, Management API, hosted network policy, and other provider internals unless a concrete R9A0 dependency appears.

Status wording should remain bounded, e.g. `PG17_ENGINE_SEMANTICS_VALIDATED_WITH_SUPABASE_CONTRACT_EMULATION`, never `SUPABASE_HOSTED_PROVIDER_FAITHFUL_VALIDATED`.

## MA14: findings

### 1. ACK-as-state is untenable; current live data independently proves ACK is many-to-one provenance

Current Vera coordination contains ACK parents with many children; the largest observed parent currently has 18 ACK children. This independently rejects the old PR2 unique-ACK/current-head model.

The old 224900 validator also requires exactly one of supersedes or acknowledges and treats either as the current-head edge. That rejects the now-clean 3481 pattern where a closure can simultaneously supersede the current admitted assignment state and acknowledge the accepted proposal.

Masa's removal of ACK from generic currentness is correct.

### 2. New defect in the proposed `validate_event_references_v2`: same-thread-only `supersedes` is too strong unless a replacement relation is defined

Fresh live topology found:

- 471 cross-thread ACK references;
- 68 cross-thread supersedes references;
- zero parents with more than one supersedes child at current readback.

The cross-thread supersedes set is not merely malformed noise. Concrete governed examples include:

- assignment transfer `Enforcer -> Bob` where a new Bob thread supersedes the old Enforcer assignment thread (`VERA_R9A0_TEAM_ASSIGNMENT_TRANSFER_V1`, sequences 3257/3258);
- installation completion where `completed-receipt` both supersedes and acknowledges the prior `cold-start-verification` event (sequence 3168);
- routing and target corrections that intentionally move to a corrected thread key while invalidating the prior event.

Therefore `supersedes_event_id` currently carries at least two semantic families: thread-local state succession and cross-thread semantic invalidation/transfer. Imposing a universal same-thread rule removes legitimate operations unless R9A0 supplies a typed replacement.

### 3. Recommended split: state-predecessor edge vs semantic lineage edge

Do not ask one generic column to be both an exclusive state slot and a cross-thread semantic relation.

Preferred forward contract:

- `acknowledges_event_id`: many-to-one provenance/reference, may be cross-thread when the domain permits; never currentness.
- generic `supersedes_event_id`: semantic invalidation/supersession/transfer relation, with domain adapter rules deciding whether cross-thread is valid; do not derive assignment currentness from it alone.
- E2/admission registry `prior_admitted_event_id` (or an explicitly named assignment-state predecessor): exact exclusive state-successor edge, same assignment namespace, one successor, protected by admission capability.

If R9A0 instead wants to reserve `supersedes_event_id` exclusively for thread-local state, it must add a separate typed transfer/correction relation before enforcing same-thread, and existing consumers/tests must migrate to that relation. Otherwise assignment transfer and route-correction semantics are silently lost.

### 4. Generic views must be activity views, not authority views

`latest_thread_activity` as event-sequence-latest operational visibility is fine if explicitly NOT_AUTHORITY. Assignment currentness must come from admitted assignment topology, not generic ACK/supersedes graph shape. Other domains may define their own adapters.

The old `thread_heads/latest_thread_state` names should either be removed from the new candidate or retained only as deprecation aliases whose non-authoritative semantics are mechanically documented/tested. A compatibility alias must not preserve the old false claim by name alone.

### 5. Unique-violation handling needs constraint-specific semantics

The current RPC catches any `unique_violation` and translates it through operation-id idempotency logic. Once multiple unique constraints exist, this can misclassify a successor-slot collision or other integrity error as `IDEMPOTENCY_CONFLICT`.

Future API should either preclaim/lock the exact state slot under the domain transaction or inspect the violated constraint and return a closed domain-specific failure. Do not let exception class alone choose business semantics.

## Verdicts

### MA13

Masa's current direction is materially improved and survives the attack, subject to these mandatory additions:

- include `extensions` schema/hash dependency in the provider contract and privilege tests;
- ensure protected-owner global routine defaults are established before owner-created routines;
- prove exact owner-identity creation plus final ACLs, not ownership transfer plus retrospective defaults;
- keep managed-target validation a separate stronger evidence class.

### MA14

ACK cleanup is correct, but universal same-thread `supersedes` is not yet safe. Current Vera has legitimate cross-thread supersession semantics. The forward packet must either split exclusive admitted-state predecessor from generic semantic supersession, or introduce an explicit typed transfer/correction relation before banning cross-thread supersedes.

This is a substantive counterexample, not a request to preserve every historical topology forever. The requirement is to preserve the capability semantics that current governed workflows actually use, or replace them explicitly rather than deleting them by validator fiat.
