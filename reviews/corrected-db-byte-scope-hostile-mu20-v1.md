# Mune MU20 — Corrected Database Successor Byte-Scope Hostile Review

**Assignment:** provisional `MU20 / CORRECTED_DB_BYTE_SCOPE_HOSTILE`  
**Review target:** Masa `MA28 CORRECTED_DB_SUCCESSOR_BYTE_SCOPE_MANIFEST`, Slack TS `1786289067.905059`  
**Semantic inputs:** MA23 V3 approved by MU15; MA24/MA27 provider qualification; MA17 rollback/provider defects; H45 nonauthorizing authority packet  
**Exact seed:** `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`  
**Disposition:** `PATHSET_APPROVED_11_MODIFY_2_CREATE_0_DELETE; PRE_LEASE_BIND_EXPLICIT_MAPPING_OWNER_AND_WORKFLOW_INTEGRATION_OWNERSHIP`

## Executive verdict

MA28's proposed **11 MODIFY + 2 CREATE + 0 DELETE = 13 changed paths** is a defensible minimum corrected-D source scope relative to exact seed `58a6ae4d...`.

I find **no required path 14** if two semantic ownership points are made explicit in the eventual authority packet:

1. the reviewed mapping for the two foundation-era hosted rows must be owned inside the existing 13-path set, not exist only as Slack prose;
2. `.github/workflows/r9a0-database-validation.yml` must have one exact integration owner because it is CREATE relative to D seed 58a but already exists on the native/Bob lineage.

Exact sorted-newline changed-path digest:

`0898b9e390031556f387e135fd2e13ea2e80ca61b459c8b186edd5b0bb946486`.

No DELETE is technically necessary. Historical incompatible artifacts can remain immutable if the new manifest/lifecycle classification prevents them from regaining current authority.

## 1. Independent seed verification

Fresh GitHub compare independently reproduces MA28:

`71b3fc4892df3a70e493e287542e68bfa1e5a798 -> 58a6ae4d4272165bd5b988bdd7a8bb0e72417302`

is exactly:

- 44 commits;
- 19 changed paths.

Exact 58a DB manifest is V2 with `file_count=22`.

Fresh direct path probes also prove both proposed CREATE paths are absent at 58a:

- `.github/workflows/r9a0-database-validation.yml` => 404 at 58a;
- `scripts/supabase/test_r9a0_postgrest_provider_contract.sh` => 404 at 58a.

Therefore their D-seed classification as CREATE is correct.

## 2. Approved 13-path set

### MODIFY, 11

1. `docs/database/R9A0_DATABASE_SLICE_MANIFEST.json`
2. `docs/database/R9A0_PRIVILEGE_MATRIX.md`
3. `docs/database/R9A0_RECOVERY_AND_ROLLBACK.md`
4. `docs/database/R9A0_SUPABASE_ARCHITECTURE.md`
5. `scripts/supabase/test_r9a0_two_session_concurrency.sh`
6. `supabase/MIGRATION_LEDGER.json`
7. `supabase/execution/20260806224900_r9a0_coordination_integrity_repairs.sql`
8. `supabase/migrations/20260806224900_r9a0_coordination_integrity_repairs.sql`
9. `supabase/rollbacks/20260806224900_r9a0_coordination_integrity_repairs.down.sql`
10. `supabase/tests/20260806224900_r9a0_coordination_integrity_repairs.test.sql`
11. `supabase/tests/20260807020800_r9a0_service_role_read_policy.test.sql`

### CREATE, 2

12. `.github/workflows/r9a0-database-validation.yml`
13. `scripts/supabase/test_r9a0_postgrest_provider_contract.sh`

### DELETE, 0

No delete is required to produce a truthful corrected successor.

## 3. Why each MODIFY is actually required

### Manifest

Current exact manifest binds 22 old files and treats the old review as an ordinary package member with no semantic lifecycle class. With ten old manifest members modified and two new members created, the successor manifest should bind **24 content members** if nothing is deleted.

The manifest itself is a changed control file outside its own content-member list, as in V2.

V3 needs at least:

- exact 24 member identities/hashes after freeze;
- lifecycle/evidence class sufficient to mark old `R9A0_DATABASE_SUCCESSOR_REPAIR_REVIEW.md` historical;
- exact workflow/PostgREST harness identities;
- exact migration/execution parity identities;
- content commit/external receipt boundary without self-reference.

