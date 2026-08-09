# Mune MU14 — Provider Evidence Provenance Hostile Audit

**Assignment:** provisional `MU14 / PROVIDER_EVIDENCE_PROVENANCE_HOSTILE` from Voss Slack 2026-08-09 09:32 EDT  
**Peer target:** MA21 provider-evidence provenance direction  
**Build-ground target:** Supabase project `agvhmutlrolbaijzlbqk`  
**Repository:** `thebrazenbeard/vera-R9A0`  
**Class:** read-only provenance/currentness falsification  
**Disposition:** `READY_FOR_REVIEW / PROVIDER_ENVIRONMENT_FACTS_REUSABLE_BUT_CANDIDATE_EXECUTION_REQUIRES_EXACT_MIGRATION_APPLICATION_BINDING`  
**Mutation performed:** none

## Executive verdict

Provider observations and candidate execution proof must remain separate evidence classes.

Fresh build-ground readback proves the hosted R9A0 governance application ledger contains exactly one R9A0 repository migration application:

- migration version `20260806133152`;
- `r9a0_coordination_foundation`;
- migration statements SHA-256 `2a8f64ccf81251a06f23b0adf3bba6f74f43cf322a7719940281ae0f0d7d3df6`;
- repository `thebrazenbeard/vera-R9A0`;
- repository commit `e394132f7269a531029ccd985056f77dd7c726fd`;
- exact applied path `supabase/applied/20260806133152_r9a0_coordination_foundation.sql`;
- target project `agvhmutlrolbaijzlbqk`;
- operation `r9a0-migration-20260806133152-e394132f`.

The provider-native `supabase_migrations.schema_migrations` table likewise contains `20260806133152`, but not the candidate versions `20260806224900`, `20260807005800`, or `20260807020800`.

Fresh catalog negative controls further show:

- `r9a0_coordination.thread_heads` is absent;
- `r9a0_governance.validate_event_chain()` is absent;
- cluster role `r9a0_owner` is absent;
- the foundation-era `latest_thread_state` and `append_coordination_event(...)` do exist.

Those facts are incompatible with claiming exact repo database head `58a6ae4d4272165bd5b988bdd7a8bb0e72417302` is presently applied to the hosted build-ground target.

The repository's own exact `58a6ae4d...` `supabase/MIGRATION_LEDGER.json` agrees: later migrations are marked `hosted_apply_status = NOT_APPLIED...`, while their tests refer to disposable CI runs.

Therefore:

`REPO_DATABASE_HEAD_DISCUSSION != HOSTED_PROVIDER_APPLICATION_PROOF`

and

`PROVIDER_ENVIRONMENT_OBSERVATION != CANDIDATE_EXECUTION_RECEIPT`.

No new bug is declared by MU14 because the exact repository ledger already preserves the distinction. The risk is evidence laundering by downstream review/receipt logic, which MA21 should mechanically prohibit.

## 1. Evidence classes

### A. Provider environment observation

A provider environment observation records facts about the target at an observation cut, such as:

- target project/database identity;
- PostgreSQL version/number;
- current/session principal;
- provider-defined roles and membership options;
- default ACLs/provider schemas/extensions;
- selected live object definitions or grants;
- observation timestamp/cut and query/readback identity.

Fresh build-ground example:

`server_version = 17.6`, `server_version_num = 170006`, current/session user `postgres`.

These facts are reusable for evaluating multiple candidate designs **only to the extent the candidate does not itself mutate the observed fact and the observation remains fresh enough for the consuming decision**.

They do not prove any particular repository migration set ran.

### B. Provider baseline/application state

This binds what the hosted target can actually prove was applied.

For repository-managed migration proof, minimum fields include:

- target project/database;
- migration version/name;
- exact migration statements digest;
- repository/path/source identity;
- repository commit or exact source artifact identity;
- operation/application ID;
- applied_at/applied_by;
- application ledger source;
- any declared provenance deviation;
- post-apply object/state fingerprint when required.

