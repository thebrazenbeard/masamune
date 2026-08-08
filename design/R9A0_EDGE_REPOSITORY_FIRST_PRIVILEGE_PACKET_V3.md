# R9A0 Edge Repository-First Least-Privilege Packet V3

**Status:** `NON_EXECUTING_PRIVILEGE_PACKET_V3_READY_FOR_INDEPENDENT_REREVIEW`  
**Assignment:** Vera coordination sequence `3313`  
**Parent / V2 immutable base:** `0b15da97f55e99165116924f75d94399964e9ded`  
**Superseded design artifact:** `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V2.md`  
**Controlling corrections:** `MUNE-3313-002` and `MUNE-3313-003`  
**Product target:** `thebrazenbeard/vera-R9A0` database surface, future separately authorized implementation only  
**Hosted apply authorized by this document:** `NO`  
**Credential creation authorized by this document:** `NO`  
**Deployment authorized by this document:** `NO`  
**Paid-service action authorized by this document:** `NO`

## 1. Decision

V3 preserves the repository-first / least-privilege direction of V2 but replaces the unsafe shared-schema future-routine default-privilege model.

The preferred architecture is now deliberately split:

- execution principal: `r9a0_edge_ingest`
- dedicated routine creator/owner: `r9a0_edge_api_owner`
- dedicated Edge-callable API schema: `r9a0_edge_api`

`r9a0_edge_api_owner` is a dedicated `NOLOGIN` owner/creator. It is not the Edge runtime identity. `r9a0_edge_ingest` remains a non-owner, non-superuser execution role with no broad administrative or data privileges.

The dedicated schema is not a second coordination authority. Its wrappers may only delegate into the canonical R9A0 coordination contract. It may not own a parallel event table, shadow ledger, generic SQL gateway, or alternate workflow state.

`service_role`, `postgres`, broad project secrets, or equivalent administrative credentials remain forbidden as Edge deployment credentials or fallbacks.

## 2. Why V2 is superseded

V2 correctly identified PostgreSQL `PUBLIC EXECUTE` as an ambient authority source, but its illustrative future-routine control used a schema-scoped default-privilege revoke:

```sql
ALTER DEFAULT PRIVILEGES FOR ROLE r9a0_owner IN SCHEMA r9a0_api
  REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

That is not a valid closure of PostgreSQL's global/default `PUBLIC EXECUTE` grant. Per-schema default privileges are additive to global defaults; a schema-scoped revoke does not subtract a globally/default-granted execute privilege unless reversing a matching per-schema grant.

V3 therefore requires a **global routine default revoke for the exact role that actually performs CREATE**, and narrows the blast radius by giving Edge-callable wrappers a dedicated creator/owner and schema.

V2 also required a safe `search_path` but did not make the temporary-schema rule executable enough. V3 requires trusted schemas first and explicit `pg_temp` last, plus fully qualified security-sensitive object references and hostile temp-shadow tests.

V1 and V2 remain immutable historical evidence. V3 is forward repair only.

## 3. Required role posture

### 3.1 Execution role: `r9a0_edge_ingest`

Specification only; exact hosted implementation is separately gated:

```sql
ALTER ROLE r9a0_edge_ingest
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOINHERIT
  NOREPLICATION
  NOBYPASSRLS;
```

The role must not own schemas, relations, sequences, routines, policies, triggers, extensions, or storage objects.

Whether it is `LOGIN` or `NOLOGIN` is a later authentication-transport decision. No password, JWT signing key, service-role key, connection string, or other secret belongs in Git or this packet.

### 3.2 Dedicated creator/owner: `r9a0_edge_api_owner`

Required posture:

- `NOLOGIN`
- `NOSUPERUSER`
- `NOCREATEDB`
- `NOCREATEROLE`
- `NOREPLICATION`
- `NOBYPASSRLS`
- owns `r9a0_edge_api`
- owns the Edge write wrapper and optional receipt wrapper
- is the only ordinary role permitted to create routines in `r9a0_edge_api`
- does not become an Edge execution credential

The implementation must enumerate every role capable of `SET ROLE r9a0_edge_api_owner` or otherwise creating an object as that creator. Broad inherited membership is not a substitute for proving the role that actually executes `CREATE`.

If the implementation cannot prove which role actually creates each protected routine, hosted apply stops.

## 4. Dedicated schema boundary

Create/use a dedicated schema:

`r9a0_edge_api`

Required schema rules:

1. owner is `r9a0_edge_api_owner`;
2. `PUBLIC` receives no `CREATE`;
3. `r9a0_edge_ingest` receives `USAGE`, never `CREATE`;
4. no unrelated migration/runtime role receives persistent `CREATE` merely for convenience;
5. if a migration runner must temporarily assume the dedicated creator role, the migration/test receipt must prove the actual creation identity and final membership/privilege state;
6. Edge receives no `USAGE` on `r9a0_api`, `r9a0_coordination`, `r9a0_governance`, or other internal schemas solely to reach canonical tables/functions. The wrapper owner performs the narrow delegation instead.

Provider-default access to `public` must be independently checked. Any path allowing Edge to create objects, reach unrelated routines, or exploit writable resolution namespaces is a blocker.

## 5. Routine default-privilege closure

The creator's **global** routine default must remove ambient `PUBLIC EXECUTE`.

Illustrative posture, exact syntax bound to the target PostgreSQL version during implementation review:

```sql
-- Specification only; do not apply from this document.
ALTER DEFAULT PRIVILEGES FOR ROLE r9a0_edge_api_owner
  REVOKE EXECUTE ON ROUTINES FROM PUBLIC;
