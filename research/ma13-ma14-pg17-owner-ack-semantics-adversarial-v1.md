# MA13 / MA14 Adversarial Pass: PG17 Managed-Role Emulation and Coordination Relation Semantics

**Class:** WORKING_PROJECT / read-only research result  
**Date:** 2026-08-08  
**Actor:** Mune independent verifier  
**Provider/database mutation:** none  
**Producer-branch mutation:** none

## Executive result

Two material findings survive adversarial attack.

1. **MA13 target-incompatibility is stronger than initially stated.** The exact PR2 integrity migration at `58a6ae4d4272165bd5b988bdd7a8bb0e72417302` is not merely insufficiently tested on PostgreSQL 17. Under the presently observed managed Supabase role posture, its first ownership-transfer step is expected to fail unless the migration explicitly establishes both the required `SET ROLE` path to `r9a0_owner` and the target owner's required `CREATE` privilege on the database. Plain `postgres:17` run as Docker superuser will miss this failure class.
2. **MA14's old generic ACK-as-head model is not forward-compatible with the current coordination contract.** Current live evidence shows `acknowledges_event_id` is many-to-one and frequently cross-thread. `supersedes_event_id` is also historically cross-thread in some records. Therefore authoritative currentness cannot be recovered from one global generic chain rule. Prospectively, ACK should be provenance/reference, while state progression is domain-admitted and typed. Legacy history needs an adapter rather than retroactive reinterpretation.

## MA13: exact migration versus live PG17 managed role

### Exact source

PR2 integrity migration:

`supabase/migrations/20260806224900_r9a0_coordination_integrity_repairs.sql`

at exact candidate head:

`58a6ae4d4272165bd5b988bdd7a8bb0e72417302`

The migration creates:

`r9a0_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT`

and then immediately executes:

- `ALTER SCHEMA r9a0_governance OWNER TO r9a0_owner`
- `ALTER SCHEMA r9a0_coordination OWNER TO r9a0_owner`
- `ALTER SCHEMA r9a0_api OWNER TO r9a0_owner`

followed by table, sequence, function and view ownership transfers.

### Live target facts reproduced

Direct current readback on the Vera Supabase target:

- `server_version = 17.6`
- `server_version_num = 170006`
- `current_user = postgres`
- `session_user = postgres`
- `postgres.rolsuper = false`
- `postgres.rolcreaterole = true`
- `postgres.rolinherit = true`
- `createrole_self_grant = ''`
- database ACL for current database includes PUBLIC `TEMP,CONNECT` but not PUBLIC `CREATE`
- `service_role` does not have database `CREATE`

The observed `postgres` role is therefore materially unlike the Docker image bootstrap superuser used by current CI.

### Why the current migration is expected to fail

PostgreSQL 17 documents two independent preconditions for `ALTER SCHEMA ... OWNER TO new_owner`:

1. the actor must be able to `SET ROLE` to the new owner; and
2. the new owner must have `CREATE` privilege on the database.

PostgreSQL 17 also documents that when a non-superuser with `CREATEROLE` creates a role, the created role is automatically granted back with `ADMIN TRUE, SET FALSE, INHERIT FALSE` by default. Thus creation of `r9a0_owner` does **not** itself establish the `SET ROLE r9a0_owner` path required by `ALTER ... OWNER`.

The current migration contains no intervening `GRANT r9a0_owner TO postgres WITH SET TRUE ...` or equivalent. Independently, the current database ACL does not give PUBLIC `CREATE`, so a fresh `r9a0_owner` also lacks the target-owner database privilege required for the first schema ownership transfer.

Therefore the first `ALTER SCHEMA ... OWNER TO r9a0_owner` has two separately missing prerequisites under the observed live posture.

This is a stronger result than merely saying "PG15 CI does not prove PG17." The exact migration is **expected target-incompatible under the current managed role posture unless corrected**. No hosted execution was performed.

### Additional creator/default-privilege trap

The foundation and integrity migrations use schema-local `ALTER DEFAULT PRIVILEGES ... IN SCHEMA ... REVOKE ... ON FUNCTIONS FROM PUBLIC` forms. PostgreSQL 17 explicitly states that per-schema default privileges only add to global defaults and cannot remove a privilege granted globally by the built-in/global function default. Removing default PUBLIC EXECUTE for future functions requires a global default-privilege revoke for the creator role before function creation.

The existing migrations do explicitly `REVOKE ALL ON ALL FUNCTIONS ...` after foundation object creation, which protects those already-created objects in that migration, but this does not make the schema-local default-privilege commands a sound future creator-default proof. MA11's creator-role closure must therefore remain a separate acceptance condition for new admission-owner routines.

### Minimum provider-faithful CI topology

A stronger future PG17 CI target should emulate the managed privilege posture, not merely the version number:

- bootstrap cluster as synthetic superuser `supabase_admin`;
- create a separate login role literally `postgres` with `NOSUPERUSER CREATEROLE`, matching the relevant live attributes;
- set `createrole_self_grant` to the observed target posture;
- make the initial R9A0 schemas/objects owned by the migration runner as the foundation migration naturally would;
- revoke PUBLIC database `CREATE`, retaining only target-faithful baseline database privileges;
- provision contract-relevant `authenticator`, `service_role`, `anon`, and `authenticated` membership structure;
- run the migration as the non-super `postgres` role;
- assert the exact owner-transfer prerequisites and final membership closure;
- record `server_version`, `server_version_num`, runner role attributes, relevant membership options, database ACL class, and target class in the CI receipt.