The current build-ground ledger proves foundation application. It does not prove 58a's later migrations.

### C. Candidate execution proof

A candidate execution receipt binds an exact ordered migration/test set to one execution environment:

- repository + candidate/head/merge identity;
- ordered migration paths and digests;
- rollback/test/harness identities where relevant;
- engine/provider fixture identity;
- exact run/operation ID;
- target class or exact target;
- preconditions/pre-state;
- per-step outcomes;
- post-state/readback/digest;
- toolchain identity and provenance limitations.

Historical CI run `31158655712`/the 58a-era database workflow is disposable PostgreSQL evidence. It is not hosted build-ground application proof.

### D. Hosted candidate-application proof

To claim a corrected database successor is actually applied to `agvhmutlrolbaijzlbqk`, the evidence must bind the exact hosted target and the exact admitted migration set. Repo head alone is not sufficient. Object equality alone is not sufficient. A disposable run is not sufficient.

### E. Native↔database integration binding

This separately binds the immutable native candidate/interface context to the exact database candidate/qualification evidence. It is not created merely by observing provider version/roles and not created merely by applying DB migrations.

## 2. Fresh exact hosted-versus-repository reconciliation

### Hosted governance ledger

One row only:

`20260806133152 / r9a0_coordination_foundation / e394132f7269a531029ccd985056f77dd7c726fd`.

Its evidence records `test_status=PASSED`, zero synthetic rows and the allowed R9A0 namespaces.

### Provider migration history

Among the four database-slice migration versions expected by the current repository workflow, only foundation `20260806133152` appears in `supabase_migrations.schema_migrations`.

Missing on the hosted target:

- `20260806224900 r9a0_coordination_integrity_repairs`;
- `20260807005800 r9a0_owner_extensions_usage`;
- `20260807020800 r9a0_service_role_read_policy`.

### Repository 58a ledger

Exact repo head `58a6ae4d...` records those three later migrations as repository-first/disposable-CI verified but with hosted apply status explicitly not applied pending authority/approval.

This is unusually nice provenance behavior by software standards, which means downstream code has no excuse to flatten it.

## 3. Foundation provenance precision

The exact repo `58a` migration ledger contains a historical warning on the one hosted foundation apply:

> the initial apply preceded the exact applied-statement commit; the deviation is retained and must not recur.

Therefore even the foundation application should be described precisely as an applied/tested historical migration with a **recorded provenance deviation**, not ideal evidence that the exact repository commit was prebound before effect dispatch.

The durable hosted row is valuable evidence, but it must not be upgraded beyond its own custody claim.

Future release qualification should require stronger prebound source identity for new hosted effects rather than treating this historical deviation as precedent.

## 4. Hostile matrix

### Hostile A — repo head laundering

Reviewer says: “database head is 58a and provider is PG17.6, therefore 58a is applied on build-ground.”

Expected result: reject. Repo head is source/candidate identity; PG17.6 is provider environment identity. Neither supplies hosted migration application proof.

### Hostile B — shared object laundering

`r9a0_governance.require_service_role()` is observed live and is also discussed while reviewing 58a.

But the exact foundation applied file already creates that helper. Its live existence cannot prove the later integrity/owner/read-policy migrations ran.

Expected result: bind object provenance to the earliest/actual applied source or classify it as observed object state only.

### Hostile C — object-body coincidence without ledger

A DBA manually executes SQL making one hosted function/view byte-equivalent to a repository migration while no migration application receipt exists.

Expected result: `OBSERVED_STATE_MATCH / APPLICATION_PROVENANCE_UNPROVEN`, not “candidate applied.” Object equality may support state equivalence for a narrowly defined property but cannot mint source-route custody.

### Hostile D — partial migration set

Foundation is applied; later integrity migration is not. A review combines foundation object observations and disposable CI results for the later migrations into one “provider-qualified 58a” claim.

Expected result: reject. Candidate-set application is conjunctive over the required migration set/receipts, not a collage of compatible evidence.

