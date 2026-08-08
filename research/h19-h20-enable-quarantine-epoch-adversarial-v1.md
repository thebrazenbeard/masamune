# Mune Adversarial Pass — H19 Effect Enable + H20 Quarantine/Recovery Epochs

**Class:** `WORKING_PROJECT` / independent read-only architecture critique  
**Related canonical lanes:** H19 root 3498, H20 root 3499  
**Assignment ownership:** Hephaestus/Voss; this is advisory research only, not a self-assigned governed lane  
**Mutation performed:** none

## Executive conclusion

The most dangerous implementation mistake would be to treat "effects enabled" as a durable standing permission.

It is not.

Effect enable should mean only:

> **the installed runtime topology is currently eligible to accept future independently authorized effect requests.**

Every actual effect still requires its own current H13/H4/E2/H6/action-capability/provider-target gate.

The cleanest composition uses **monotonic enable/quarantine epochs**:

- an enable cut creates a new `effect_enable_epoch` after exact current evidence is checked;
- every future H6 effect claim binds that exact epoch;
- quarantine/disable advances a separate generation or terminates the current enable epoch;
- no pre-quarantine uncut claim/capability can be used after the epoch closes;
- already-authorized/in-flight effects retain their historical cut evidence and move into reconciliation/quarantine handling, not retroactive deletion;
- re-enable always creates a brand-new epoch and cannot reuse the old enable receipt/capabilities.

This separates **environment eligibility** from **per-effect authority** and makes later disable/re-enable mechanically intelligible.

---

# H19 — future effect-enable cutover

## 1. Avoid the H14 self-staleness trap

H19 depends on a positive H14 attestation of the actual production publisher/provider topology.

Naively enabling effects can itself change the reachable capability graph and instantly stale the attestation that authorized enable.

Example failure:

1. H14 attests runtime while publisher dispatch action is disabled/unreachable.
2. H19 enables the publisher action.
3. Reachable tool/capability surface changed.
4. H14 evidence is now stale exactly when H19 claims effects are safe.

The design needs one of two explicit solutions.

### Preferred: attest the **armed topology**, gate only request acceptance

Provision the exact production publisher code, narrow provider principals, routes, secrets and network topology in a mechanically effect-disabled state where the **capabilities themselves are visible/inspectable to H14**, but ordinary effect acceptance is blocked by a protected publisher enable-state control.

H14 attests:

- publisher binary/config;
- exact credentials/principal scopes;
- tool/route inventory;
- alternate mutator absence;
- break-glass isolation;
- the exact enable-state mechanism and allowed transition;
- both the current disabled state and the capability graph that would exist after the internal guard accepts work.

Then H19's final enable changes only the protected acceptance state, not credentials, routes, plugin actions, provider permissions, network egress or publisher code.

If enable changes any of those, H14 must be rerun before effect acceptance.

### Fallback: `ENABLE_PENDING` plus post-change attestation

If provider topology cannot be inspected until a route is technically enabled:

```text
DISABLED
  -> ENABLE_PENDING   (provider route activated, ordinary effect acceptance still blocked)
  -> H14 re-attests actual now-active topology
  -> ENABLED          (publisher begins accepting independently authorized effects)
```

No ordinary effect dispatch is permitted during `ENABLE_PENDING`.

This avoids the absurd but very achievable state "we enabled it so we could prove enabling it was safe, and something used it before the proof finished."

## 2. Enable authorization is not an effect capability

A one-time H19 authorization should bind:

- exact environment/project/deployment identity;
- exact installed candidate/config/settings identity;
- exact H13 current authority mapping revision;
- exact authority source/assurance;
- exact H14 attestation receipt/digest/valid-until;
- exact PG17/provider-parity evidence;
- exact publisher binary/config/principal identifiers;
- exact effect-claim/policy versions;
- exact disabled/current enable-state generation;
- no active quarantine/break-glass unresolved condition;
- no newer material staleness event;
- intended transition `DISABLED|ENABLE_PENDING -> ENABLED` only.

It **must not** authorize any concrete provider mutation beyond the enable-state transition itself.

After enable, each actual effect independently requires a fresh effect capability/H6 cut.

Therefore compromise/replay of an old enable receipt must not grant a repository/database/provider action.

## 3. Enable state should be versioned/epoch-bound

Conceptual state:

```text
EffectRuntimeState
  environment_id
  enable_epoch bigint
  state DISABLED | ENABLE_PENDING | ENABLED | QUARANTINED
  activation_request_id
  authority_mapping_revision
  install_identity_digest
  h14_attestation_digest
  h14_valid_until
  policy_version
  enabled_at
  disabled_at nullable
  supersedes_state_id
```

The exact storage mechanism belongs to future implementation design; the invariant matters now.

Each H6 claim binds:

```text
(environment_id, enable_epoch, publisher_revision, authority_mapping_revision, target_conflict_digest, request_digest)
```

Before the H6 authority cut, transaction rechecks:

- current runtime state is `ENABLED`;
- enable epoch matches;
- H14 attestation is still current/policy-sufficient;
- no quarantine generation superseded it.

This makes a stale effect claim mechanically fail after disable/re-enable.

## 4. Crash semantics at cutover

### Crash before durable enable transition

Runtime remains DISABLED. Retry may re-resolve all evidence and reuse the same idempotent activation request only if the request digest/current state is identical and no evidence changed.

### Crash after durable `ENABLED` commit but before response/readback

Do not issue another enable transition blindly.

Read current effect-runtime state by activation request ID / exact epoch. If the exact enabled state exists, return its receipt. If state differs, fail/re-resolve.

### Partial provider/config enable

If activation requires more than one provider/control-plane change, do not pretend it is atomic. Use `ENABLE_PENDING`, record each provider-side step/readback, keep ordinary effect acceptance blocked, and either complete to a fully attested state or enter QUARANTINED/RECOVERY_REQUIRED.

The cleanest H19 architecture minimizes cutover changes so final `ENABLED` is one protected application-state transition after all provider topology already exists.

## 5. Exact Patrick/current-authority requirement

H19 should not allow:

- an old chat statement;
- a CI approval;
- an install commit;
- admin account possession;
- provider credential ownership;
- a previous enable receipt;
- Voss procedural role string;

to self-enable effects.

The enable request needs current authority under the H13 mapping/assurance policy appropriate to this high-risk transition.

If the future policy requires exact user-presence confirmation, bind it to the activation request digest and environment/epoch. If current assurance remains only PROCEDURAL, the receipt must say so and the release policy decides whether that is sufficient; a field cannot promote itself by enthusiasm.

## 6. Dual control is a policy option, not a hidden prerequisite

H19 can support a future policy requiring two independent approvals, but do not invent dual control as current Vera truth.

If enabled later, model it as a closed authorization policy such as:

```text
required_approvals = [CREATOR, SECURITY_REVIEWER]
approval_independence = DISTINCT_AUTHORITY_PRINCIPALS
```

Each approval binds the same exact activation digest/epoch and has independent expiry/revocation.

Do not implement "two approvals" as two copies of the same reusable account/session.

## 7. Immediate post-enable readback

Final cutover receipt should prove:

- durable enable state/epoch;
- exact current H14 attestation remains valid for enabled topology;
- publisher reports expected revision/config;
- provider principal/scopes unchanged from attestation;
- no ordinary raw alternate mutator became reachable;
- break-glass remains isolated;
- no effect was dispatched as part of the enable ceremony itself.

If any readback conflicts, immediately classify `QUARANTINED`/`RECOVERY_REQUIRED`; do not leave the system effect-eligible while investigating.

---

# H20 — quarantine and recovery

## 8. Disable should be easier than enable, but not a hidden destructive capability

Security architecture usually benefits from an emergency **one-way fail-closed quarantine primitive** whose authority threshold is no higher than enable and whose action only reduces future capability.

Potential future delegated triggers:

- H14 attestation expired/failed;
- authority issuer/mapping compromise epoch;
- provider principal compromise;
- plugin/tool/permission broadening;
- break-glass use;
- evidence custody loss where current qualification becomes unavailable;
- publisher health/integrity failure;
- unreconciled effect ambiguity beyond policy tolerance.

The architecture may allow trusted monitoring/control to enter QUARANTINED automatically if separately authorized by policy, but **re-enable always requires a new H19 cutover**.

This advisory does not authorize any current automatic production config change.

## 9. Quarantine semantics

On durable quarantine transition:

1. increment/terminate the active enable epoch;
2. refuse creation of new H6 effect claims;
3. refuse pre-cut claims/capabilities bound to the old epoch;
4. stop ordinary publisher dispatch as soon as mechanically possible;
5. inventory already-cut/in-flight provider operations;
6. attempt cancellation only where provider supplies trustworthy semantics and policy permits;
7. reconcile every ambiguous/in-flight effect independently;
8. preserve all authority/effect/provider evidence;
9. classify current release `BLOCKED_*` / recovery status according to trigger;
10. require new evidence + new H19 epoch for any future re-enable.

