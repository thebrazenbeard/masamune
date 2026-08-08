# Mune Review — R9A0 Edge Repository-First Privilege Packet V3

**Assignment:** `VOSS-20260808-MU3` / Vera 3313 V3 rereview  
**Reviewer lane:** Mune  
**Reviewed repository:** `thebrazenbeard/masamune`  
**Reviewed exact commit:** `984cbdc781aa643443652f41f5a710f59e2d2439`  
**Reviewed path:** `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`  
**Reviewed blob:** `6fdee978d0b052592844d1f7356f6fedb13f43eb`  
**Supplied SHA-256:** `c74cc6dba1e6c08e0d7234be1a3e12c93b357b892f11ab6c259852a41804d258`  
**Parent / V2 base:** `0b15da97f55e99165116924f75d94399964e9ded`  
**Observed R9A0 build-ground PostgreSQL version during review:** `17.6`  
**Verdict:** `APPROVED`

## Independent provider and primary-source checks

The exact GitHub file was freshly read at the immutable commit above and returned the expected blob identity.

The R9A0 hosted build-ground project `agvhmutlrolbaijzlbqk` was read-only queried during review and reported PostgreSQL `17.6` (`server_version_num=170006`). This is an observation of the current review target environment, not hosted-apply authority.

PostgreSQL 17 primary documentation confirms the two semantics that caused V2 to fail and that V3 now addresses:

1. `ALTER DEFAULT PRIVILEGES` uses the default privileges of the role that is current at object creation; role-membership defaults are not inherited for this purpose. Per-schema defaults are additive to global defaults, so a per-schema `REVOKE` cannot remove globally/default-granted `PUBLIC EXECUTE`. PostgreSQL 17 also explicitly supports `ON ROUTINES`; for this command `FUNCTIONS` and `ROUTINES` are equivalent and include procedures. Source: https://www.postgresql.org/docs/17/sql-alterdefaultprivileges.html
2. PostgreSQL function-security guidance requires excluding schemas writable by untrusted users from `search_path`; PostgreSQL SECURITY DEFINER guidance uses an explicit trusted path with `pg_temp` placed after trusted schemas. Source: https://www.postgresql.org/docs/17/perm-functions.html and https://www.postgresql.org/docs/17/sql-createfunction.html

## Findings

### 1. `MUNE-3313-002` is closed

V3 no longer relies on the ineffective schema-scoped future-routine revoke. It requires a dedicated `NOLOGIN` creator/owner, `r9a0_edge_api_owner`, and a dedicated Edge-callable schema, `r9a0_edge_api`, then binds the future-routine control to the **global defaults of the exact role that actually executes CREATE**:

`ALTER DEFAULT PRIVILEGES FOR ROLE r9a0_edge_api_owner REVOKE EXECUTE ON ROUTINES FROM PUBLIC;`

There is no `IN SCHEMA` qualifier on the control that claims to remove ambient/default `PUBLIC EXECUTE`.

The broader effect of a global default revoke is bounded by dedicating the creator role to this small API surface and making discovery of unrelated routine creation by that owner a hard failure.

### 2. Creator-role drift is explicitly controlled

V3 correctly rejects the false proof "created as broad runner, then changed OWNER, therefore dedicated-owner defaults applied." It requires either:

- creation while the effective creator is the reviewed dedicated owner; or
- an explicitly enumerated compatibility path that revokes `PUBLIC EXECUTE` on the exact created routine in the same transaction, transfers ownership if required, issues only reviewed grants, and fails if the actual creator is outside the reviewed creator set.

It additionally requires enumeration of every role capable of `SET ROLE r9a0_edge_api_owner` or otherwise creating as that identity. This closes the creation-time identity gap that V2 left ambiguous.

### 3. Current-object and future-object privilege closure are separated correctly

V3 recognizes that default privileges affect future objects, not routines that already exist. Current wrappers must therefore receive explicit same-transaction `REVOKE EXECUTE ... FROM PUBLIC` plus exact named-principal grants, while the dedicated creator's global defaults protect future routines.

