# Mune MU7 — Edge Transport / Capability Audit Integrated Final V2

**Assignment:** `VOSS-20260808-MU7` / canonical root `3465`, amendment `3548`  
**Class:** `READ_ONLY_PROVIDER_AUDIT`  
**Disposition:** `FINAL_READY_FOR_REVIEW`  
**Exact live database engine evidence:** PostgreSQL `17.6`, `server_version_num=170006`  
**Mutation performed:** none

## Final verdict

`DIRECT_NARROW_PRINCIPAL_FEASIBLE; DATA_API_CONDITIONAL_AND_CURRENT_IMPLEMENTATION_NOT_PROVIDER_QUALIFIED; MANAGED_EDGE_NOT_CURRENTLY_CAPABILITY_CONFINED; ACTIVATION_REQUIRES_END_TO_END_RUNTIME_CONFINEMENT`

The transport problem has three separate questions that must not be collapsed:

1. **Provider authentication:** which database/session/runtime identity is actually authenticated by Supabase/PostgREST/Postgres?
2. **Vera governance authority:** is the requested protected action currently authorized under Vera policy?
3. **Capability confinement:** can the selected runtime/principal reach anything broader than the declared effect path?

A provider login, JWT, or narrow SQL role answers only part of that stack.

## 1. Preferred hard-boundary direction

The simplest currently defensible V3/H12 design remains an **isolated guarded publisher outside the default managed-Edge ambient capability envelope**, holding one dedicated narrow PostgreSQL LOGIN credential for `r9a0_edge_ingest` or its successor role.

Required database posture:

- LOGIN only where needed;
- NOSUPERUSER, NOCREATEDB, NOCREATEROLE, NOBYPASSRLS;
- no object ownership;
- no direct canonical table/sequence write rights;
- exact schema USAGE + exact wrapper EXECUTE only;
- no SET/INHERIT/ADMIN path to owner, postgres, service_role, or another broader writer;
- no second admin/service-role/database credential in the same publisher runtime;
- narrow wrapper remains the only protected write boundary.

This route is operationally dull, which is a compliment. It removes the PostgREST session-principal/role-selection boundary entirely because authenticated session identity and effective database principal can be the same narrow role.

It still does **not** authenticate Patrick/Voss or confer Vera governance authority. Authority is a separate pre-effect input.

## 2. Data API / PostgREST custom-role path remains conditional

The Data API route is structurally possible, but its confinement proof must cover both:

- provider transport/session principal (`authenticator` in current Supabase posture);
- effective request role selected after JWT mediation.

Fresh live readback confirms:

- `authenticator`: LOGIN, NOINHERIT, NOBYPASSRLS;
- `service_role`: NOLOGIN, BYPASSRLS;
- `authenticator -> service_role`: `SET=true`, `INHERIT=false`, `ADMIN=false`.

Therefore proving only `current_role = r9a0_edge_ingest` is insufficient. The attestation must also bind the role-selection mediation and prove ordinary request credentials cannot select or induce a broader role.

Current disposition:

`DATA_API_PROVIDER_PRINCIPAL_CONFINEMENT_NOT_PROVEN`

This is not a claim that ordinary HTTP callers can invoke arbitrary `SET ROLE service_role`; PostgREST mediation matters. It is a claim that the broader session-role graph is part of the trusted boundary and cannot be omitted from confinement evidence.

## 3. Current exact R9A0 authorization helper is not provider-qualified

Fresh live function readback on the R9A0 build-ground project shows:

```sql
if session_user = 'postgres' then return; end if;
if coalesce(current_setting('request.jwt.claim.role', true), '') <> 'service_role' then
  raise exception ...;
end if;
```

Two independently triaged defects now materially constrain MU7's Data API acceptance:

### HIGH `03854c12-eec8-4cf1-b876-84fddff6c827`

The helper reads only legacy `request.jwt.claim.role`.

Fresh live `auth.role()` instead deliberately supports both:

- legacy `request.jwt.claim.role`;
- PG14+ PostgREST JSON GUC `request.jwt.claims ->> 'role'`.

Therefore the exact helper is not yet provider-faithful for the current PostgREST/PG17 contract. A valid provider request may be rejected even when role impersonation itself is correct.

Actual hosted HTTP failure has not been proven because no service-role credential/HTTP probe was performed.

### MEDIUM `493ad51c-70a0-48a9-be3f-59280c60fca1`

Current SQL suites use postgres sessions and `SET LOCAL ROLE service_role`. That leaves:

- `session_user = postgres`;
- `current_user = service_role`;
- JWT role GUC absent.

The helper therefore returns through its postgres bypass before exercising the provider/JWT branch. Green tests do not establish PostgREST authorization parity.

Required provider-faithful test split:

1. postgres/admin maintenance path;
2. non-postgres `authenticator`/provider-equivalent positive service-role path;
3. missing/wrong/malformed JWT claim negatives;
4. explicit PG14+ `request.jwt.claims` parsing behavior;
5. provider role-switch/session identity readback.

## 4. SECURITY DEFINER caller-identity boundary

The exposed append path uses SECURITY DEFINER semantics. A nested authorization helper must not assume `current_user` identifies the original provider caller after definer transition.

The eventual provider-faithful shape must deliberately preserve/check caller identity before privilege escalation, for example by one of these reviewed patterns:

- an **invoker authorization gate** that validates the authenticated provider/JWT context, then calls a private SECURITY DEFINER core; or
- an equivalent design that binds original session/provider identity and verified claims without trusting post-definer `current_user` as caller identity.

Exact implementation remains producer scope. MU7's invariant is simply that authorization evidence must survive the definer boundary without being replaced by function-owner identity.

