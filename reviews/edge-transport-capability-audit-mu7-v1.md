# Mune MU7 — Edge Transport / Capability Audit V1

**Assignment:** `VOSS-20260808-MU7` / canonical root sequence `3465`  
**Class:** `READ_ONLY_PROVIDER_AUDIT`  
**Reviewed design basis:** MU3-approved R9A0 Edge privilege packet V3 + H11/H12 authority/confinement model  
**Build-ground Supabase project:** `agvhmutlrolbaijzlbqk`  
**Live PostgreSQL:** `17.6`  
**Mutation performed:** none  
**Verdict:** `DIRECT_NARROW_PRINCIPAL_FEASIBLE; MANAGED_EDGE_NOT_CURRENTLY_CAPABILITY_CONFINED`

## Executive conclusion

V3's narrow execution principal is technically feasible. Supabase supports ordinary custom Postgres login roles, direct/pooler database connections, and a PostgREST/Data API model in which `authenticator` validates a JWT and changes into a database role. The problem is not whether `r9a0_edge_ingest` can exist or receive exact wrapper `EXECUTE`.

The blocker is **where that narrow principal runs**.

Current first-party Supabase documentation says hosted Edge Functions receive broad project capabilities by default, including a direct database URL and secret API keys that bypass RLS. The current `@supabase/server` authenticated-user pattern also exposes both an RLS-scoped `ctx.supabase` and a privileged `ctx.supabaseAdmin` that bypasses RLS. Service-to-service `auth:'secret'` explicitly yields the admin client.

Therefore:

> **A hosted managed Edge Function does not become V3/H12 least-privilege merely because its intended code path uses `r9a0_edge_ingest`, a user JWT, or an exact wrapper.**

The runtime still has documented ambient broader capability unless a provider-supported per-function containment control is separately demonstrated.

Best current implementation direction for V3's hard capability boundary is an **isolated guarded publisher runtime outside the default managed-Edge capability envelope**, holding only a dedicated narrow Postgres credential or equivalently narrow Data API credential path. A self-hosted/externally controlled Deno/server runtime is technically possible, but changes infrastructure/deployment/cost responsibility and therefore needs a separate design/authority stage.

The current hosted Supabase Edge target remains:

`IMPLEMENTATION_BLOCKED_ON_AMBIENT_ADMIN_CAPABILITY_CONTAINMENT`.

---

## 1. Fresh build-ground evidence

Read-only live inspection of `agvhmutlrolbaijzlbqk` confirms:

- PostgreSQL `17.6`;
- current tool route executes as `postgres`;
- `postgres` is LOGIN, CREATEROLE, CREATEDB, REPLICATION and BYPASSRLS;
- `authenticator` is LOGIN, NOINHERIT and not BYPASSRLS;
- `service_role` is NOLOGIN but BYPASSRLS;
- `authenticator` has membership allowing `SET` into `anon`, `authenticated` and `service_role` on the current platform posture;
- `r9a0_edge_ingest` does not yet exist;
- `r9a0_edge_api_owner` does not yet exist;
- `r9a0_edge_api` schema does not yet exist.

Thus MU7 is transport feasibility only. There is no hidden implementation to inherit or accidentally bless.

---

## 2. First-party provider facts used

### Postgres connections and custom users

Supabase documents direct Postgres, Supavisor session mode and transaction mode, with transaction mode intended for temporary/serverless/edge workloads. It also documents that Postgres users are LOGIN roles and recommends creating a distinct database user for each external service rather than sharing the default database password.

Sources:

- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/docs/guides/database/postgres/roles
- https://supabase.com/docs/guides/database/connection-management

### Data API / PostgREST role model

Supabase documents `authenticator` as the PostgREST role that validates JWT and then changes into a role determined by JWT verification. Its custom-role guidance grants custom roles to `authenticator`; the Data API preserves PostgreSQL roles, grants and RLS.

Sources:

- https://supabase.com/docs/guides/database/postgres/roles
- https://supabase.com/docs/guides/storage/schema/custom-roles
- https://supabase.com/docs/guides/api
- https://supabase.com/docs/guides/api/securing-your-api

### Hosted Edge ambient capabilities

Supabase currently documents that hosted Edge Functions have these project secrets by default:

- `SUPABASE_DB_URL`, which can connect directly to Postgres;
- `SUPABASE_SECRET_KEYS`, whose secret keys bypass RLS;
- legacy `SUPABASE_SERVICE_ROLE_KEY`, where still present, also bypasses RLS.

