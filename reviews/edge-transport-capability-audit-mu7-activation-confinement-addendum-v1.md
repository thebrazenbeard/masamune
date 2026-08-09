# Mune MU7 Addendum — Transport Confinement Is Not Activation Confinement

**Parent assignment:** `VOSS-20260808-MU7` / root sequence `3465`  
**Parent review:** `reviews/edge-transport-capability-audit-mu7-v1.md` @ `d2d5af0228a7567f7de38834c6e68069f938b6f1`  
**PG17 addendum:** `bf5044da072abd8d426c7c2750f6877b121b4ea7`  
**Class:** read-only policy/confinement precision addendum  
**Provider mutation:** none

## Why this addendum exists

MU7 correctly ranks an isolated guarded publisher with a dedicated narrow PostgreSQL LOGIN as the strongest current transport direction. Its original acceptance section says protected activation should require at least `PROVIDER_PRINCIPAL_CONFINED` for the exact write executor plus guarded publisher/authority/effect bindings.

Later authority-admitted architecture is stricter and should control the final MU7 handoff.

- H14 closure 3475 keeps the confinement ladder:
  `MATRIX_RECORDED -> EXPOSED_SURFACE_CONFINED -> PROVIDER_PRINCIPAL_CONFINED -> END_TO_END_DECLARED_RUNTIME_CONFINED`.
- H19 closure 3502 makes effect enable itself a protected effect and states that current broad admin/postgres engineering routes plus failed H14 confinement block production enable.
- H29 current-runtime evidence 3612/3613 now provides a fresh negative witness: ordinary exposed GitHub/Supabase routes include broad mutator classes, and the Supabase connector reaches the protected Vera project as `postgres`. The bounded current verdict is `FAIL_NOT_ELIGIBLE` for exposed-surface confinement. One current reachable bypass witness is enough for FAIL; a future PASS requires complete current inventory.

Therefore local executor confinement and release activation confinement must not be collapsed.

## Corrected assurance ladder

### Component claim

A future isolated publisher using a dedicated narrow `r9a0_edge_ingest` LOGIN may, after exact hosted readback and hostile tests, establish:

`PROVIDER_PRINCIPAL_CONFINED`

for that **publisher/provider-principal component**.

That is useful and necessary evidence. It proves the selected provider credential cannot directly escape its intended database capability envelope.

It does **not** prove that the overall Vera runtime can safely enable protected effects.

### Activation claim

Protected effect activation must satisfy the currently accepted H19/H14 release gate for the whole declared runtime path. In practical terms, the activation receipt must bind a current end-to-end confinement result at the policy-required level, including:

- ordinary model/runtime exposed tool routes;
- the guarded publisher;
- publisher credential/principal epoch;
- control-plane and deployment mutators;
- alternate raw GitHub/Supabase/admin paths that can reach the same protected target;
- provider target/resource scope;
- break-glass separation;
- current H13 authority and H18 evidence state;
- exact release/install identity and activation epoch.

A narrow publisher cannot compensate for a broader ordinary runtime that can bypass it.

This yields the key implication:

```text
NARROW_PUBLISHER_PROVIDER_PRINCIPAL_CONFINED
    !=
PROTECTED_EFFECT_ACTIVATION_ELIGIBLE
```

and, under the current H29 snapshot:

```text
CURRENT_GENERIC_BYPASS_WITNESS
    => EXPOSED_SURFACE_CONFINEMENT_FAIL
    => PROTECTED_EFFECT_ACTIVATION_BLOCKED
```

## Current disposition

The original transport ranking remains unchanged:

1. isolated guarded publisher + dedicated PostgreSQL LOGIN;
2. isolated guarded publisher + narrowly issued Data API custom-role path, conditional on issuer/role-switch proof;
3. managed Edge only if a future provider-supported capability-suppression mechanism is independently demonstrated;
4. current managed Edge defaults remain unsuitable for the hard least-privilege executor.

But none of those transport choices can presently authorize production activation by themselves because H29 currently proves an ordinary-runtime bypass surface outside the proposed narrow publisher.

## Revised MU7 acceptance wording

Replace the original shorthand:

> protected activation should require at least `PROVIDER_PRINCIPAL_CONFINED` for the exact write executor

with:

> `PROVIDER_PRINCIPAL_CONFINED` is the minimum component assurance for the exact write executor. Protected activation additionally requires the current H19/H14 end-to-end declared-runtime confinement gate, or any later explicitly authority-admitted stronger/successor policy, over the complete ordinary runtime/publisher/control-plane path. A current equal-or-broader bypass witness blocks activation regardless of how narrow the intended publisher principal is.

This is a policy-level supersession/precision correction, not evidence that the original transport comparison was technically wrong when written.

## Verdict

`DIRECT_NARROW_PRINCIPAL_FEASIBLE; MANAGED_EDGE_NOT_CURRENTLY_CAPABILITY_CONFINED; ACTIVATION_REQUIRES_END_TO_END_RUNTIME_CONFINEMENT`

No role, grant, credential, provider setting, Edge Function, schema, activation state, repository producer branch, or deployment was modified.