Do not delete or rewrite earlier enable/effect receipts.

## 10. Historical evidence vs future authority

A later revoke/compromise/quarantine has different consequences depending on temporal position.

### Effect not yet at H6 durable authority cut

New invalidation applies. Claim/capability cannot cross the cut.

### Effect already at valid H6 authority cut, dispatch not yet attempted

Architecture should define whether quarantine cancels queued dispatch before provider call. Safest default: **do not dispatch a not-yet-sent request after quarantine**, record `ABORTED_BEFORE_PROVIDER_DISPATCH`, unless a policy explicitly says post-cut dispatch is irrevocable. H6's authority cut proves it *was authorized*, not that Vera must execute it despite an emergency disable before any provider effect occurred.

This is one place to challenge the earlier shorthand "revocation after cut cannot cancel." It is true that Vera cannot promise cancellation **after provider dispatch/in-flight**. Before the network call, Vera can and should usually stop.

Historical receipt remains valid evidence that the request had authorization; outcome becomes verified non-execution/aborted.

### Provider dispatch already accepted/in-flight

Quarantine cannot rewrite history or promise cancellation. Attempt provider-native cancellation only if trustworthy. Otherwise reconcile to `VERIFIED_COMMITTED`, `VERIFIED_NON_EXECUTION`, or `OUTCOME_UNKNOWN`.

New requests stay blocked.

This temporal split is more precise than making the H6 cut magically turn a queued request into an unstoppable object.

## 11. Quarantine reason taxonomy should determine recovery class

Recommended classes:

### `BLOCKED_STALE`

Evidence/policy expired or target moved, but no integrity/compromise evidence.

Orientation may remain `DEGRADED_BOUNDED` for read-only work if authoritative state is still coherent.

### `BLOCKED_UNAVAILABLE`

Required evidence/authority service temporarily unavailable; no contradiction.

Read-only operation may continue where safe; protected effects fail closed.

### `BLOCKED_CONFLICTED`

Contradictory authority/evidence/target state; do not select a winner by timestamp.

### `RECOVERY_REQUIRED`

Use when there is an actual integrity/security condition that invalidates normal resumption, for example:

- issuer/principal compromise affecting trust root;
- protected registry integrity mismatch;
- unexplained privileged provider effect;
- break-glass changed state without completed reconciliation;
- capability/tool-surface evidence contradicts expected topology;
- provider target cannot be reconciled after ambiguous privileged operation;
- required authority history/custody lost such that trust cannot be reconstructed normally.

Do not use `RECOVERY_REQUIRED` merely because an attestation TTL expired. That is stale/blocking evidence, not an integrity disaster.

This matches Vera's orientation discipline: `RECOVERY_REQUIRED` should mean real recovery, not bureaucracy wearing a siren.

## 12. Compromise epochs

For authority issuer/provider credential/publisher compromise, bind an explicit compromise/revocation epoch.

Conceptually:

```text
principal_id
credential_or_issuer_epoch
status ACTIVE | REVOKED | COMPROMISED | RETIRED
known_bad_from nullable
uncertainty_start nullable
```

Consequences:

- unconsumed capabilities from a compromised epoch invalid;
- new issuance requires new epoch/principal;
- historical effects before a confidently bounded compromise time may retain prior assurance;
- effects inside uncertain compromise interval become `ASSURANCE_COMPROMISED_REVIEW_REQUIRED` rather than automatically valid or automatically deleted;
- re-enable requires fresh H13/H14/H19 evidence tied to new epochs.

Never make changing a key erase the evidence that the old key existed.

## 13. Permission/tool-surface broadening

If H14-observed app/plugin/tool/provider scope broadens:

- current H14 becomes RERUN_REQUIRED/stale;
- immediately block new protected effects under policy;
- if ordinary raw alternate mutator is now reachable, quarantine is stronger than mere stale status because the mechanical effect gate may be bypassable;
- inspect provider audit/effect history for out-of-band mutations within the uncertain interval;
- do not assume absence of known bad effects equals confinement restored.

Restoration requires removing/isolating the bypass under exact authority, re-attesting, reconciling target state and then a new H19 enable epoch.

## 14. Break-glass use

Break-glass is intentionally out of the normal publisher path, so its use must:

- immediately close the current enable epoch or at minimum mark it ineligible;
- classify affected targets/currentness/evidence for reconciliation;
- preserve provider-native audit plus Vera out-of-band receipt;
- require H14 rerun because the actual provider state may have changed through an alternate authority plane;
- require fresh currentness/target reconciliation;
- never allow the old enable receipt to reactivate normal effects automatically after the admin session ends.

Break-glass being "authorized" does not make prior H14 topology magically current.

## 15. Evidence disappearance and restoration

If a required qualification/authority/confinement receipt disappears:

- current effect eligibility becomes blocked/unavailable;
- historical effect receipts remain historical where their own evidence is intact;
- quarantine new effects if the missing evidence is necessary to prove current mechanical safety.

If the **exact same immutable ref+digest** returns and custody/readback can be revalidated, the evidence may move through `REVALIDATE_REQUIRED -> VALID` without rerunning unrelated tests.

Digest mismatch is conflict/recovery territory, not "close enough, probably the same PDF."

## 16. Target divergence

If provider target head/version/state changes outside the expected controlled path:

- invalidate outstanding precondition-bound claims;
- block new dispatch until currentness/target reconciliation;
- distinguish ordinary expected concurrent movement from unexplained privileged movement;
- unexplained movement by an authority-equivalent principal may trigger RECOVERY_REQUIRED and provider audit, while ordinary expected head movement may be a bounded stale/precondition failure.

The classification should depend on provenance, not merely the fact of change.

## 17. Re-enable contract

Never `UNQUARANTINE` by flipping the old state back to enabled.

Future recovery path:

1. preserve old epoch/history;
2. resolve/quarantine all in-flight/ambiguous operations;
3. remediate the trigger under separately authorized procedures;
4. establish new authority/principal/publisher/config evidence as applicable;
5. rerun/revalidate H14 and other stale axes;
6. verify PG/provider parity where relevant;
7. create **new H19 activation request** with new exact evidence graph;
8. commit new `effect_enable_epoch = N+1`;
9. future H6 claims bind only N+1.

Old capabilities/claims never float across epochs.

---

# Combined hostile cases

1. old enable receipt replayed after disable -> fails current epoch/predecessor check;
2. enable approved for candidate A, installed candidate moves to B before cut -> fail;
3. H14 valid at approval but expires before cut -> fail/re-resolve;
4. H14 tool permission broadens after approval before cut -> fail;
5. publisher credential scope changes before enable -> fail and re-attest;
6. crash after enable commit before response -> read existing activation result, no duplicate epoch;
7. multi-step provider enable partially succeeds -> ENABLE_PENDING/QUARANTINED, no ordinary effects;
8. enabled runtime receives actual effect without individual H6 capability -> deny; enable is not standing effect authority;
9. authority revoked before H6 cut -> deny;
10. quarantine after H6 cut but before provider dispatch -> default abort before provider call, preserve prior authorization evidence;
11. quarantine after provider accepted request -> reconcile/cancel if supported, no promise of non-execution;
12. provider timeout during quarantine -> OUTCOME_UNKNOWN, no blind redispatch;
13. principal compromise time uncertain -> affected interval review-required;
14. H14 bypass path appears -> new effects blocked, old success does not prove no bypass;
15. break-glass changes target -> close/invalidate normal epoch and re-attest/reconcile;
16. missing qualification evidence later restored with exact same digest -> revalidate, do not gratuitously rerun independent tests;
17. restored evidence has different digest -> conflict/recovery, not auto-accept;
18. re-enable after recovery tries to reuse old effect capability -> reject epoch binding;
19. disable monitor can also re-enable -> design failure unless separately authorized as full H19 authority;
20. two-person approval policy configured later -> both approvals must bind exact same new activation digest/epoch; no inherited old approval.

## Advisory verdict

`EFFECT_ENABLE_IS_ENVIRONMENT_ELIGIBILITY, NOT STANDING_EFFECT_AUTHORITY`

and

`QUARANTINE_CLOSES_AN_ENABLE_EPOCH; REENABLE_ALWAYS_CREATES_A_NEW_ONE`.

The epoch model gives H19/H20 a mechanical way to preserve historical truth while refusing stale future authority. It also sharpens the network boundary: after a valid H6 cut but **before provider dispatch**, quarantine can still safely stop execution; after dispatch/in-flight, only provider cancellation/reconciliation can resolve outcome.

No database schema, effect state, provider permission, credential, configuration, deployment, Project setting or canonical coordination row was modified by this research.