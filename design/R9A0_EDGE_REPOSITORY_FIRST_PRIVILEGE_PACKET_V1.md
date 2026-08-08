# R9A0 Edge Repository-First Least-Privilege Packet V1

**Status:** `NON_EXECUTING_PRIVILEGE_PACKET_READY_FOR_REVIEW`  
**Assignment:** Vera coordination sequence `3313`  
**Predecessor design:** Masa Edge implementation-readiness exact head `3e5290a096a7069c9b194470ae6d0efa2830b41d`  
**Independent predecessor approval:** Mune sequence `3331`  
**Product target:** `thebrazenbeard/vera-R9A0` database surface, future authorized implementation only  
**Hosted apply authorized by this document:** `NO`  
**Credential creation authorized by this document:** `NO`  
**Deployment authorized by this document:** `NO`  
**Paid-service action authorized by this document:** `NO`

## 1. Decision

The deferred `r9a0-coordination-ingest` Edge adapter may reach R9A0 Postgres only through one dedicated least-privilege database execution role and a deliberately tiny API surface. The Edge adapter is transport, not a second coordination authority, workflow engine, memory store, or generic database gateway.

The future database execution role is named:

`r9a0_edge_ingest`

It must be a non-owner, non-superuser role with no database-creation, role-creation, replication, bypass-RLS, schema-creation, table, view, sequence, or broad function privileges. It must not inherit `r9a0_owner`, `postgres`, `service_role`, or any other broad administrative role.

`service_role` is forbidden as the Edge deployment credential or fallback. If the hosted platform cannot expose the required narrow principal without giving the Edge runtime a broad project secret, implementation stops. There is no “temporary” broad-secret exception.

## 2. Repository-first implementation packet

A later authorized implementation must land as repository code and tests before any hosted apply. The candidate must be bound to an exact product-repository parent head and reviewed before migration execution.

The future packet contains exactly these responsibilities:

1. one monotonic Supabase migration defining or hardening `r9a0_edge_ingest` and the narrow API grants;
2. one SQL privilege/negative-test suite proving the role cannot bypass the intended API surface;
3. if the canonical coordination writer is not already callable with the needed narrow contract, one `SECURITY DEFINER` wrapper in `r9a0_api` that delegates to the canonical coordination write semantics rather than duplicating them;
4. one read-only receipt lookup RPC only if the canonical write path cannot deterministically resolve ambiguous commit outcomes by `operation_id`;
5. no Edge Function source, credential, deployment configuration, paid-service configuration, or hosted mutation in the same packet.

The packet must not invent a second coordination event table or parallel ledger.

## 3. Required role attributes

The future migration must assert the equivalent of the following role posture:

```sql
-- Specification only. Do not apply from this document.
ALTER ROLE r9a0_edge_ingest
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOINHERIT
  NOREPLICATION
  NOBYPASSRLS;
```

Whether the role is `LOGIN` or `NOLOGIN` is an authentication-transport choice that must be resolved before hosted deployment without putting a password, JWT signing key, service-role key, or connection secret in Git. The privilege contract is unchanged either way. No credential is created by this packet.

The role must not own any R9A0 schema, table, sequence, view, function, trigger, policy, extension, or storage object.

## 4. Required grant/revoke shape

The final migration must make privilege closure explicit rather than depending on inherited/default ACL behavior.

### 4.1 Database and schema posture

`r9a0_edge_ingest` may have only the minimum database connection privilege required by the chosen transport. It must not receive database `CREATE` or `TEMPORARY` merely for convenience.

It receives:

- `USAGE` on `r9a0_api` only.

It receives no `USAGE` or `CREATE` grant on:

- `r9a0_governance`
- `r9a0_coordination`
- `public` beyond unavoidable provider defaults that are independently proven non-mutating for this role.

Any provider-default `CREATE ON SCHEMA public` exposure applicable to the role must be revoked or proven unreachable through its membership graph.

### 4.2 Relation and sequence posture

