# Mune Adversarial Pass — H17 Effect-Disabled Implementation Staging

**Class:** `WORKING_PROJECT` / read-only architecture critique  
**Peer lane:** H17 / root 3491, Hephaestus advisory request in `#mune` TS `1786195931.211169`  
**Related Mune lane:** MU7  
**Mutation performed:** none

## Executive conclusion

Hephaestus's central correction is right:

> **A staging branch is not a security boundary unless every credential and control-plane path reachable by the staging runtime is also staging-bounded.**

Supabase branch-local database/API credentials are useful and materially isolate the **data plane**. Current first-party docs say every branch is a separate environment with its own database instance, API endpoints, credentials, Auth configuration, Storage and Edge Functions, and changes in one branch do not affect the others.

But a Supabase Management API/PAT/OAuth principal is a different capability plane. It can create/manage/merge branches, and branch merge runs a production deployment workflow. Likewise, a GitHub integration can automatically deploy changes from repository branches and deploy to production when the relevant branch is merged.

Therefore H17 must classify two independent properties:

1. `STAGING_DATA_PLANE_ISOLATED`
2. `PRODUCTION_CONTROL_PLANE_UNREACHABLE`

A branch can satisfy the first while failing the second spectacularly. Humans have achieved this configuration often enough to give it the respectable name "staging."

---

## 1. Provider facts from current Supabase documentation

### Branch isolation

Supabase currently documents:

- each branch is a separate environment with its own Supabase instance and API credentials;
- each branch has its own database instance, API endpoints, authentication settings and Storage buckets;
- branch credentials are unique to the branch;
- changes in one branch do not affect other branches, including database schema/data, Storage, Edge Functions and Auth configuration;
- new branches are data-less by default unless seeded.

Sources:

- https://supabase.com/docs/guides/deployment/branching
- https://supabase.com/docs/guides/deployment/branching/working-with-branches

This supports branch-specific DB/API credentials as a genuine non-production data-plane boundary.

### Production promotion is a separate control-plane capability

Supabase documents that merging a branch into the main project runs a deployment workflow that can:

- configure services;
- apply database migrations and vault secrets;
- seed;
- deploy changed Edge Functions and update function secrets.

The Management API exposes branch create/delete/diff/merge/push/reset/configuration operations under environment read/write permissions. PATs carry user-account privileges; OAuth tokens may be scoped, but an appropriately privileged Management API token can operate the branch/production control plane.

Sources:

- https://supabase.com/docs/guides/deployment/branching
- https://supabase.com/docs/reference/api/introduction

Therefore a staging runtime holding an org/project Management API token or an unconstrained connector that exposes merge/deploy cannot claim `NO_PROD_TARGET` merely because its SQL connection string points at a preview branch.

### Hosted Edge ambient capabilities still exist inside the branch

Current Edge documentation says a hosted function receives by default a project DB URL and secret API keys that bypass RLS.

A branch being isolated does **not** make the function least-privileged inside that branch. It only bounds the likely provider target to that branch if all injected credentials are branch-local and no broader control-plane credential is reachable.

Source:

- https://supabase.com/docs/guides/functions/secrets

Current public docs do not explicitly state on the Edge secrets page that each default `SUPABASE_*` variable is branch-derived. Branch docs separately say each branch has its own instance/endpoints/credentials and isolated Edge Functions. That strongly suggests branch-local defaults, but H17 should require exact runtime readback of non-secret identifiers/endpoint refs rather than turn an inference into a deployment guarantee.

---

## 2. Two-axis staging classification

For each staging runtime, record:

### A. Data-plane target confinement

```text
NONE
BRANCH_LOCAL_ENDPOINT_BOUND
CANARY_PROJECT_BOUND
PRODUCTION_CAPABLE
UNKNOWN
```

Evidence:

- exact project/branch ref;
- DB host/ref;
- API URL/ref;
- credential principal ID/class;
- provider role/scopes;
- negative proof that the credential is rejected by production endpoint where a safe auth-only/introspection test exists;
- no caller-selectable arbitrary project ref in the guarded adapter.

### B. Control-plane reachability

```text
NO_PROVIDER_CONTROL_PLANE
BRANCH_LOCAL_CONTROL_ONLY
PRODUCTION_PROMOTION_CAPABLE
ORG_WIDE_ADMIN_CAPABLE
UNKNOWN
```

Evidence:

- Management API/PAT/OAuth token absence/presence and scope;
- Supabase connector/action surface;
- GitHub app/token repository/Actions/environment permissions;
- CI environment/secret access;
- deployment automation triggers;
- branch merge/push/reset/deploy ability.

A staging environment is production-safe only if the first axis is non-prod bounded **and** the second cannot promote/address production.

---

## 3. Branch-local credentials are sufficient for S1 data-plane isolation only if no promotion credential rides beside them

Hephaestus's S1 model is sound with these refinements:

- use branch-specific DB/API credentials only;
- no Supabase Management API/PAT/org token in the runtime;
- no current broad ChatGPT Supabase connector in that runtime;
- no production DB URL/API URL/service secret;
- no shared environment variable bundle copied from production;
- synthetic seed only;
- all server-derived target refs are exact branch refs;
- publisher/adapter rejects a request whose target ref is not the configured canary/branch identity.

This is enough to test database mechanics such as E2/currentness on a disposable provider surface without granting a route to production.

It is **not** enough to prove V3/H12 least privilege inside the branch if the same hosted Edge function has branch-admin credentials. That is a separate test property.

---

## 4. Do not use managed Edge branch-admin capability to qualify the eventual narrow publisher

A preview branch can safely contain broad branch-local admin credentials from the standpoint of **production isolation** and still be an invalid fidelity test for **provider-principal confinement**.

Example:

- preview Edge function cannot address prod because every default project secret points at branch B;
- function nevertheless has branch service/admin capability in addition to `r9a0_edge_ingest`;
- H17 says production is safe from the test;
- H12 must still say the tested publisher topology is not narrow.

Therefore:

- S1 can test E2/H4 database mechanics using a branch-local admin/runner where explicitly required by test harness;
- S2/S3 confinement tests must use the **same narrow publisher architecture intended for production**, preferably the isolated publisher route from MU7, against canary resources;
- do not accept "nothing escaped preview" as evidence that the publisher itself was least privileged.

`NO_PRODUCTION_REACHABILITY != PROVIDER_PRINCIPAL_CONFINED`.

---

## 5. Management API and current ChatGPT connector must be absent from the staging executor

Current Vera engineering Supabase route has already been observed as broad postgres/admin across multiple projects. H15 independently classifies this as a multi-project admin route.

H17-qualified staging should not try to tame that route with instructions such as "please only use branch X." It should simply not be present in the ordinary staging execution runtime.

The staging executor should have only:

- the exact branch/canary data-plane principal needed by the stage;
- optionally the guarded publisher interface whose own credential is stage-bounded;
- read-only evidence interfaces whose scopes are independently bounded.

A separate human/admin provisioning plane may create/delete branches or configure credentials under explicit authority, but its token must not become available to the tested runtime.

This is the same H14 rule applied to environment creation: **provisioning authority is not runtime authority**.

---

## 6. GitHub/CI is a second promotion plane

Supabase docs explicitly support GitHub-driven deployments, including preview branches and production deployment from `main`.

Thus H17 must inspect GitHub separately:

- can staging CI push/merge to production branch?
- can it write workflow files?
- can it access production GitHub Environment secrets?
- can its token trigger a production deploy workflow?
- does a pull-request merge automatically invoke Supabase production deployment?
- can a preview workflow inherit organization/repository secrets that include production Supabase/other provider credentials?

A branch-local Supabase credential is irrelevant if the same workflow can edit/merge a privileged GitHub workflow that then deploys production.

For S1-S3:

- use canary repository/app installation or tightly scoped branch/repo token where provider testing requires GitHub effects;
- production environments/secrets unavailable;
- no automatic promotion;
- workflow/ref mutation that could reach prod is out of scope or permission-denied.

For S4, actual production topology can be provisioned only under a later exact authority stage, with dispatch still mechanically disabled.

---

## 7. Preview/staging Edge endpoint hostiles

A branch-isolated function may still call arbitrary external networks using an ordinary secret or caller-supplied URL.

Therefore no-prod-target needs more than Supabase ref isolation when the test covers external effects.

Require:

- webhook/API targets are synthetic/canary endpoints;
- target allowlist is publisher/server-derived;
- no production hostname/API account secret in staging environment;
- caller cannot submit arbitrary URL/organization/repository/project target beyond canary ceiling;
- network egress where controllable is limited to required canary/provider endpoints;
- a copied production webhook secret does not exist in staging even if the endpoint itself is absent.

A canary publisher that can phone production Stripe/GitHub/Supabase because DNS exists is not canary-confined just because its database is preview.

---

## 8. Stage model challenge/refinement

### S0 `DESIGN_STATIC`

No provider write credentials. Pure code/schema/test synthesis. Strongest safe stage and should remain usable longest.

### S1 `ISOLATED_DATA_PLANE`

- disposable branch/project;
- synthetic data;
- branch-local credentials;
- no Management API/org token;
- no prod-connected generic Supabase connector;
- no external provider effect capability;
- synthetic H13 identities/capabilities only.

Goal: E2/H4/MA12 database/protocol mechanics.

### S2 `CANARY_EFFECT`

- isolated publisher using canary-only provider principals;
- canary GitHub repo/app token and canary external endpoints;
- branch-local Supabase principal;
- H6 can dispatch only to canary conflict scopes;
- no production credentials in runtime or CI.

Goal: ambiguous outcome, reconciliation and exact capability consumption on non-prod targets.

### S3 `PREPROD_TOPOLOGY`

- same logical issuer/E2/H6/publisher/H14 architecture intended for prod;
- still canary provider resources;
- provider principal privilege *shape* should match prod as closely as provider allows without granting prod targets;
- authorized canary positive/negative probes;
- H14 attests this topology as **preprod**, never transposes target identity into prod attestation.

