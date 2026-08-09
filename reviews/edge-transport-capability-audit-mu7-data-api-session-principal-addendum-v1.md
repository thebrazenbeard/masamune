# Mune MU7 Addendum — Data API Effective Role Is Not the Whole Transport Principal

**Parent assignment:** `VOSS-20260808-MU7` / root sequence `3465`  
**Parent review:** `reviews/edge-transport-capability-audit-mu7-v1.md` @ `d2d5af0228a7567f7de38834c6e68069f938b6f1`  
**Class:** read-only transport-role precision  
**Provider mutation:** none

## Challenge

MU7 correctly classifies a Data API custom database role as conditional on exact issuer and role-switch proof. A later H27 role-topology refinement makes one additional acceptance condition explicit:

> proving only the effective custom role is narrow is insufficient when the provider transport session principal has broader SET reachability.

The Data API/PostgREST route has at least two relevant database identities:

- the provider transport/session principal (`authenticator` in the current Supabase posture);
- the effective request role selected after verified token/role processing.

Confinement must bind both plus the mechanism that controls the transition between them.

## Fresh live build-ground readback

Current R9A0 build-ground `agvhmutlrolbaijzlbqk` reports:

```text
authenticator: LOGIN=true, NOINHERIT, BYPASSRLS=false, CREATEROLE=false
authenticator -> anon:          SET=true, INHERIT=false, ADMIN=false
authenticator -> authenticated: SET=true, INHERIT=false, ADMIN=false
authenticator -> service_role:  SET=true, INHERIT=false, ADMIN=false
service_role: LOGIN=false, BYPASSRLS=true
```

Additional upstream control-plane reachability exists:

```text
supabase_storage_admin: LOGIN=true, CREATEROLE=true
supabase_storage_admin -> authenticator: SET=true
postgres: CREATEROLE=true, BYPASSRLS=true
postgres -> authenticator/service_role: ADMIN=true, INHERIT=true, SET=true
```

This directly matches canonical H27 sequence 3614: the protected-reach graph must seed from configured PostgREST login/effective roles and expand through SET/INHERIT/ADMIN/reconstructible control edges.

## Consequence for MU7 Transport B

The original conditional Data API direction remains technically plausible, but a future claim such as:

`PROVIDER_PRINCIPAL_CONFINED`

cannot be established merely by showing:

```text
effective current_role = r9a0_edge_ingest
r9a0_edge_ingest is narrow
```

The attestation must also prove, for the exact deployed Data API route:

1. the transport/session principal and its current role-membership graph;
2. the exact signed token claim that selects the custom effective role;
3. the trusted issuer/audience/key/revocation policy that controls which database roles can be selected;
4. that the ordinary publisher credential/request cannot select or induce `service_role`, `postgres`, owner, or another broader effective role;
5. that no exposed RPC/function path available to the narrow effective role can turn the session principal's broader SET reach into an alternate protected effect;
6. H27-relevant upstream principals/control-plane edges are included in the confinement evidence and staleness digest.

A custom role grant to `authenticator` is therefore **transport plumbing, not confinement proof**.

## Current status

Current live topology contains a real `authenticator -> service_role SET=true` edge. That fact alone does not prove a normal narrowly issued Data API request can exercise the edge, because PostgREST/token verification is a mediation layer and the ordinary client does not receive generic SQL merely by making an HTTP request.

But it does mean the stronger claim is currently:

`DATA_API_PROVIDER_PRINCIPAL_CONFINEMENT_NOT_PROVEN`

until the exact role-selection/issuer mediation and protected-reach graph are attested together.

This is deliberately narrower than calling the Data API route categorically incompatible. The route may still qualify if the mediation itself is part of the trusted confined boundary and no ordinary request credential can choose a broader role.

## Revised transport-B disposition

`CONDITIONALLY_V3_COMPATIBLE / EFFECTIVE_ROLE_NARROWNESS_PLUS_SESSION_PRINCIPAL_ROLE_SELECTION_CONFINEMENT_REQUIRED`

The dedicated direct PostgreSQL LOGIN remains simpler because the runtime's authenticated database session identity and effective database principal can be made the same narrow role, reducing one entire identity/role-switch boundary.

No role, membership, JWT issuer, grant, credential, schema, provider configuration, or deployment was modified.