The role receives **zero** direct privileges on canonical relations and sequences. The migration/test packet must prove there is no effective `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES`, `TRIGGER`, or sequence `USAGE/SELECT/UPDATE` privilege through direct grants, `PUBLIC`, or inherited role membership.

This includes all existing and future coordination/governance relations. A future schema addition must not silently expand Edge rights.

### 4.3 Function posture

PostgreSQL functions default to `EXECUTE` for `PUBLIC`; therefore every Edge-specific API function created by the packet must revoke `PUBLIC` execution in the same migration before granting the dedicated role.

The only Edge-callable symbols permitted by this contract are:

- one canonical write entry point exposed in `r9a0_api` for a complete validated coordination-ingest request;
- optionally, one read-only receipt lookup entry point keyed by the same durable `operation_id` when needed to resolve an ambiguous write outcome.

The exact symbol/signature must be bound to the product repository’s current database contract during implementation review. The implementation may not grant `EXECUTE ON ALL FUNCTIONS`, wildcard future-function rights, or schema-wide default execute rights to `r9a0_edge_ingest`.

If a wrapper is required, it must be owned by the narrow canonical database owner (`r9a0_owner` or the then-reviewed equivalent), be `SECURITY DEFINER`, and set an explicit safe `search_path` that excludes attacker-controlled schemas. It must not construct dynamic SQL from request values.

## 5. Canonical-write preservation

The Edge API must not bypass existing coordination invariants. The one write entry point must preserve the canonical R9A0 semantics for:

- durable `operation_id` identity;
- replay with identical semantics returning the existing effect/receipt rather than duplicating it;
- same `operation_id` with changed canonical semantics failing closed;
- authoritative event ordering/sequence assignment by the database;
- request/event validation;
- source/target/thread/event-type constraints already owned by the canonical coordination layer;
- no caller-supplied generated identity/sequence override;
- no direct Edge table write.

The Edge caller may not submit a generated database sequence value or use a raw table insert as a fallback.

## 6. Ambiguous-commit contract

An ambiguous network/transport result is not permission to repeat a write blindly.

Required behavior:

1. caller sends one canonical request with one durable `operation_id`;
2. if the result is clearly committed, return the canonical receipt;
3. if the result is clearly rejected, return the stable failure class;
4. if commit state is ambiguous, perform a **read-only** receipt lookup by `operation_id`;
5. if a matching receipt exists with the same canonical request digest, return it;
6. if the identity exists with a different digest/semantics, fail `OPERATION_ID_CONFLICT` with zero new effect;
7. if no receipt exists, only then may the same exact operation be retried.

The receipt lookup cannot mutate state.

## 7. Negative-test contract

A future repository test suite is incomplete unless it proves the following as the `r9a0_edge_ingest` role or an equivalent effective-privilege simulation.

### 7.1 Role and membership

Must fail/deny:

- membership in `postgres`, `service_role`, `r9a0_owner`, or any broad writer/admin role;
- `SET ROLE` into a broader role;
- `CREATE DATABASE`, `CREATE ROLE`, extension ownership, schema creation, and role/grant administration;
- ownership of any R9A0 object.

### 7.2 Direct data access

Must fail/deny on every canonical governance/coordination relation:

- direct `SELECT` when not explicitly required by the one receipt RPC;
- direct `INSERT`;
- direct `UPDATE`;
- direct `DELETE`;
- `TRUNCATE`;
- sequence `nextval`, `setval`, or direct sequence update;
- direct writes through views or convenience functions outside the exact allowlist.

Receipt retrieval must be possible only through the exact read-only API symbol, never a broad table grant.

### 7.3 API surface

Must fail/deny:

- execute on any `r9a0_api` function outside the exact allowlist;
- wildcard/function-default expansion after an unrelated API function is added;
- dynamic-search-path hijack using a caller-controlled `public` or temporary object;
- malformed payloads, unsupported event types, disallowed source/target/thread scope, and missing durable operation identity;
- same `operation_id` with a changed canonical payload digest;
- caller-supplied database sequence or generated identity fields;
- attempts to use the receipt lookup as a write path.