```

If the target version requires function/procedure-specific syntax rather than `ROUTINES`, the implementation must cover every callable routine class supported by that version. Function-only wording is insufficient if procedures remain exposed.

This global revoke intentionally affects **all future routines created by `r9a0_edge_api_owner`**, not only routines in `r9a0_edge_api`. That broader effect is acceptable only because V3 makes the creator dedicated to this tiny API surface. The implementation must fail if the owner is discovered to create unrelated application routines.

No `IN SCHEMA` form may be used as the control that claims to remove the global/default `PUBLIC EXECUTE` grant.

## 6. Current-routine ACL closure

Default privileges affect future object creation, not already-created routines. Therefore the reviewed migration must atomically close current routine ACLs as well.

For every current routine owned by `r9a0_edge_api_owner` in `r9a0_edge_api`:

1. inventory exact identity arguments/signature, owner, security mode, ACL and effective execute principals;
2. `REVOKE EXECUTE ... FROM PUBLIC` explicitly on the created routine in the same reviewed migration transaction;
3. grant only the exact legitimate named principals/signatures required by the contract;
4. grant `r9a0_edge_ingest` only the exact Edge allowlist;
5. prove no role membership, ownership, provider default, extension, schema privilege, or `PUBLIC` path restores non-allowlisted execution.

Edge-callable symbols are limited to:

- one write wrapper for a complete validated coordination-ingest request;
- optionally one read-only receipt lookup wrapper keyed by the same durable `operation_id` when required to resolve ambiguous write outcomes.

No `EXECUTE ON ALL FUNCTIONS`, `EXECUTE ON ALL ROUTINES`, wildcard grant, broad default execute grant, or `PUBLIC EXECUTE` fallback is permitted.

## 7. Creator-role drift is a hard failure

PostgreSQL default privileges are selected from the role that actually creates the object. A migration performed as a broad runner and followed by `ALTER ... OWNER TO r9a0_edge_api_owner` does **not** prove that the dedicated owner's default privileges governed object creation.

The implementation must use one of these bounded strategies and prove which one occurred:

### Strategy A: create as the dedicated creator

The migration performs creation while the effective creator is `r9a0_edge_api_owner` (for example through an authorized, tightly bounded `SET ROLE` path), then reads back the owner and ACL/default-privilege posture.

### Strategy B: explicit same-transaction closure

If provider/tooling constraints prevent creation under the dedicated creator role, the same transaction must:

1. create the routine under the explicitly enumerated migration role;
2. immediately revoke `PUBLIC EXECUTE` on that exact routine;
3. transfer ownership to the dedicated owner if required;
4. issue only the exact reviewed grants;
5. verify final owner and effective ACLs;
6. fail the migration/test gate if the actual creator role was not one of the reviewed creator paths.

Strategy B does not waive the dedicated owner's global future-routine default closure. It is a bounded compatibility path, not permission for arbitrary creators.

Any newly introduced creator role is denied by default until its creation path and global routine defaults are explicitly reviewed.

## 8. SECURITY DEFINER hardening

If the Edge wrapper is `SECURITY DEFINER`, it must be treated as a privileged API boundary.

Required controls:

- owner is the dedicated narrow `r9a0_edge_api_owner` or an exact separately reviewed equivalent;
- no dynamic SQL constructed from request values;
- every security-sensitive relation/function/sequence reference is fully qualified;
- explicit trusted-only `search_path`;
- `pg_temp` appears explicitly last;
- writable `public` or user-controlled schemas are absent;
- extension/provider schemas are included only when exact dependency and trust posture are reviewed;
- wrapper arguments are validated before canonical delegation;
- wrapper cannot expose arbitrary SQL, arbitrary relation names, arbitrary routine names, generated sequence values, or privilege-changing operations.

Illustrative posture:

```sql
SET search_path = pg_catalog, <exact_trusted_dependency_schemas>, pg_temp;
```

This is illustrative, not permission to include any schema merely because it is named "trusted". Exact dependencies must be bound to the implementation head.

## 9. Canonical-write preservation

The Edge write wrapper must preserve the canonical R9A0 coordination semantics:

- durable `operation_id` identity;
- identical semantic replay returns the existing canonical effect/receipt;
- same `operation_id` with changed canonical semantics fails closed;
- database-owned sequence/event ordering;
- request/event validation;
- existing source/target/thread/event-type constraints;
- no caller-supplied database sequence/generated identity override;
- no direct Edge table write;
- no alternate event table or shadow ledger.

The wrapper may delegate to an existing canonical writer that itself has broader internal privileges. That dependency does **not** make the canonical writer directly executable by `r9a0_edge_ingest`.

If preserving the canonical writer requires giving Edge direct execute on a broad internal routine, the design fails and must be revised.

## 10. Relation and sequence posture

`r9a0_edge_ingest` receives zero direct privileges on canonical relations/sequences.

Tests must prove absence of effective:

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `TRUNCATE`
- `REFERENCES`
- `TRIGGER`
- sequence `USAGE`
- sequence `SELECT`
- sequence `UPDATE`
- `nextval`
- `setval`

Receipt retrieval is allowed only through the exact read-only wrapper, never through a table/view grant that expands the API.

## 11. Ambiguous-commit contract

An ambiguous transport outcome is not permission to blindly repeat a write.

Required behavior:

1. send one canonical request with one durable `operation_id`;
2. clear commit -> return canonical receipt;
3. clear reject -> return stable rejection;
4. ambiguous commit state -> perform read-only receipt lookup by `operation_id`;
5. matching identity + same canonical request digest -> return existing receipt;
6. matching identity + different digest/semantics -> fail `OPERATION_ID_CONFLICT`, zero new effect;
7. no receipt -> only then may the exact same operation be retried.

The receipt lookup itself cannot mutate state.

## 12. Required hostile / negative tests

A future repository implementation is incomplete unless exact-head tests prove all of the following using **effective privileges**, not only direct ACL text.

### 12.1 Creator/default privilege tests

- `r9a0_edge_api_owner` global routine defaults do not grant `PUBLIC EXECUTE`;
- a newly created unrelated routine by the dedicated owner is non-executable by `PUBLIC` and `r9a0_edge_ingest` before explicit grant;
- schema-scoped default revoke alone is rejected as insufficient evidence;
- alternate/unreviewed creator cannot create in `r9a0_edge_api`;
- actual creator-role readback differs from reviewed creator -> fail;
- creating as a broad migration role then changing owner cannot pass merely because final ownership looks correct;
- functions and procedures/routines are covered for the exact PostgreSQL version.

### 12.2 Role / membership tests

Must deny:

- membership in `postgres`, `service_role`, `r9a0_owner`, or other broad writer/admin roles;
- `SET ROLE` into an unreviewed broader role;
- database/role/extension/schema administration;
- object ownership by `r9a0_edge_ingest`.

### 12.3 Direct-data tests

Must deny every direct canonical relation/sequence access listed in section 10 and deny convenience views/functions outside the exact wrapper allowlist.

### 12.4 API-surface tests

Must deny:

- execute on every routine outside the exact allowlist through direct grants, `PUBLIC`, ownership and membership;
- residual `PUBLIC EXECUTE` on Edge-owned routines;
- wildcard/default privilege expansion;
- new unrelated routine execution before explicit grant;
- callable bypass through `public`, extension, provider-default or other schemas;
- malformed payload, unsupported event type, disallowed source/target/thread scope, missing operation identity;
- same `operation_id` with changed canonical payload digest;
- caller-supplied generated identity/sequence fields;
- use of receipt lookup as a write path.

Must pass:

- one valid scoped ingest through the wrapper;
- identical replay returning the same durable effect/receipt;
- ambiguous-outcome lookup returning the committed receipt with zero duplicate event.

### 12.5 SECURITY DEFINER hostile tests

- attacker creates same-named table/view/function in temporary schema -> wrapper still reaches only fully qualified trusted object;
- attacker creates same-named object in writable `public` -> no effect;
- `SHOW`/catalog readback proves explicit `pg_temp` last in configured search path;
- no dynamic identifier substitution can redirect the privileged operation;
- current definer owner remains the reviewed narrow owner.

### 12.6 Provider / secret tests

- no `service_role` or equivalent broad secret in Edge config;
- no credential value in Git, CI logs, fixtures, receipts or Slack;
- provider-generated callable routes do not expose non-allowlisted routines to the Edge principal;
- any provider API that bypasses the intended database role causes implementation failure rather than a fallback to broader authority.

## 13. Repository-first verification gate

Before any hosted apply, one immutable product-repository head must bind:

- migration path + digest;
- SQL privilege/negative test path + digest;
- exact parent/base;
- exact PostgreSQL version expected by syntax/tests;
- dedicated schema/owner/execution-role identifiers;
- complete protected routine inventory;
- actual routine creator path(s);
- current routine ACL readback;
- creator global default-privilege readback;
- effective execute-principal matrix;
- SECURITY DEFINER definition/search-path readback;
- canonical-writer dependency and proof Edge cannot call it directly;
- zero direct relation/sequence rights;
- no `service_role` deployment dependency;
- all existing database validation suites green;
- no unrelated repository/native-project drift;
- no hosted mutation merely because CI is green.

Unexpected branch movement invalidates the candidate and requires fresh rebinding/review.

## 14. Forward repair and rollback

Repairs remain monotonic:

1. add a new migration/reviewed API symbol;
2. make tests fail against the previous broad behavior first;
3. preserve canonical coordination rows and operation identity;
4. never rewrite an already-applied migration in place;
5. retire superseded grants only after exact-head review.

Rollback removes Edge reachability, not canonical data:

1. revoke/disable Edge credential at deployment boundary;
2. revoke Edge execute on write/receipt wrappers;
3. terminate dedicated execution sessions if required;
4. revoke Edge schema `USAGE`;
5. remove wrapper functions only after dependency proof;
6. drop execution role only after ownership/dependency readback proves it owns nothing;
7. preserve canonical coordination/governance rows and migration history.

No rollback deletes canonical events merely to erase the Edge deployment.

## 15. Hosted-apply authority gate

Repository acceptance is not hosted mutation authority.

A future hosted apply requires Patrick's explicit authority for the exact R9A0 target and immutable implementation candidate, plus then-current evidence for recovery/backup policy, narrow authentication, zero-paid cost/abuse gating, disable/revocation procedure, and independent exact-head review.

Nothing in V3 authorizes role creation, schema creation, migration execution, credential provisioning, Edge deployment, paid service use, production mutation, or `service_role` use.

## 16. Required future completion receipt

A future applied implementation must bind, without secret material:

- repository owner/name;
- implementation branch/head and exact parent;
- migration/test paths and digests;
- database/PostgreSQL version;
- dedicated schema, owner and execution-role names;
- role attribute/membership readback;
- protected routine inventory and definition digests;
- exact actual creator role for each routine;
- global default-privilege readback for each reviewed creator;
- effective ACL matrix proving zero ambient `PUBLIC`/non-allowlisted Edge execution;
- exact Edge-callable signatures;
- SECURITY DEFINER owner/search-path readback and hostile-test result;
- effective relation/sequence denial snapshot;
- canonical-writer delegation proof;
- exact CI/test identifiers;
- no-broad-secret/config evidence;
- hosted-apply authority receipt;
- post-apply readback matching the reviewed privilege surface.

## 17. V3 delta from V2

V3 changes only the privilege-boundary design needed to close the newly confirmed defects while preserving V2's accepted repository-first, canonical-write, ambiguous-commit, least-privilege, service-role-exclusion, zero-paid and no-hosted-effect constraints.

Material changes:

1. replaces shared `r9a0_api` Edge exposure with dedicated `r9a0_edge_api`;
2. introduces dedicated `NOLOGIN` routine creator/owner `r9a0_edge_api_owner`;
3. replaces ineffective schema-scoped default revoke with global creator-role routine default revoke;
4. explicitly binds default privileges to the role that actually executes `CREATE`;
5. rejects create-as-broad-role + owner-transfer as proof of dedicated-owner defaults;
6. requires function + procedure/routine coverage appropriate to target PostgreSQL;
7. makes SECURITY DEFINER search-path order executable with explicit `pg_temp` last and fully qualified sensitive references;
8. adds hostile alternate-creator, creator-drift, temp-shadow, provider-route and canonical-writer-direct-exposure tests.

## 18. Current disposition

`REPOSITORY_FIRST_PRIVILEGE_PACKET_V3_READY_FOR_INDEPENDENT_REREVIEW`

V3 is a non-executing design artifact. V1/V2 history is preserved. No merge, rebase, force push, hosted apply, schema/role creation, credential action, Edge deployment, paid-service action, production mutation, native Project mutation, or canonical-memory write is authorized by this document.