Source:

- https://supabase.com/docs/guides/functions/secrets

The current authenticated-user Edge pattern exposes:

- `ctx.supabase` scoped to the user/RLS;
- `ctx.supabaseAdmin` that bypasses RLS;
- verified user/JWT claims.

The service-to-service secret mode explicitly yields `ctx.supabaseAdmin` for privileged work.

Sources:

- https://supabase.com/docs/guides/functions/auth
- https://supabase.com/docs/guides/functions/connect-to-postgres
- https://supabase.com/docs/guides/functions/auth-headers

I found no current first-party function-configuration documentation exposing a per-function control that removes the platform-provisioned DB URL / secret-key capability set. The documented per-function controls cover auth verification, dependencies/import maps and entrypoint behavior. This is an evidence statement about current public docs, not proof no undocumented/support-only mechanism exists.

---

# 3. Transport A — dedicated Postgres LOGIN role from an isolated guarded publisher

## Shape

A separately controlled backend/publisher connects to Supabase Postgres using a dedicated LOGIN principal corresponding to `r9a0_edge_ingest`, via direct connection or Supavisor transaction/session mode appropriate to runtime lifetime/network.

Expected database posture remains V3:

- non-superuser;
- NOBYPASSRLS;
- no schema/relation/sequence ownership;
- no direct canonical table/sequence rights;
- exact `USAGE` only on `r9a0_edge_api`;
- exact wrapper `EXECUTE` only;
- no membership/USAGE/SET/ADMIN path into `r9a0_edge_api_owner`, `postgres`, `service_role` or broad internal writer roles;
- wrapper is the narrow SECURITY DEFINER boundary into canonical write semantics.

## Assurance

**Provider principal:** strong and directly inspectable. PostgreSQL session should read back exact `session_user/current_user = r9a0_edge_ingest` on the intended path.

**Vera governance authority:** not supplied by the DB login itself. H11/H13 must validate/consume authority capability separately.

**RLS:** direct runtime role is NOBYPASSRLS. But V3 does not rely on broad RLS table access anyway; it should reach only exact wrapper EXECUTE.

**Credential:** one dedicated password/DSN secret. Must be stored only in the guarded publisher environment, rotated/revoked independently, absent from chat/Git/CI logs/receipts.

## H12 fit

This is the strongest current candidate for `PROVIDER_PRINCIPAL_CONFINED` if:

- the ordinary Vera runtime cannot obtain this credential;
- the publisher runtime has no second postgres/service-role/admin credential;
- provider/network/config inspection proves the publisher credential's effective privilege closure;
- break-glass uses a distinct admin principal/runtime;
- runtime code cannot retrieve broader project secrets through some adjacent control plane.

## Limitations

- password/DSN lifecycle must be governed;
- Supavisor connection identity with the custom role must receive exact hosted readback;
- transaction pooling may require prepared statements disabled and may change session-state assumptions;
- this route does not authenticate Patrick/Voss; it authenticates a database service principal.

## MU7 disposition

`V3_COMPATIBLE_IN_PRINCIPLE / PREFERRED_CURRENT_HARD_BOUNDARY_DIRECTION`

provided the publisher is outside the managed Edge ambient-admin capability envelope.

---

# 4. Transport B — PostgREST / Data API custom-role JWT path

## Shape

The guarded service calls the Supabase Data API and presents a JWT whose role claim maps to a custom PostgreSQL role that `authenticator` may `SET ROLE` into. That custom role receives schema USAGE + exact wrapper EXECUTE, with no direct canonical relation rights.

Supabase's role model makes this structurally plausible:

- PostgREST connects as `authenticator`;
- JWT verification determines the role PostgREST assumes;
- custom roles can be granted to `authenticator`;
- grants + RLS govern object/row access.

## Important caveat: ordinary user JWT != automatically `r9a0_edge_ingest`

Supabase's normal Auth user tokens use the standard application roles such as `authenticated`. Current docs also support custom claims/RBAC, but a normal custom application claim such as `user_role` is not automatically the database `role` claim used for PostgREST role switching.

Therefore the implementation must **prove the exact token issuance/verification mechanism that safely yields the custom database role**. Do not write `role=r9a0_edge_ingest` in caller-controlled JSON or assume every standard user JWT can request it.