### Privilege matrix

Required by independently verified provider differences and bugs: service_role BYPASSRLS reality, dedicated owner, direct base mutation denial, exact API USAGE/EXECUTE, default ACL behavior, admin/authenticator topology. Old “RLS policy equals service-role confinement” prose is insufficient.

### Recovery / rollback

Required for MA17 rollback equivalence and MA23 V3 phase boundary:

- precanonical rollback/reapply;
- exact predecessor fingerprint restoration;
- role/default ACL/dependency cleanup;
- post-`SUCCESSOR_CANONICAL` destructive-down refusal;
- forward-only or separately authorized recovery epoch after source flip.

### Architecture

Required to own current normative design rather than rewriting the historical repair review:

- orthogonal events/state/evidence;
- hybrid cutover;
- auth family B;
- P0-P6 evidence classes;
- provider-environment vs application/qualification provenance;
- P3 vs P4 nonlaundering.

### Concurrency harness

Current harness tests the obsolete same-thread/single-chain model. Correct D needs state-lineage/workload snapshot CAS/batch retry/concurrency hostiles under MA23, not merely old head serialization.

### Migration ledger

Must preserve hosted foundation-only truth while binding corrected, still-unshipped D candidate identities. Do not rewrite the historical foundation provenance deviation into ideal custody.

### 224900 migration + execution pair

These are the actual corrected successor bytes and must remain byte-identical at freeze. They own the structural fixes: owner collision/admission, role hardening, effective default ACL policy, orthogonal relation model, source/cutover state, operation receipts, state/workload append machinery, auth family B helpers/RPCs, exact ACL confinement and compatibility migration from foundation.

### 224900 rollback

Required because current rollback is materially wrong. It must restore the declared predecessor state and obey the MA23 V3 precanonical/postcanonical destruction boundary.

### 224900 test

Must carry the bulk of MA17/23/24 SQL-level hostiles: role provenance, ACL/defaults, relation types, state transitions, evidence nonconsumption, cutover operation IDs, selector/source phase, retry, workload CAS, rollback fingerprints and provider-like principal prerequisites that can be tested in SQL.

### 070208 test

Exact current test is stale: it sets legacy `request.jwt.claim.role`, uses postgres -> `SET ROLE service_role`, and reads old `latest_thread_state`. Modifying the test while preserving the 070208 migration as compatibility history is justified. The rewritten test must not claim the permissive RLS policy proves hosted service-role authorization/confinement because provider service_role is BYPASSRLS.

## 4. Why the 12 old members can remain KEEP

The 22-file V2 manifest minus the ten modified members leaves twelve unchanged members:

- historical `R9A0_DATABASE_SUCCESSOR_REPAIR_REVIEW.md`;
- foundation applied copy;
- foundation source migration;
- foundation rollback;
- foundation test;
- 070058 migration/execution/rollback/test;
- 070208 migration/execution/rollback.

I agree with MA28 that these need not be edited solely to make history look current.

Notably, the old review currently says acknowledgements help consume controlling tips and presents the former six-finding/same-thread design as the repair. **Do not rewrite that document.** The new manifest/architecture must classify it `HISTORICAL_AUDIT` so no current qualification or migration logic consumes its prose as authority.

The 070208 migration only creates named SELECT policies. On a hosted BYPASSRLS service_role those policies are not the provider confinement mechanism, but retaining the exact unshipped compatibility migration is not harmful if the corrected 224900 + privilege/qualification layers own real mutation confinement and the rewritten 070208 test stops making false provider claims.

## 5. Required pre-lease binding A — foundation-row mapping ownership

MA23 V3 requires the two hosted foundation-era rows to be classified by an explicit reviewed mapping artifact, never heuristic relation typing.

MA28's 13 paths are sufficient **only if the authority packet says exactly where that mapping lives**.

Recommended no-path-expansion ownership:

- normative mapping representation / migration consumption: corrected `20260806224900...migration.sql` and byte-identical execution copy;
- mapping hostiles / exact expected rows: `20260806224900...test.sql`;
- architecture meaning + historical source class: `R9A0_SUPABASE_ARCHITECTURE.md`;
- exact source/artifact/hash membership: V3 DB manifest.

