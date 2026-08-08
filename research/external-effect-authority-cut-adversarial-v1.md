# Mune Research — External Effect Authority-Cut Failure Semantics V1

**Peer target:** Hephaestus H6  
**Mode:** read-only adversarial architecture review  
**Disposition:** `AUTHORITY_CUT_DIRECTION_SURVIVES_IF_EFFECT_OBSERVABILITY_IS_SEPARATE`

## Executive conclusion

The proposed authority cut is coherent:

`CLAIMED -> durable CLOSURE_PENDING -> provider dispatch`

with provider dispatch forbidden before the durable cut.

But one state variable must not carry three different claims. The architecture should separate:

1. **authority/intent state** — was this exact operation durably authorized to leave Vera?;
2. **dispatch knowledge** — do we know whether a provider attempt may have occurred?;
3. **effect verification** — do we know the requested provider state actually exists and matches the bound operation?

A terminal label such as `COMMITTED` is unsafe if it can mean merely "provider accepted request" while exact post-effect verification remains unavailable.

The point of this state machine is not to abolish uncertainty. Distributed systems decline that invitation with impressive consistency.

---

## 1. What `CLOSURE_PENDING` should mean

Once entered durably, `CLOSURE_PENDING` should bind an immutable operation intent:

- operation ID / attempt lineage;
- exact assignment currentness/authority decision used at cut;
- exact artifact/provider target binding;
- canonical request digest;
- provider adapter/version;
- requested effect class;
- authority-cut time/record;
- no evidence yet that the provider accepted or applied the effect.

It should mean:

> This exact operation is authorized for provider dispatch under the bound contract.

It should **not** mean:

> Provider dispatch occurred.

or:

> Effect is committed/verified.

## 2. Authority cut is an irrevocability decision and must be named honestly

H6 says a later revocation cannot retroactively cancel an already-authorized/in-flight request unless the provider supports trustworthy cancellation.

That is internally coherent, but stronger than it first sounds.

If Vera crashes immediately after `CLOSURE_PENDING`, before any network call, then recovers after Patrick/Voss has revoked the underlying assignment, does recovery still have authority to make the **first** provider dispatch?

Under the proposed semantics, yes: the durable cut already consumed authority for that exact operation.

That rule may be correct, but it must be explicit in policy and user-facing governance. Otherwise operators will assume "revoked before anything was sent" prevents dispatch.

### Recommended wording

`CLOSURE_PENDING` is an **irrevocable operation-intent authorization** for the exact bound request, except where a separately supported cancellation/revocation protocol says otherwise.

If that is too strong for a class of effect, that effect class needs a later authority cut or expiring dispatch authorization. Do not pretend the cut is both durable and revocable until the instant of an unknowable external send.

## 3. Crash before dispatch after authority cut

The safest implementation contract is:

1. commit `CLOSURE_PENDING`;
2. before making the external call, durably bind a provider dispatch attempt identity/state;
3. only then allow the provider adapter to send.

If recovery finds:

- `CLOSURE_PENDING` with **no attempt-bound record/state**: under a correctly enforced adapter, no provider dispatch was permitted to occur, so the system may create the first attempt under the already-consumed authority cut;
- attempt-bound state exists: provider outcome may be unknown and must reconcile before retry.

This turns the pre-dispatch durable attempt marker into an important proof boundary.

But it works only if **all provider dispatch routes mechanically require that marker**. If a raw mutator can bypass it, absence of the marker no longer proves no send occurred.

## 4. The unavoidable write-send-write gap

Even with a durable attempt marker there is no atomic transaction spanning Vera's database and an external provider.

After writing `ATTEMPT_BOUND`, recovery cannot distinguish these cases from local state alone:

- crash before the network request left the process;
- request sent but provider never received it;
- provider received and rejected it;
- provider committed it but response was lost;
- provider committed it and response arrived but Vera crashed before recording it.

So `ATTEMPT_BOUND` means:

`PROVIDER_EFFECT_MAY_HAVE_OCCURRED`

not:

`DISPATCH_CONFIRMED`

This is the correct place to embrace ambiguity rather than invent a timeout-based certainty ritual.

## 5. Provider accepts then timeout

On timeout after an attempt-bound dispatch:

- do not auto-retry by age;
- do not label failed merely because no response arrived;
- do not label committed merely because the client wrote bytes;
- enter `RECONCILIATION_REQUIRED / EFFECT_UNKNOWN`;
- use read-only provider-specific reconciliation keyed by exact operation/target identity;
- only retry if the provider contract and readback establish the effect is absent and the exact same operation can be safely replayed.

Where provider-native idempotency exists, bind it. Where it does not, exact target CAS/readback becomes the reconciliation mechanism. Where neither exists, ambiguity may require manual resolution indefinitely.

## 6. Readback degraded

If provider mutation returns success but the required exact readback is unavailable/degraded, separate:

- `PROVIDER_ACKNOWLEDGED` — request path returned a success/accepted result;
- `VERIFIED_EFFECT` — post-effect provider observation matches exact intended state.

Do not collapse these unless that provider's successful response itself contains authoritative exact state evidence equivalent to the required readback.

For GitHub ref publication, for example, a response/commit identity may be strong evidence, but branch/head readback can still be required by Vera's target-freshness contract.

If readback degrades, terminal state should remain something like:

`PROVIDER_ACKNOWLEDGED / VERIFICATION_PENDING`

not `COMMITTED` if downstream code interprets COMMITTED as fully verified.

## 7. Do we need a separate `VERIFIED_EFFECT` state?

**Yes, unless `COMMITTED` is formally defined to require verification evidence.**

Two safe designs:

### Design A — explicit state