Possible future families include a separately trusted JWT issuer / provider-authenticated authority service whose signed role claim is accepted by the Data API, but that becomes H11/H13 authentication/issuer architecture and needs exact provider proof.

## Membership risk

Granting `r9a0_edge_ingest` to `authenticator` is a deliberate `SET ROLE` path. That is acceptable only if:

- `authenticator -> r9a0_edge_ingest` is the intended Data API transport;
- `r9a0_edge_ingest -> r9a0_edge_api_owner` is impossible;
- the custom execution role itself is narrow;
- no JWT role claim can choose a broader role from the same authority source;
- issuer/audience/signature/expiry/revocation semantics are exact.

This is why V3's owner membership test and H11's authority-issuer work are separate.

## RLS

The Data API respects grants/RLS for ordinary roles. The wrapper may be SECURITY DEFINER and execute the narrow privileged canonical operation internally.

The custom API role must not be BYPASSRLS and must not inherit `service_role`.

## H12 fit

Potentially `PROVIDER_PRINCIPAL_CONFINED` if an **isolated external guarded publisher** has only a narrowly scoped JWT/credential path and no broad Supabase secret/admin route.

Inside current managed Edge, the same request route does not solve ambient admin capabilities.

## MU7 disposition

`CONDITIONALLY_V3_COMPATIBLE / AUTH_ISSUER_AND_ROLE_SWITCH_PROOF_REQUIRED`.

It is more complex than a dedicated DB login and should not be chosen merely because HTTP looks friendlier than PostgreSQL.

---

# 5. Transport C — hosted Edge Function with authenticated user JWT

## Positive properties

Supabase's current `auth:'user'` flow can:

- require/verify a user JWT;
- provide `userClaims` / full JWT claims;
- provide an RLS-scoped `ctx.supabase` client.

That is useful H11/H13 evidence for **provider-authenticated human/user identity**.

## Blocking capability problem

The same first-party example hands the function `ctx.supabaseAdmin`, explicitly documented as bypassing RLS.

Hosted functions also receive secret-key dictionaries and `SUPABASE_DB_URL` by default.

Thus a compromised/mis-prompted/changed function can potentially choose a broader path than the intended user-scoped or narrow wrapper path.

Caller authentication does not constrain the function runtime's provider capability.

This is precisely H11 vs H12:

`AUTHENTICATED_CALLER != CONFINED_EXECUTION_RUNTIME`.

## MU7 disposition

`CALLER_IDENTITY_STRONGER / V3_H12_RUNTIME_CONFINEMENT_FAILS_CURRENT_DOCS`.

A user-JWT Edge endpoint may become an authority **front door** to a separately confined publisher, but should not itself be treated as the hard-confined write executor while admin capabilities remain available.

---

# 6. Transport D — hosted Edge Function with custom direct Postgres DSN

## Positive property

Supabase documents raw Postgres clients from Edge Functions. A custom DSN can therefore technically establish a dedicated LOGIN role such as `r9a0_edge_ingest`, including Supavisor transaction mode for short-lived/serverless workloads.

This proves V3's narrow transport is not intrinsically impossible.

## Blocking property

A custom narrow DSN does not erase the function's default environment:

- `SUPABASE_DB_URL` remains documented as a direct database capability;
- `SUPABASE_SECRET_KEYS` remain documented as RLS-bypassing API capabilities;
- `ctx.supabaseAdmin` is available under current server helper patterns.

Application code promising never to read those variables is not mechanical confinement.

## MU7 disposition

`DATABASE_PATH_COMPATIBLE / HOST_RUNTIME_NOT_H12_CONFINED`.

This is the exact managed-runtime blocker already identified in the earlier MU3 provider addendum.

---

# 7. Transport E — hosted Edge service-to-service secret mode

Supabase documents `auth:'secret'` as accepting a secret API key and yielding `ctx.supabaseAdmin` for privileged operations. Secret API keys bypass RLS.

Named secret keys improve identity/rotation/selection of the key, but do not turn the resulting admin client into the V3 narrow execution principal.

## MU7 disposition

`INCOMPATIBLE_WITH_V3_HARD_LEAST_PRIVILEGE_WRITE_PATH`.

It may be valid for other administrative workloads, but it cannot be the fallback for `r9a0_edge_ingest`.

---

# 8. Transport F — hosted Edge public/webhook mode