A plain `postgres:17` superuser job remains useful compatibility evidence but is not provider-faithful privilege evidence.

### Corrective-design caution

Do not "fix" the migration by leaving a permanent broad `SET` or database-`CREATE` path merely so ownership transfer passes. The safe pattern is a reviewed, bounded migration-time ownership-transfer capability with explicit final readback proving runtime roles have no unintended `SET`, `ADMIN`, `CREATEROLE`, owner, or broad creator path. Exact implementation belongs to MA13/MA14/Voss review, not this advisory pass.

## MA14: ACK is not a generic state edge

### Exact PR2 behavior

The exact PR2 integrity migration installs a generic `validate_event_chain()` that:

- computes a thread head by treating either `supersedes_event_id` **or** `acknowledges_event_id` as consuming the predecessor;
- requires every non-initial event to reference exactly one current head;
- rejects cross-thread references;
- creates a unique index on `supersedes_event_id`;
- creates a unique index on `acknowledges_event_id`;
- defines `thread_heads` as events with no successor through either relation.

Its test suite then advances synthetic state using an ACK-only event and expects that event to become `latest_thread_state`.

That model was coherent for its earlier contract. It is no longer coherent with the current live coordination semantics.

### Live counterevidence

Current Vera coordination readback shows:

- many `acknowledges_event_id` parents have multiple children; one observed parent has 18 acknowledging children;
- those many-to-one ACK patterns are not assignment-only. Examples include model-behavior mandates and R8A0 owner-audit / consolidated-manifest work;
- **471** observed ACK references are cross-thread;
- **68** observed `supersedes_event_id` references are cross-thread in retained history.

Therefore:

- unique ACK is factually incompatible with the current coordination usage pattern;
- ACK cannot globally mean "the one state successor";
- same-thread-only ACK is incompatible with substantial retained coordination history;
- historical `supersedes` cannot be globally reinterpreted as a same-thread canonical state edge without a legacy/domain adapter.

### Preferred prospective semantics

For new R9A0 typed coordination, use relation semantics that do not ask one field to perform three jobs:

- `acknowledges_event_id`: **non-state provenance/reference**. Many-to-one is valid. Cross-thread may be valid when the domain contract permits it. ACK never consumes a state slot merely by existing.
- `supersedes_event_id`: **replacement/state-predecessor candidate**, but authoritative state effect is still determined by a typed domain adapter/admission rule, not the generic bus alone.
- assignment state: authoritative only through the E2/admission topology and assignment resolver.
- generic coordination UI: expose `latest_thread_activity` or equivalent, explicitly non-authoritative.
- generic `thread_heads/latest_thread_state`: deprecate as authority-bearing names unless redefined over a closed typed domain.

If an event both advances state and acknowledges a proposal, both relations are legitimate: `supersedes=current_admitted_state`, `acknowledges=accepted_proposal`. This is exactly why a global "exactly one link" validator is structurally wrong for the current contract.

### Non-assignment counterexample challenge

I did not find evidence that a non-assignment domain *needs* ACK itself to be the state-transition primitive. Older records sometimes used ACK that way, but that establishes legacy usage, not a reason to preserve the ambiguity prospectively. A non-assignment domain that wants an acknowledgement to change state can state that explicitly in its typed payload/relation contract and, where appropriate, use `supersedes` for the state edge plus ACK for the acknowledged evidence.

The safer forward-only rule is therefore:

1. preserve legacy bytes and adapt them by version/domain;
2. stop deriving authoritative state from generic ACK;
3. do not globally rewrite historical cross-thread supersedes into same-thread state;
4. add typed/domain constraints for new stateful workflows;
5. retain generic latest-activity views for operations, never authority.

### Required hostile tests

A corrected MA14 test suite should include at least:

- two non-state proposals ACKing the same root are both accepted;
- proposal ACK does not consume the admitted state predecessor slot;
- closure may carry both `supersedes=current_admitted_state` and `acknowledges=accepted_proposal`;
- unadmitted ACK noise cannot change assignment currentness;
- cross-thread ACK provenance accepted/rejected according to explicit domain policy, not a global prohibition;
- cross-thread supersedes in legacy input is adapter-classified, never silently treated as new canonical same-thread state;
- generic latest activity may move without authoritative state moving;
- a domain requiring ACK-as-state must declare that rule in a closed versioned adapter rather than inherit it from bus mechanics;
- replay/idempotency remains operation-bound and does not depend on ACK uniqueness.

## Bottom line

MA13's proposed managed-role emulation is necessary, but it should add the missing **target-owner database CREATE prerequisite** to the existing SET-role concern. The current PR2 migration is expected to fail before meaningful privilege tests under the observed live PostgreSQL 17 managed role posture.

MA14's proposed cleanup is directionally correct, but should avoid globally declaring `supersedes` to be same-thread state across all retained history. The clean cut is prospective typed semantics plus legacy adapters: ACK is provenance, state is domain-admitted, and generic activity is not authority.