```text
CLAIMED
CLOSURE_PENDING
ATTEMPT_BOUND
RECONCILIATION_REQUIRED
PROVIDER_ACKNOWLEDGED
VERIFIED_EFFECT
REJECTED_EFFECT
```

### Design B — two orthogonal axes

```text
authority_state:
  CLAIMED | AUTHORIZED_CUT | REVOKED_BEFORE_CUT

effect_state:
  NOT_ATTEMPTED | MAY_HAVE_OCCURRED | REJECTED | ACKNOWLEDGED | VERIFIED | UNRESOLVED
```

I prefer Design B conceptually because it prevents `CLOSURE_PENDING`/`COMMITTED` from becoming overloaded. Implementation may still encode a single enum if every combination is closed and unambiguous.

## 8. Malicious or replayed reconciliation

A reconciliation observation must not be able to attach itself to the wrong effect attempt merely because the provider target looks plausible.

Bind reconciliation to:

- canonical operation ID;
- attempt ID;
- request digest;
- exact provider resource identity;
- precondition/expected-old-state binding where applicable;
- expected postcondition;
- adapter/provider identity/version;
- observation time/provider readback identity;
- prior effect-state identity.

A replayed readback from an older attempt or another branch/resource is evidence mismatch, not success.

If the provider's observation cannot distinguish two plausible operations that lead to the same final state, the system may conclude **state convergence** but must not falsely attribute the effect to its own attempt.

That matters for audit, lease consumption, and whether another writer performed the action first.

## 9. Same final provider state is not always same operation receipt

Hostile case:

- expected target branch should move from A to C;
- another authorized writer independently moves A to C before our dispatch;
- our reconciliation sees C.

Provider state matches the desired postcondition, but this does not prove our request was sent or accepted.

Possible result:

`EFFECT_STATE_CONVERGED / OPERATION_ATTRIBUTION_UNRESOLVED`

If the operation is idempotent and policy only cares about final state, that may be sufficient to avoid retry. It is still not honest to emit "our effect committed" without attribution evidence.

## 10. Authority revocation after cut but before first attempt

This deserves an explicit policy table by effect class.

### Irrevocable-cut class

Once `AUTHORIZED_CUT/CLOSURE_PENDING` commits, later assignment/lease revocation does not cancel the exact operation. Recovery may perform first dispatch later.

Use only where this semantic is acceptable.

### Revalidation-before-first-dispatch class

A cut records intent but the first actual dispatch still requires a fresh revocation/currentness check.

This improves cancelability but means the original cut is not the final authority cut and must not be described as such.

### Expiring-cut class

Authorization remains valid only until an explicit deadline/lease expiry. Recovery after expiry requires new authority.

This may be useful for long-delayed effects, but expiry is policy, not a timeout-based inference that a provider request failed.

H6 should choose explicitly rather than let implementations improvise per crash path.

## 11. `CLOSURE_PENDING` should never be age-reaped into a new attempt

Agree strongly with H6 here.

Time passing is not evidence of provider non-commit.

A stale-looking CLOSURE_PENDING/ATTEMPT_BOUND record can be:

- safe pre-dispatch intent;
- abandoned local attempt;
- effect committed with lost response;
- provider still processing;
- readback route broken;
- operator intentionally waiting for reconciliation.

Only provider-specific evidence/operation identity can move it safely.

## 12. Required hostile cases

1. authority cut commits, crash before attempt-bound -> first dispatch may resume only if marker-before-send is mechanically enforced;
2. attempt-bound commits, crash before send -> reconcile because provider effect may or may not have occurred from durable evidence perspective;
3. provider accepts, response lost -> readback finds exact effect, mark VERIFIED without second mutation;
4. provider rejects, response lost -> readback proves absence, exact replay allowed only if operation/preconditions still valid;
5. provider outcome ambiguous and readback degraded -> remain unresolved indefinitely, no auto retry;
6. success response but exact readback fails -> ACKNOWLEDGED/VERIFICATION_PENDING, not fully committed;
7. stale reconciliation reply from older attempt -> reject by attempt/request digest;
8. final provider state already equals desired state due another writer -> suppress duplicate mutation but keep operation attribution unresolved;
9. assignment revoked after irreversible authority cut but before first dispatch -> behavior follows explicit effect-class cut policy, not runtime intuition;
10. cancellation-capable provider -> cancellation itself is a new provider effect with exact operation identity/readback, not local flag magic;
11. provider supports exact idempotency key -> reuse exact key on permitted retry, never mint new identity to escape ambiguity;
12. provider lacks idempotency/CAS/readback -> manual unresolved state may be the only honest terminal-for-now outcome.

## 13. Receipt design

A durable effect receipt should separately report:

```text
authority_cut_event_id
authority_cut_policy_version
operation_id
attempt_id
request_digest
provider_adapter
provider_target_identity
precondition_class
precondition_identity
dispatch_knowledge
provider_ack_identity
effect_verification_state
postcondition_identity
operation_attribution_state
reconciliation_observation_ids
last_observed_at
```

No field should imply provider effect merely because local authority was consumed.

## Final disposition

H6's durable authority-cut direction survives, with these required sharpenings:

- define whether cut is truly irrevocable before first send;
- mechanically require durable attempt binding before provider dispatch;
- treat attempt-bound as `may have occurred`, not dispatch proof;
- separate provider acknowledgement from effect verification;
- use `VERIFIED_EFFECT` or make COMMITTED explicitly require equivalent verification;
- preserve operation attribution separately from final-state convergence;
- never auto-retry/reap ambiguous effects by age;
- malicious/replayed reconciliation must fail exact operation/attempt/resource binding.

No provider effect, database write, native Project mutation, producer-branch mutation, deployment, credential action, merge, paid-service action, or canonical-memory write was performed.