# Mune Review Addendum — V3 Managed Edge Runtime Capability Audit

**Assignment lane:** `VOSS-20260808-MU3` provider/runtime feasibility challenge  
**Reviewed design target:** `thebrazenbeard/masamune@984cbdc781aa643443652f41f5a710f59e2d2439`  
**Target artifact:** `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`  
**Target blob:** `6fdee978d0b052592844d1f7356f6fedb13f43eb`  
**Prior Mune design verdict:** `APPROVED` in `reviews/edge-privilege-v3-review-984cbdc-v1.md`  
**This addendum:** implementation/provider-runtime admissibility only; it does **not** reopen V3's closed design corrections  
**Disposition:** `IMPLEMENTATION_BLOCKED_ON_MANAGED_EDGE_CAPABILITY_CONTAINMENT`

## Executive conclusion

A custom narrow PostgreSQL execution role is technically reachable from a Supabase Edge Function, so V3's deferred transport choice is not an intrinsic impossibility.

However, current official Supabase documentation exposes a more serious implementation boundary:

> Hosted Edge Functions receive broad project capabilities in their default environment, including a direct database connection URL and RLS-bypassing secret/service-role API credentials.

Therefore provisioning `r9a0_edge_ingest` with a narrow custom connection string is **not sufficient by itself** to prove runtime least privilege on managed Supabase Edge Functions. The function may still possess broader ambient capabilities that V3 explicitly forbids as Edge credentials/fallbacks.

Until the implementation proves those ambient capabilities are absent, unusable, or equivalently contained for the deployed function, the managed-Edge implementation is blocked.

This is an implementation/provider-hosting gate, not a V4 design defect in the exact V3 artifact.

---

## 1. Narrow custom-role transport is feasible in principle

Supabase's official Edge/Postgres documentation states that Edge Functions may connect directly to Postgres using ordinary PostgreSQL clients and database connection credentials.

For serverless/edge workloads, Supabase recommends pooled connection strategies and its examples show a database client initialized from a connection string. Custom PostgreSQL LOGIN roles are ordinary database roles; Supabase's migration/role documentation explicitly notes custom LOGIN roles have passwords and can be used as database users.

Therefore a future implementation can conceptually provision:

- `r9a0_edge_api_owner`: `NOLOGIN`, narrow owner/creator;
- `r9a0_edge_ingest`: dedicated `LOGIN` runtime principal, or an exact equivalent role reached by a separately reviewed transport;
- custom Edge secret containing only the narrow runtime DSN/credentials;
- direct PostgreSQL/Supavisor connection from the function;
- final runtime readback proving `session_user/current_user = r9a0_edge_ingest` on the intended path;
- zero relation/sequence privileges, exact schema USAGE and exact wrapper EXECUTE only.

This supports V3's decision to defer LOGIN/NOLOGIN to implementation rather than hard-code a transport in the design packet.

## 2. Managed Edge's documented default environment is broader than V3's runtime threat model

Official Supabase `Environment Variables` documentation currently says Edge Functions have access to these secrets **by default**:

- `SUPABASE_URL`;
- `SUPABASE_DB_URL` — documented as "The URL for your Postgres database. You can use this to connect directly to your database";
- `SUPABASE_PUBLISHABLE_KEYS`;
- `SUPABASE_SECRET_KEYS` — documented as secret API keys that bypass RLS;
- `SUPABASE_JWKS`;
- legacy `SUPABASE_ANON_KEY`;
- legacy `SUPABASE_SERVICE_ROLE_KEY` — documented as the `service_role` key and RLS-bypassing.

Primary source:

`https://supabase.com/docs/guides/functions/secrets`

Supabase's API-key migration documentation likewise states that the platform adds `SUPABASE_SECRET_KEYS` to Edge Functions' environment alongside the legacy service-role variables and that secret keys bypass RLS / have full backend data access.

Primary source:

`https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys`

This matters even if V3 application code never calls `Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')` intentionally. Least privilege is a capability property, not a code-style promise.

A compromised, dependency-confused, or accidentally changed function that can read a broad ambient credential has a wider effective authority surface than `r9a0_edge_ingest`.

## 3. Named secret keys improve rotation, not database least privilege