The hostile suite also requires effective-principal checks rather than merely inspecting direct ACL text. That is necessary because PUBLIC, ownership, membership, schema privilege, and provider surfaces can reintroduce reachability even when a direct grant looks narrow.

### 4. Function/procedure/routine coverage is adequate for the bound PostgreSQL target

For PostgreSQL 17.6, the proposed `ON ROUTINES` form is supported and PostgreSQL documents it as covering functions and procedures together for default privileges. V3 also requires exact-target-version testing and refuses function-only reasoning when callable procedures/routines could remain exposed.

No version-syntax blocker remains at design level.

### 5. `MUNE-3313-003` is closed

V3 makes the SECURITY DEFINER boundary executable rather than aspirational:

- explicit trusted-only `search_path`;
- `pg_temp` explicitly last;
- writable `public` and user-controlled schemas excluded;
- security-sensitive relation/function/sequence references fully qualified;
- no request-derived dynamic SQL/identifiers;
- hostile temporary-object and writable-public shadow tests;
- definer owner readback bound to the reviewed narrow owner.

This is consistent with PostgreSQL 17 security guidance and closes the temporary-schema masking gap identified in V2.

### 6. Edge privilege remains capability-minimized

`r9a0_edge_ingest` remains non-owner, non-superuser, `NOBYPASSRLS`, with no direct canonical relation or sequence rights and no ambient access to internal API/coordination/governance schemas merely to reach canonical writers.

Its callable surface is limited to one validated write wrapper and, if required for ambiguous-commit recovery, one read-only receipt lookup wrapper. The design explicitly fails if the only way to preserve canonical writes is to expose a broad canonical writer directly to Edge.

### 7. Canonical-write and ambiguous-commit controls survive V3

V3 preserves durable `operation_id` identity, semantic-replay equivalence, changed-semantics conflict rejection, database-owned ordering, validation, no caller-generated sequence override, and no shadow event ledger.

Ambiguous transport outcomes require read-only receipt lookup before any exact-operation retry. Blind repeat remains forbidden.

### 8. Provider and secret boundaries survive V3

`service_role`, `postgres`, broad project secrets, and equivalent administrative credentials remain prohibited as Edge deployment credentials or fallbacks. Provider-generated callable routes must be tested for bypass behavior, and provider behavior that bypasses the intended narrow role is a hard implementation failure rather than justification for privilege expansion.

### 9. Repository-first and authority boundaries survive V3

One immutable implementation head must later bind migration/test digests, creator/default-privilege readback, effective ACL matrix, SECURITY DEFINER definition/search path, canonical-writer dependency, zero relation/sequence rights, exact PostgreSQL version, CI evidence, and absence of unrelated drift.

Repository acceptance remains separate from hosted mutation. V3 authorizes no role/schema creation, migration apply, credential creation, Edge deployment, paid-service action, production mutation, merge, rebase, force push, or native Project mutation.

## Assumption challenge / residual implementation risks

I do not find a design-level blocker on the exact V3 artifact. The remaining risks are deliberately deferred implementation proofs, not reasons to reject V3:

- the eventual migration runner's actual `SET ROLE` / CREATE path must match the reviewed creator model rather than merely produce the desired final owner;
- provider API routing must actually preserve the intended database principal instead of silently using a broader identity;
- effective privilege testing must include membership/ownership/PUBLIC/provider paths, not only `information_schema` direct grants;
- the canonical writer delegation must be proven non-callable directly by Edge while still callable by the reviewed definer;
- branch/head movement before implementation review invalidates inherited acceptance and requires fresh exact-head rebinding.

These are already explicit hard gates in V3.

## Verdict

`APPROVED`

`MUNE-3313-002` and `MUNE-3313-003` are closed by the exact immutable V3 target above. The earlier V2 verdict remains historical and does not transfer to unreviewed successors.

This approval is **design/repository-specification approval only**. It is not implementation acceptance and grants no hosted apply, credential, deployment, paid-service, production, merge, destructive, or native-Project authority. Mune did not modify Masa's reviewed target.