### S4 `PROD_TOPOLOGY_DISABLED`

Separately authorized future provisioning only:

- narrow prod principals exist;
- publisher dispatch hard-disabled by independent config/capability gate;
- ordinary runtime cannot turn it on;
- H14 attests actual prod credential/tool topology;
- break-glass isolated.

### S5 `EFFECT_ENABLE`

Only after exact release, authority, H14 and provider target/readback gates. Enabling effect is itself a separately authorized state transition/config change, not a side effect of deploying S4.

This stage decomposition is stronger than one vague "staging" environment because it binds which kinds of failure are allowed to have consequences.

---

## 9. Rollback: rebuild is usually safer for disposable data-plane state, but call it rebuild, not rollback

For S1-S3 disposable Supabase branches/projects, I prefer:

`capture evidence -> destroy disposable environment under authorized admin path -> recreate from exact frozen migrations/config/seed -> re-run qualification`

over reverse migrations.

Reasons:

- reverse migrations are additional state transitions that require their own correctness proof;
- they may not restore privileges/defaults/sequence/catalog/provider state exactly;
- they invite a false belief that the environment has returned to a known baseline;
- disposable environments are specifically valuable because reconstruction from source can be the baseline proof.

But two caveats matter:

### A. Do not delete before evidence capture

Preserve privacy-safe:

- exact branch/project identity;
- migration/config/code digests;
- test receipts;
- failure logs without secret values;
- provider version/config readback;
- incident/anomaly record.

Deletion is not evidence erasure policy.

### B. Rebuild evidence must bind the exact source set

A rebuilt branch is qualified only if it was reconstructed from exact:

- repository head/tree;
- ordered migration files/digests;
- branch config digest;
- seed digest;
- Edge/publisher code digest;
- dependency/runtime versions;
- synthetic authority/capability fixture set;
- provider major/version policy.

A new environment with "same branch name" is not the same qualification target.

For production, forward repair remains the safer governance posture. Disposable rebuild semantics do not authorize dropping/recreating real production state.

---

## 10. Paid/service boundary

Current Supabase documentation says preview branching is a Pro-plan feature and branch usage can incur compute/storage/egress charges.

Therefore H17 may specify branches architecturally, but creating/running them is not implied by this design stage and requires the applicable exact Patrick authority/cost posture.

No branch/project creation should occur merely because the design likes branches. Infrastructure has a charming habit of turning architecture diagrams into invoices.

Sources:

- https://supabase.com/docs/guides/deployment
- https://supabase.com/docs/guides/platform/manage-your-usage/branching

---

## 11. H17 release-blocking STOP conditions

STOP the staging test or refuse qualification if any of these holds:

1. staging runtime can address production DB/API endpoint with any reachable credential;
2. Management API/PAT/OAuth token capable of production merge/push/config/deploy is reachable;
3. broad current ChatGPT Supabase admin connector is present in staging executor;
4. prod secret/DSN/API token copied into environment, CI or fixtures;
5. GitHub/CI token can merge/write prod branch/workflow or read prod environment secrets;
6. preview/staging auto-promotion can deploy production without a separate gated authority stage;
7. external effect target is caller-selectable outside exact canary allowlist;
8. staging Edge/publisher has production webhook/API credentials;
9. break-glass principal/credential is reachable by ordinary staging runtime;
10. S2/S3 publisher is broader than the topology being claimed merely because its broad capability is branch-local;
11. canary positive/negative probes are attempted on non-disposable real targets;
12. recreated environment is not bound to exact migration/config/code/seed/runtime evidence;
13. destructive cleanup happens before evidence capture;
14. production data is copied into a preview environment without separate privacy/authority review;
15. required branching/hosting cost action lacks exact authorization.

---

## 12. What branch credentials actually prove

The strongest honest branch-local claim is:

`THIS_DATA_PLANE_CREDENTIAL_TARGETS_ONLY_THIS_SUPABASE_BRANCH_INSTANCE`

if exact provider readback confirms that credential/ref binding.

It does **not** prove:

- runtime lacks a Management API token;
- runtime lacks a second prod credential;
- runtime cannot mutate GitHub and cause prod deployment;
- runtime is least-privileged inside the branch;
- external egress cannot target production systems;
- final production topology is equivalent.

H17 should make these non-substitutions first-class in its checklist.

## Verdict

`BRANCH_LOCAL_DATA_PLANE_IS_A_VALID_STAGING_PRIMITIVE; CONTROL_PLANE_AND_AMBIENT_CAPABILITY_ISOLATION_REMAIN_MANDATORY`

Use Supabase branches for disposable isolated database/API environments only when their branch-specific identity/credentials are exactly bound and the test runtime has no Management API/production promotion capability. For V3/H12 publisher tests, branch isolation alone is insufficient: the tested publisher must also use the narrow runtime/principal topology intended for production.

No Supabase branch/project, credential, secret, GitHub environment, workflow, provider endpoint, deployment or repository producer target was created or modified.