A separate mapping file is unnecessary if those existing paths contain a closed machine-readable mapping and exact tests. But “the mapping was reviewed in Slack” is not enough for an executable migration packet.

At minimum bind:

- legacy store/project identity;
- exact foundation row/event IDs or exact immutable selectors that cannot accidentally match later rows;
- expected source digests/shape;
- resulting classification: historical envelope vs non-consuming evidence;
- mismatch result `UNRESOLVED_EXISTING_EVENTS` / fail closed.

## 6. Required pre-lease binding B — workflow integration ownership

At D seed 58a the database workflow is absent, so MA28 correctly calls it CREATE.

On the native/Bob lineage the path already exists with historical PG15 workflow semantics. Therefore future composition has a known add/add/logical ownership collision if D is literally forked from 58a.

This does **not** require path 14. It requires one exact ownership strategy before D writer publication:

### Strategy A — D owns corrected workflow content

D branch may create the corrected PG17/PostgREST workflow for self-validation. Integration branch later resolves the known collision by taking the exact reviewed D workflow bytes under one transferred/integration writer lease. Native writer does not concurrently patch the DB workflow.

### Strategy B — choose a D publication base that already contains the workflow path

Then the scope classification for that exact publication base changes from CREATE to MODIFY, while the semantic changed-path set remains one workflow path. The authority packet must recompute path arithmetic against the actual base.

What is forbidden is two writers independently “fixing” the same workflow and leaving integration to divine intent from YAML confetti.

## 7. New workflow/harness are justified, not convenience sprawl

### Database workflow CREATE

The historical workflow cannot satisfy current MA24 requirements: it is PG15/superuser-shaped, lacks provider PostgREST HTTP qualification, uses mutable tool/action/runner identities, and emits the older receipt model.

The corrected workflow should be thin orchestration over pinned PG17/PostgREST fixture identities and exact source/harness digests, with a typed P3+P5 receipt.

### PostgREST provider-contract harness CREATE

A separate deterministic HTTP/provider harness is justified because PostgREST exposure/JWT/Content-Profile/PGRST106/PGRST202 semantics are not the same test axis as database concurrency. Combining them would couple unrelated procedures and make qualification identity harder to audit.

One new script is enough; no separate compose/config/requirements path is required if the workflow/harness own a closed, pinned, hermetic fixture.

## 8. No hidden provider/config path

MA27 P4 hosted exposed-schema configuration is an external provider/control-plane fact. It does not belong in this source path count.

Given current target naming/purpose drift (`agvh...` now Project Lantern), this separation is especially important. Correct D source qualification can use disposable P3 and read-only provider topology evidence without assuming permission to mutate Project Lantern hosted configuration.

No credential file, hosted config file or production target path should be smuggled into D source merely to make P4 convenient.

## 9. Required manifest arithmetic

If MA28 remains `11 MODIFY + 2 CREATE + 0 DELETE` relative to 58a:

- changed source paths = 13;
- V2 content members = 22;
- ten of those members change;
- twelve remain byte-identical historical/predecessor members;
- two new content members are added;
- successor DB content manifest should therefore bind **24 members**.

The changed-path count and manifest member count are different dimensions. Do not report “13-file database package” merely because 13 files changed.

## 10. Final scope verdict

`PATHSET_APPROVED_11_MODIFY_2_CREATE_0_DELETE`.

No mandatory path 14 was found.

Before a D writer lease is authority-request eligible, H45/Voss should bind:

1. exact 13-path list + digest `0898b9e390031556f387e135fd2e13ea2e80ca61b459c8b186edd5b0bb946486`;
2. exact publication base and resulting CREATE/MODIFY classification;
3. one writer / branch / expected head;
4. explicit foundation-row mapping ownership inside the existing 13 paths;
5. explicit DB-workflow integration ownership/collision strategy;
6. no DELETE;
7. exact no-hosted-effect boundary;
8. MA23 V3 / MA24 / MA27 / MA17 semantic input versions;
9. stop on path14, unexpected branch movement, mapping ambiguity or workflow ownership conflict.

With those bindings, the 13-path scope is sufficiently closed for Patrick to authorize if he chooses. This review does not itself grant that authority.

No Vera-R9A0 repository producer byte, Project Lantern/Vera provider state, schema/role/grant, credential, merge, deployment, installation or canonical coordination state was modified by MU20.