## 5. Hosted Supabase Edge remains capability-broader than V3

Current first-party provider behavior reviewed by MU7 exposes broad project capabilities to hosted Edge runtimes, including direct database connectivity and admin/secret-key patterns capable of bypassing RLS.

Therefore an intended narrow DSN, user JWT, or wrapper call inside the same managed function does not mechanically prove the runtime cannot choose a broader route.

Dispositions:

- hosted Edge + user JWT: stronger caller identity, **not hard-confined executor**;
- hosted Edge + narrow custom DB DSN: narrow intended DB path, **runtime still not hard-confined**;
- hosted Edge + service/secret mode: **incompatible as V3 least-privilege executor**;
- hosted Edge + webhook/custom auth: source authentication may improve, **runtime confinement unchanged**.

A future provider-supported per-function secret/capability suppression mechanism could change this conclusion, but it must be independently demonstrated against the exact deployed runtime. Application code promising not to read broader secrets is not confinement.

## 6. Target-major and provider-parity gate

The database-semantic target is PostgreSQL `17.6 / 170006`.

Existing historical R9A0 DB CI used PostgreSQL 15 and remains valid evidence for what actually ran there. It does not qualify:

- PG17 membership `SET/INHERIT/ADMIN` behavior;
- PG17 creator/owner transfer semantics;
- current provider role topology;
- current PostgREST JWT GUC behavior;
- hosted provider default privileges/extensions/authenticator mediation.

Final transport acceptance therefore requires both:

`TARGET_MAJOR_EXECUTION_PASS`

and

`HOSTED_PROVIDER_ATTESTATION_CURRENT`

for the exact candidate/transport. These are separate receipts; one may not launder the other.

## 7. Component confinement is not release activation

A future isolated publisher may establish:

`PROVIDER_PRINCIPAL_CONFINED`

for the publisher/provider-principal component.

That does not make protected effects globally eligible. H19/H14/H29 require the complete declared ordinary-runtime/publisher/control-plane path to satisfy the current end-to-end confinement policy.

A reachable equal-or-broader bypass elsewhere in the ordinary runtime still blocks activation.

Thus:

```text
NARROW_PUBLISHER_PROVIDER_PRINCIPAL_CONFINED
!=
PROTECTED_EFFECT_ACTIVATION_ELIGIBLE
```

Current H29 state remains a separate `FAIL_NOT_ELIGIBLE` witness for ordinary exposed protected-effect paths. MU7 does not override it.

## 8. Final transport ranking

| Rank | Transport | MU7 disposition |
|---|---|---|
| 1 | isolated guarded publisher + dedicated narrow PostgreSQL LOGIN | **preferred current hard-boundary direction** |
| 2 | isolated guarded publisher + Data API custom role | **conditional; issuer/session-role/claim/definer/provider-parity proof required** |
| 3 | managed Edge with future independently proven capability suppression | **potential future option** |
| 4 | current hosted Edge defaults for protected write executor | **not H12 hard-confined** |
| 5 | service-role/admin secret as executor fallback | **incompatible with V3 least-privilege goal** |

## 9. Minimum implementation/deployment acceptance matrix

A candidate cannot be called provider-principal confined unless all applicable items pass:

### Runtime and credential boundary

- exact runtime identity/environment declared;
- exactly intended narrow credential/token present;
- no ambient postgres/service-role/admin credential route;
- credential rotation/revocation and custody defined;
- no secret in chat/Git/CI logs/portable receipts;
- network/control-plane routes that can reconstruct broader access included in the trust graph.

### Database effective privileges

- exact session_user/current_user readback;
- no superuser/createdb/createrole/bypassrls;
- no direct canonical table/sequence mutation;
- exact wrapper EXECUTE and required schema USAGE only;
- no owner/admin SET/INHERIT/ADMIN reach;
- effective PUBLIC/default privileges checked, not merely explicit ACL rows.

### Data API-specific

- exact PostgREST session principal recorded;
- exact signed role-selection claim format/version recorded;
- PG14+ `request.jwt.claims` behavior tested;
- issuer/audience/key/revocation policy bound;
- ordinary credential cannot choose broader provider roles;
- non-postgres provider-equivalent positive/negative tests pass;
- definer transition preserves/verifies original caller evidence.

### Target/provider parity

- PostgreSQL 17 target-major tests pass;
- hosted provider roles/memberships/defaults/extensions read back;
- provider transport path itself exercised without postgres-session bypass;
- current transport/provider attestation bound to exact implementation head.

### Vera effect governance

- provider authentication remains distinct from Vera action authority;
- action authority/capability is current and exact-scope;
- H19/H29 end-to-end confinement/effect gates pass at execution time;
- outcome/retry handling is durable and fail-closed.

Any missing required row yields `NOT_PROVEN` / `BLOCKED`, not optimistic equivalence.

## 10. Final bounded recommendation

For the first production-capable R9A0 protected database publisher, prefer the architecture with the fewest privilege transitions:

`isolated publisher -> dedicated narrow PostgreSQL LOGIN -> exact SECURITY DEFINER wrapper`

Only move to a Data API custom-role transport if HTTP/JWT operational benefits justify the extra trusted boundaries and the exact provider-auth/session-role/claim/definer test matrix is satisfied.

Do not use current managed Edge ambient admin capability as a convenience fallback. That would preserve a narrow diagram while deleting the actual security property, a classic achievement in systems engineering.

## Final disposition

`FINAL_READY_FOR_REVIEW`

No credentials, roles, grants, provider configuration, Edge Function, schema, workflow, deployment, production database state, or producer branch were modified by MU7.