`auth:'none'` / `verify_jwt=false` can support externally signed webhooks where the handler verifies the sender's signature itself.

That may authenticate an external event source, but the function runtime still has the same broad project secret/admin capability problem.

## MU7 disposition

`CALLER_AUTH_CUSTOM / RUNTIME_CONFINEMENT_UNCHANGED`.

Useful for source authentication; irrelevant to the V3 least-privilege execution boundary unless it forwards into a separately confined publisher.

---

# 9. Transport G — self-hosted / externally controlled Deno or backend runtime

Supabase documents Edge Functions as portable Deno code and `@supabase/server` as usable on other runtimes when environment variables are supplied explicitly.

A self-hosted/external runtime can therefore, in principle, be configured with:

- only the narrow `r9a0_edge_ingest` DSN or exact narrow Data API token;
- no Supabase secret/service-role key;
- no default broad DB URL;
- explicit network egress policy;
- dedicated runtime identity;
- separately isolated break-glass administration.

This is the cleanest route to H12 provider-principal confinement if managed Edge cannot suppress ambient broad capabilities.

But it changes:

- infrastructure/hosting;
- operations/monitoring;
- deployment pipeline;
- cost/paid-service posture depending on host;
- credential custody.

## MU7 disposition

`TECHNICALLY_COMPATIBLE / ARCHITECTURE_AND_AUTHORITY_STAGE_REQUIRED`.

Do not smuggle a hosting migration into an Edge SQL implementation because the word "Deno" appears in both places. Human civilization has suffered enough from nouns pretending two deployment models are the same thing.

---

# 10. Transport comparison matrix

| Transport | Provider-auth caller | Effective DB principal | RLS bypass available in runtime | Exact wrapper path feasible | Ambient broad fallback risk | V3/H12 disposition |
|---|---|---|---|---|---|---|
| Isolated publisher + dedicated Postgres LOGIN | separate H11/H13 | exact custom LOGIN | can be **NO** if environment is narrow | yes | lowest if proven | **Preferred compatible direction** |
| Isolated publisher + Data API custom DB role | issuer-dependent | `authenticator -> custom role` | can be **NO** if no secret/admin path | yes | issuer/role-claim complexity | **Conditionally compatible** |
| Hosted Edge + user JWT | yes | user/Data API for intended path | **YES**, documented admin path | yes in principle | high | **Not hard-confined** |
| Hosted Edge + custom narrow DB DSN | separate | exact custom LOGIN intended | **YES**, default broad env documented | yes | high | **DB path okay, runtime blocked** |
| Hosted Edge + secret service auth | service key only | admin/Data API | **YES by design** | possible but pointless | inherent | **Incompatible as V3 executor** |
| Hosted Edge + custom webhook auth | external source only | runtime-dependent | **YES**, default broad env | possible | high | **Not hard-confined** |
| Self-hosted/external runtime + narrow credential | separate H11/H13 | exact narrow principal | can be **NO** | yes | controllable | **Technically compatible, new infra stage** |

---

# 11. Minimum implementation/deployment acceptance matrix

Any future implementation must bind one exact candidate/runtime and prove all relevant rows below.

## A. Provider/runtime identity

- runtime/provider principal identity;
- exact DB session `session_user/current_user` or PostgREST assumed role;
- LOGIN/NOBYPASSRLS/non-owner posture;
- no owner/admin role membership;
- no `USAGE`, `SET`, `ADMIN` chain into `r9a0_edge_api_owner`, `service_role`, `postgres`, canonical owner or other broad writer;
- if Data API, exact `authenticator -> r9a0_edge_ingest` membership/options and token role-binding mechanism.

## B. Database privilege closure

- exact `r9a0_edge_api` schema USAGE only;
- no schema CREATE;
- exact wrapper EXECUTE signatures only;
- PUBLIC execute closed;
- zero direct canonical table/view/sequence rights;
- no broad internal writer execute;
- no alternate callable function/procedure through another exposed schema;
- SECURITY DEFINER owner/search_path/current routine ACL/default privilege proofs from V3.

## C. Caller/authority separation

- provider-authenticated caller identity, if relevant;
- H13 current Vera authority mapping resolved separately;
- exact capability/assignment revision/effect scope consumed under H9/H11/H13 policy;
- no caller-supplied actor/role/source string grants authority;
- DB credential identity never treated as Patrick/Voss identity.