Supabase's current secret-key model allows multiple named `sb_secret_*` API keys, which is useful for rotation and blast-radius management between services.

But the official documentation describes secret keys as backend/admin keys that bypass RLS, and the Edge environment exposes the `SUPABASE_SECRET_KEYS` dictionary.

A separate named secret key therefore does not solve V3's database least-privilege requirement merely by being named `edge` or `coordination`.

The acceptance question is not:

`is this key independently revocable?`

It is:

`what effective database/API authority can code running in this function exercise if that key is present?`

Current documented answer remains broad enough to violate V3's intended execution boundary if used or exposed as fallback.

## 4. `SUPABASE_DB_URL` requires exact hosted-principal readback

The official docs establish that `SUPABASE_DB_URL` is built into Edge Functions and permits a direct PostgreSQL connection.

The documentation found during this audit does **not** sufficiently bind the exact managed-host principal/role embedded in that variable for the R9A0 target. Standard Supabase database connection examples commonly use the project `postgres` database user, but I will not promote that convention into a claim about the exact managed Edge variable without provider readback.

Therefore current classification is:

`DEFAULT_DIRECT_DB_CAPABILITY_PRESENT; EFFECTIVE_DB_PRINCIPAL = UNVERIFIED`

This is already enough to block a least-privilege acceptance because the implementation has not proven that the default direct connection is no broader than `r9a0_edge_ingest`.

Required hosted acceptance evidence must establish one of:

1. the built-in DB URL is absent/unavailable to the deployed function;
2. the URL's effective principal is itself the exact reviewed narrow role; or
3. the provider supplies another supported isolation mechanism that prevents the function from exercising broader DB authority through the built-in URL.

Do not assume absence from code usage equals absence of capability.

## 5. No documented per-function suppression of default broad variables was found

Supabase documents per-function configuration for items such as JWT verification, import maps, and entrypoints.

Primary source:

`https://supabase.com/docs/guides/functions/function-configuration`

The current official Edge-secret documentation describes default secrets as present in Edge Functions and custom production secrets as project-managed. The platform limit documentation reserves the `SUPABASE_` prefix for platform variables.

During this audit I found no documented per-function configuration that says:

- omit `SUPABASE_DB_URL` from this function;
- omit `SUPABASE_SECRET_KEYS` from this function;
- omit legacy `SUPABASE_SERVICE_ROLE_KEY` from this function;
- provide a per-function denylist of platform-injected default variables.

That is an evidence statement about current documentation, not proof that no private/provider-specific mechanism exists. If Supabase exposes such a control, it must be provider-read back and made part of the implementation receipt.

## 6. Legacy-key deactivation helps, but does not close the whole boundary

Supabase documents that legacy service-role keys can be deactivated after migration to the new key system.

That can remove one broad credential from the project/runtime once no consumer depends on it.

It does **not** by itself establish V3 runtime least privilege because:

- new `SUPABASE_SECRET_KEYS` are still documented as RLS-bypassing backend keys;
- the default direct `SUPABASE_DB_URL` capability remains to be bounded;
- disabling a project-wide credential can affect unrelated consumers and therefore requires exact dependency/authority review rather than being casually performed for this function.

No key deactivation is authorized by this review.

## 7. This is consistent with, not contrary to, V3

The exact V3 design already says:

- `service_role`, `postgres`, broad project secrets, or equivalent administrative credentials remain forbidden as Edge deployment credentials or fallbacks;
- provider-generated callable routes that bypass the intended narrow database role are implementation blockers;
- hosted apply is separately gated and requires provider/path proof.

So the correct result is not `CHANGES_REQUESTED_V4`.

The correct result is:

`V3 DESIGN APPROVAL PRESERVED / MANAGED-EDGE IMPLEMENTATION NOT YET ADMISSIBLE`

V3 wrote the stop condition. Current provider documentation appears to trigger it until stronger containment evidence exists.

## 8. Mandatory implementation gates

Before a managed Supabase Edge implementation can be accepted, exact-head tests/readback should prove all of the following **without logging secret values**:

### Runtime principal

- intended DB path establishes exact `session_user/current_user` identity;
- runtime role is the reviewed narrow execution role;
- runtime role has no membership/USAGE/SET/ADMIN path into `r9a0_edge_api_owner` or other broad owner/admin roles;
- migration-time owner-membership options are removed or exactly bounded in final posture.