Must pass:

- one valid scoped ingest through the canonical API;
- identical replay returning the same durable effect/receipt;
- ambiguous-outcome lookup returning the committed receipt without creating another event.

### 7.4 Service-role exclusion

The repository test/validation packet must contain an explicit assertion that Edge deployment configuration does not reference a `service_role` secret or equivalent broad administrative database secret. This is a repository/configuration gate; secret values must never be printed or committed.

## 8. Forward repair

If review finds the initial privilege surface too broad, repair is additive and monotonic:

1. add a new migration that revokes the excess grant or introduces a narrower versioned API symbol;
2. update the SQL negative tests first so the previous broad behavior fails;
3. preserve canonical coordination rows and receipt identity;
4. do not edit an already-applied migration in place;
5. retire the superseded API grant only after the replacement path passes exact-head tests and review.

A function signature change requires an explicit new reviewed symbol/signature or a migration that atomically replaces it without widening ACLs.

## 9. Rollback

Rollback means removing Edge reachability, not deleting coordination data.

Safe rollback order for a future hosted deployment:

1. disable/revoke the Edge caller credential at the deployment boundary;
2. revoke `EXECUTE` from `r9a0_edge_ingest` on the Edge write and receipt functions;
3. terminate remaining sessions for the dedicated role if required;
4. revoke `USAGE` on `r9a0_api`;
5. drop the dedicated role only after dependency/readback proves it owns nothing and no active dependency requires it;
6. drop Edge-only wrapper functions only if no other reviewed consumer uses them;
7. preserve canonical coordination/governance rows and existing database migrations.

No rollback path may delete canonical events merely to make the Edge deployment disappear.

## 10. Repository verification gate

Before any hosted apply, the exact implementation candidate must prove:

- migration and SQL tests exist on one immutable product-repository head;
- exact parent/base is recorded;
- no unrelated database/native-project drift is present;
- all existing database validation suites still pass;
- new privilege-negative tests pass;
- effective ACL readback from an ephemeral/test database matches this contract;
- `r9a0_edge_ingest` has zero direct relation/sequence rights and only the exact function allowlist;
- no `service_role` deployment dependency is introduced;
- no credential or secret value appears in Git, CI logs, test fixtures, receipts, or Slack;
- no hosted apply has occurred merely because repository tests are green.

## 11. Hosted-apply authority gate

Repository acceptance is not hosted mutation authority.

A later hosted apply requires Patrick’s explicit authority for the exact R9A0 target and candidate, plus current pre-apply evidence that:

- an independent restorable backup/recovery route exists or the exact governing policy for the mutation permits proceeding without one;
- the narrow authentication mechanism exists without exposing a broad project secret;
- the zero-paid abuse/cost gate from the Edge readiness design is satisfied before invocation, not merely by in-function rejection;
- deployment disable/revocation procedure is tested;
- exact migration candidate and test receipt are immutable and independently reviewed.

## 12. Required completion receipt

A future applied packet is not complete without a receipt binding all of the following, while excluding secret values:

- repository owner/name;
- branch and exact implementation commit;
- exact parent/base commit;
- migration path + SHA-256;
- SQL privilege-test path + SHA-256;
- exact Edge-callable function signatures and definition digests;
- database role name and non-secret role attributes;
- effective ACL snapshot/digest proving zero direct relation/sequence rights;
- exact test/CI run identifiers and outcomes;
- actor/scope configuration digest if deployment is later authorized;
- key identifiers/lifecycle states only, never key material;
- current cost/quota/no-paid-overage evidence required by the Edge gate;
- disable/rollback procedure identifier;
- Patrick’s exact hosted-apply authority receipt;
- post-apply readback showing the same effective privilege surface.

## 13. Current disposition

`REPOSITORY_FIRST_PRIVILEGE_PACKET_SPEC_COMPLETE`

This document completes assignment 3313 at design-contract level only. It authorizes **no** migration apply, role/credential creation, hosted mutation, Edge deployment, paid-service action, production mutation, or `service_role` use.