### Hostile E — disposable CI target laundering

PG17 or PG15 disposable CI passes an exact candidate.

Expected result: candidate execution evidence for that disposable environment only. Hosted target facts/credentials/control-plane/role topology remain separate.

### Hostile F — target substitution

A provider observation on `agvhmutlrolbaijzlbqk` is cited as proof for the protected Vera production project or a different Supabase target.

Expected result: reject unless the fact is explicitly target-independent and the policy allows such reuse. Database application receipts are always exact-target evidence.

### Hostile G — stale reusable environment fact

A previously observed provider role graph is reused after provider/config/role movement.

Expected result: only the dependent qualification becomes stale/revalidation-required. Historical observation remains true for its cut.

### Hostile H — candidate mutates the supposedly reusable fact

Pre-apply provider readback says `r9a0_owner` absent. Candidate creates/changes `r9a0_owner`. A post-candidate privilege conclusion reuses the pre-apply role graph.

Expected result: invalid. The observation is a precondition/baseline, not final effective-state proof.

### Hostile I — ledger row without post-state proof where behavior matters

An application receipt records exact SQL dispatch but downstream decision needs effective ACL/RLS/owner/function behavior.

Expected result: application identity and effective post-state remain separate axes. Add required post-apply readback instead of assuming SQL text had the intended effect.

### Hostile J — matching migration version with changed bytes

A migration version/name matches but SHA/source differs.

Expected result: provenance conflict. Version string is not content identity.

## 5. Minimum machine contract for MA21

Recommended closed evidence records:

### `PROVIDER_ENVIRONMENT_OBSERVATION_V1`

- target/provider identity;
- observation cut/time;
- engine/platform facts;
- observed object/role/config fields;
- source query/adapter identity;
- freshness/dependency class.

### `MIGRATION_APPLICATION_BINDING_V1`

- exact target;
- migration version/name;
- exact statements SHA-256;
- repository/path/commit or exact prebound source artifact;
- operation/application identity;
- applied_at/by;
- provenance status/deviation;
- post-state fingerprint requirements.

### `DATABASE_CANDIDATE_EXECUTION_RECEIPT_V1`

- exact repository candidate;
- ordered migration-set digest;
- target class/exact target;
- execution toolchain/run identity;
- step outcomes;
- post-state/readback;
- test/rollback/concurrency qualification identities.

### `DATABASE_PROVIDER_QUALIFICATION_CURRENT_V1`

A current projection consuming environment observations + exact candidate execution/application + post-state evidence according to a versioned policy. It must never manufacture hosted application from environment observations.

## 6. Reuse rules

Reusable without rerun when still current and dependency-compatible:

- engine version/number observation;
- provider role topology/default ACL fact, **only for decisions about the same target/cut and only while no relevant candidate/provider change has invalidated it**;
- historical foundation application receipt for historical foundation provenance.

Not reusable as candidate-specific execution proof:

- repo branch/head labels;
- design documents naming a DB head;
- object existence shared with an earlier migration;
- disposable CI pass on another target;
- server-version observation;
- a migration manifest saying what *would* be applied.

## 7. Current bounded conclusion

Current hosted build-ground database state is **not an applied 58a database candidate** on the evidence reviewed.

The strongest supported statement is:

`HOSTED_FOUNDATION_APPLIED_WITH_RECORDED_PROVENANCE_DEVIATION + CURRENT_PROVIDER_ENVIRONMENT_OBSERVED + LATER_58A_MIGRATIONS_DISPOSABLE_CI_ONLY/NOT_HOSTED_APPLIED`.

That distinction is exactly what future provider qualification should preserve. No evidence was found in this audit that warrants a new bug report; the repo ledger itself is explicit. If a consumer currently promotes environment observations into 58a-hosted-application truth, that consumer would be the defect, not Supabase or the migration ledger.

No provider write, repository producer write, schema/role/grant change, credential action, deployment or canonical coordination state was modified by MU14.