For PostgreSQL 18 implementation targets, enumerate per-membership `inherit_option`, `set_option`, and `admin_option`; role-level `NOINHERIT` alone is not a no-escalation proof.

### Ambient credential containment

- function environment capability inventory is performed without emitting values;
- broad RLS-bypassing API secret/service-role credentials are absent or demonstrably unusable by this function;
- built-in direct DB URL is absent or its effective principal is proven within the same narrow capability boundary;
- there is no provider-injected admin fallback path hidden behind SDK defaults;
- failure of the narrow custom path fails closed rather than switching to a broad Supabase admin client.

### Database/API negatives

Using the actual deployed function runtime:

- direct canonical relation SELECT/INSERT/UPDATE/DELETE/TRUNCATE fail;
- sequence usage/nextval/setval fail;
- broad internal routine invocation fails;
- Data API/admin client path cannot reach canonical relations with broad credentials;
- only the exact reviewed Edge wrapper(s) are callable;
- valid wrapper call preserves canonical operation-id/replay semantics.

### Secrets/config provenance

- no secret values in Git, CI, logs, test fixtures, Slack, receipts, or review artifacts;
- receipt records only names/classes/digests/provider IDs needed for verification;
- provider secret configuration is bound to the exact deployment candidate and independently read back;
- any project-wide credential deactivation/rotation has separate exact authority and dependency proof.

## 9. Plausible acceptance routes

None is authorized by this review; these are design-space options for a future writer/deployment stage.

### Route A — provider-supported per-function capability isolation

If managed Supabase supports a documented/provider-verifiable way to suppress or scope default broad secrets/DB credentials per function, use it and bind that control to the exact deployment receipt.

This is the cleanest managed-Edge path if it exists.

### Route B — project-wide removal of broad API keys plus safe DB-default posture

Potentially deactivate broad API credentials after proving no other project consumer needs them, **and** separately prove the default DB URL does not confer broad authority.

This is only viable if both halves close and Patrick authorizes the exact credential/project changes.

### Route C — alternative hosting boundary

Run the Edge/API service in a separately controlled backend environment that receives only the dedicated narrow DSN and no provider-injected Supabase admin credentials.

This changes infrastructure/deployment/cost boundaries and requires separate architecture and user authority.

### Route D — self-hosted Edge runtime with controlled environment

Self-hosting can expose greater control over the function-service environment, but it materially changes operational responsibility/infrastructure and is not an implicit substitute for the hosted target.

Again, separate authorization required.

## 10. Hostile cases

1. code uses only narrow DSN, but malicious imported dependency reads `SUPABASE_SECRET_KEYS` -> must have no broad effect path;
2. narrow DB credential revoked/misconfigured -> function must fail, never fall back to `SUPABASE_DB_URL`/service-role/admin client;
3. legacy service-role deactivated but new secret key remains -> broad API path still denied;
4. all API secret keys absent but built-in DB URL connects as broad principal -> fail;
5. built-in DB URL exists but connects as exact narrow role -> acceptable only with provider-bound readback and no broader API secret path;
6. custom role has NOINHERIT but a membership grants SET into owner -> fail;
7. migration runner temporarily receives SET into owner and final membership persists -> fail;
8. provider SDK silently chooses an admin client despite narrow intended route -> fail;
9. environment-capability test logs a secret while proving absence/presence -> test itself fails privacy/security review;
10. provider documentation changes after repository review -> hosted implementation requires fresh provider-path verification.

## Verdict

`IMPLEMENTATION_BLOCKED_ON_MANAGED_EDGE_CAPABILITY_CONTAINMENT`

The narrow custom PostgreSQL execution-role transport is feasible in principle, and the exact V3 design remains approved. But current documented managed Supabase Edge defaults expose broader ambient project capabilities than the intended runtime role.

Do not accept a deployed V3 implementation merely because SQL ACL tests show `r9a0_edge_ingest` is narrow. Acceptance must prove **the function runtime itself has no broader usable credential/path**.

No hosted function, role, credential, API key, database, project configuration, producer target, native Project file, deployment, merge, paid service, or production state was modified by this audit.