## D. Ambient capability inventory

Inside the exact deployed runtime, without logging values:

- environment variable **names/classes**;
- Supabase secret/admin key availability;
- default DB URL availability and effective principal;
- SDK-created admin client availability;
- provider management API/token availability;
- other connected credentials/secrets;
- network/egress routes;
- plugin/tool/control-plane routes able to substitute for the intended write path.

Any equal/broader path outside the guarded publisher fails H12 confinement.

## E. Credential custody

- one dedicated narrow runtime secret/capability only where possible;
- no credential in Git/Slack/receipt/test output;
- provider identifier/digest only in receipts;
- independent rotation/revocation procedure;
- expiry/TTL where supported;
- restart behavior;
- no automatic fallback to broad credentials when narrow path fails.

## F. Provider-path hostile tests

1. intended path reports exact narrow principal;
2. direct relation/sequence operations fail;
3. exact wrapper call succeeds;
4. unrelated routine call fails;
5. `SET ROLE` toward owner/admin fails;
6. malformed/changed operation identity fails;
7. narrow credential disabled -> hard failure, no broad fallback;
8. admin/Data API client path from the runtime is unavailable or provider-denied;
9. default DB URL absent or proven no broader than narrow principal;
10. temporary/public schema shadow attacks fail;
11. ambiguous write outcome uses read-only receipt lookup before retry;
12. plugin/connector/config/secret change invalidates confinement attestation.

## G. H12 status needed before protected activation

SQL ACL tests alone can earn only a database-component result.

Protected activation should require at least:

`PROVIDER_PRINCIPAL_CONFINED`

for the exact write executor, plus the guarded publisher/authority/effect-claim bindings. `MATRIX_RECORDED` or `EXPOSED_SURFACE_CONFINED` alone is not enough where the provider runtime itself still receives broader credentials.

---

# 12. Ranking

### 1. Isolated guarded publisher + dedicated Postgres LOGIN

**Best current engineering fit.** Fewest identity translations. Strong direct DB-principal readback. Exact wrapper-only surface is straightforward to test. Requires external/self-controlled runtime or a future managed Supabase capability-isolation feature.

### 2. Isolated guarded publisher + Data API custom-role JWT

Viable if HTTP/JWT transport is operationally preferred, but exact custom role issuance, authenticator membership and authority mapping add more moving pieces. Do not choose it to avoid one password while quietly inventing a JWT authority service.

### 3. Managed Supabase Edge with provider-supported per-function capability suppression

Would be attractive **if** Supabase documents/provides a verifiable control that removes or scopes the current default broad DB/API capabilities for the specific function. No such current public control was found in this audit. If one appears, re-audit rather than inherit this blocker forever.

### 4. Current managed Supabase Edge defaults

Not acceptable for V3 hard least privilege. The code can be narrow while the runtime is broad.

---

# 13. Interaction with H11/H13

Transport solves `which technical principal can invoke the wrapper`.

It does not solve `who authorized the transition`.

A strong future composition is:

1. H13 authenticates/enrolls human authority and resolves current Vera governance mapping;
2. H9/H11 issues exact capability for the proposed admission/effect;
3. ordinary runtime submits typed intent but has no protected provider credential;
4. isolated guarded publisher validates capability/current assignment/effect claim;
5. publisher uses `r9a0_edge_ingest` narrow provider credential;
6. V3 wrapper performs canonical DB operation;
7. exact readback/reconciliation produces bounded receipt;
8. H12 proves ordinary runtime has no equivalent/broader alternate mutator within the achieved confinement boundary.

The DB service principal is deliberately *not* Patrick, Voss or the user. That separation is a feature.

---

## Verdict

`DIRECT_NARROW_PRINCIPAL_FEASIBLE; MANAGED_EDGE_NOT_CURRENTLY_CAPABILITY_CONFINED`

V3 should **not** be revised merely because transport is deferred. The design correctly forbids broad fallbacks and current provider evidence triggers that stop condition.

A future implementation can use a dedicated Postgres LOGIN role or conditionally a Data API custom role. But if the executor runs inside the currently documented managed Supabase Edge environment, exact SQL least privilege does not prove runtime least privilege because broader project credentials/direct DB capability remain documented and available.

No role, password, grant, schema, JWT issuer, secret, Edge Function, project configuration, provider credential, deployment or repository producer target was modified during this audit.