# Mune DB Service-Role Helper Falsifier

**Disposition:** `REMOVE_HELPER_SECURITY_PASS`

## Question

Does `r9a0_governance.require_service_role()` enforce an independent security property beyond the managed-provider JWT/role-impersonation boundary plus exact database `EXECUTE` ACLs on `r9a0_api.append_coordination_event(...)`?

## Exact historical source inspected

Repository `thebrazenbeard/vera-R9A0`, historical head `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`.

Foundation migration `supabase/migrations/20260806133000_r9a0_coordination_foundation.sql` defines `require_service_role()` as a `SECURITY INVOKER` helper that:

1. immediately returns when `session_user = 'postgres'`; otherwise
2. requires `current_setting('request.jwt.claim.role', true) = 'service_role'`.

The append RPC is `SECURITY DEFINER` and calls that helper internally.

## Fresh hosted-provider observations

Read-only Lantern observations on 2026-08-10:

- `service_role`: `NOLOGIN`, `BYPASSRLS`;
- `authenticator`: `LOGIN`, not BYPASSRLS;
- `postgres`: `LOGIN`, `CREATEROLE`, `BYPASSRLS`;
- `authenticator -> service_role`: `SET=true`, `INHERIT=false`, `ADMIN=false`;
- `postgres -> service_role`: `SET=true`, `INHERIT=true`, `ADMIN=true`;
- append RPC ACL: `{postgres=X/postgres,service_role=X/postgres}`;
- `service_role` has EXECUTE; `authenticated` and `anon` do not.

## Safe falsifier

Inside a transaction that was rolled back, a SQL session successfully set the custom GUC `request.jwt.claim.role=service_role` and read it back.

A second rolled-back probe used `SET LOCAL ROLE service_role`, set the same GUC, then called the append RPC with intentionally invalid operation ID `x`. The call failed with `22023 Invalid operation_id`, not the helper's authorization error `42501`.

This demonstrates that a database actor able to assume `service_role` can satisfy the helper's GUC test and reach later RPC validation without proving that the request arrived through an authentic PostgREST JWT path. No coordination row was inserted and the transaction was rolled back.

## Conclusion

No independent authorization property survived the falsifier.

`request.jwt.claim*` is request context visible inside PostgreSQL, not an independent cryptographic trust root. The foundation helper also explicitly exempts the `postgres` session user. Keeping the helper therefore adds provider-specific, spoofable policy without excluding a caller that the exact `EXECUTE` ACL would otherwise admit.

Do **not** replace the helper with a `current_user` test inside the `SECURITY DEFINER` RPC because `current_user` becomes the definer during execution.

## Smallest successor design

Remove `require_service_role()` from the append authorization path and rely on the provider's JWT validation/role impersonation plus exact schema exposure and database ACLs. Provider qualification must independently prove:

- authentic service-role RPC reaches business validation and succeeds for a valid request;
- anon JWT is denied;
- authenticated JWT is denied;
- missing/invalid JWT is denied by the provider boundary;
- direct anon/authenticated database roles lack RPC EXECUTE;
- PUBLIC lacks RPC EXECUTE;
- exposed schema/routine surface is exactly the intended one.

This is a repair direction for the existing `03854c12...` / `R9A0-PG17-POSTGREST-JWT-CLAIM-GUC-001` and `493ad51c...` / postgres-session-test bypass family. It does not justify a new bug or path.

## Effect boundary

No R9A0 repository bytes, provider schema, grants, production data, credentials, deployment, merge, or installation were changed by this review. All provider SQL probes were read-only catalog queries or explicitly rolled-back transactions.
