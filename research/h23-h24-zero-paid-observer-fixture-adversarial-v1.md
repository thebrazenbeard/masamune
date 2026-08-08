# Mune Adversarial Pass — H23 Zero-Paid Observer + H24 Quarantine Fixtures

**Class:** `WORKING_PROJECT`  
**Scope:** read/research/design only  
**Canonical Vera coordination observed before analysis:** through `3521`  
**Peer request:** Hephaestus `#mune` TS `1786197206.261829`  
**No provider/account/credential/config/permission/schema/native mutation.**

## Executive result

H23/H24 are directionally sound, but four remaining traps matter enough to freeze before implementation:

1. **Temporal coverage is not semantic coverage.** A source can be complete for one day while never recording the action class that matters. `NO_ADVERSE_EVENT_OBSERVED_WITHIN_COVERAGE` therefore needs a closed `covered_event_class_set` / `covered_effect_class_set`, not merely a time interval and successful query.
2. **Restored bytes do not restore a missed observation interval.** Exact ref+digest recovery can restore artifact integrity/current availability, but an outage interval remains an `OBSERVABILITY_GAP` unless another independent source covered it.
3. **A proved false alert does not prove no effect occurred.** F16 may clear the alert mechanism only after separately proving current protected state and provider outcome are reconciled; otherwise `FALSE_POSITIVE_RESOLVED` can coexist with an unrelated `OUTCOME_UNKNOWN` or historical gap.
4. **Cadence must be source- and risk-bounded.** `max_detection_latency` must be shorter than the shortest relied-on retention horizon by a safety margin and must account for manual-only sources. A source that can only be manually inspected cannot satisfy an automated observer SLO merely because its retention is long.

These are contract refinements, not objections to the overall architecture.

---

## H23 — zero-paid observation baseline

### 1. Separate four evidence dimensions

Every H23 source should declare independently:

- `source_availability`: runtime-readable | manual-provider-evidence | unavailable;
- `temporal_coverage`: exact queried interval, retention horizon, cursor/sequence completeness if available;
- `semantic_coverage`: closed provider event/action classes the source is documented or empirically known to record;
- `independence_class`: co-resident/admin-readable, provider-hosted same account, separately scoped observer, external separate-admin domain.

Do not let one dimension imply another. A current ChatGPT app-permission readback is useful `CURRENT_STATE` evidence but has no historical change interval. A Supabase API/Postgres log query can cover a time interval but not necessarily every organization/dashboard/control-plane mutation. A GitHub personal security log has long retention, but its 90-day horizon must not be promoted into evidence that every protected repository effect is represented unless the exact event category is covered.

### 2. Coverage certificate must be action-class aware

Recommended minimum receipt fields:

`source_id`, `provider`, `observed_at`, `coverage_start`, `coverage_end`, `retention_horizon`, `covered_event_class_set`, `covered_effect_class_set`, `query/filter identity`, `pagination_or_sequence_completeness`, `source_availability`, `independence_class`, `evidence_ref`, `evidence_digest`, `unknown_or_uncovered_classes`.

A positive bounded statement should be shaped like:

`NO_ADVERSE_EVENT_OBSERVED_WITHIN_COVERAGE(effect_classes=..., event_classes=..., interval=..., source_set=...)`

not a free-standing global status.

### 3. Current zero-paid facts do not establish independent absence proof

Current primary-source findings support H23's present ceiling:

- Supabase Free plan exposes one-day API/database log retention, while Platform Audit Logs are not included on Free.
- Supabase Platform Audit Logs record dashboard/Platform API organization-member actions and Account Audit Logs are the user-account subset; they are provider-hosted same-account evidence, not an independent failure domain.
- GitHub personal security log covers the last 90 days, but event-category coverage must be enumerated rather than inferred from retention length.
- ChatGPT app permissions describe when ChatGPT asks before app actions; they do not enlarge or narrow the provider access already granted and are current control-plane state, not a historical audit stream.

Therefore the strongest current zero-paid posture remains corroborative partial coverage. It cannot prove absence of postgres/admin or provider-account compromise.

### 4. Cadence contract

Do not freeze `hourly` as architecture. Freeze a relationship:

`max_detection_latency <= min(required_source_retention_horizons) - retrieval_safety_margin`

and separately require the chosen latency to satisfy the protected-effect risk policy.

If a required source is manual-only, report `AUTOMATED_DETECTION_SLO_UNSATISFIED` rather than pretending the manual retention window creates continuous observation. Scheduled polling is implementation/policy, not an intrinsic property of H23.

### 5. Same-account audit is corroboration, not independent observation

Account Audit Logs may narrow actor/time/action for provider-account control-plane activity, but the same authenticated account/admin domain can often influence both the action and the account's access to evidence. Treat this as `PROVIDER_HOSTED_SAME_ACCOUNT`, useful for incident reconstruction and cross-checking, not as H22's independent observer.

---

## H24 — fixture oracle refinements

### 1. F01 needs semantic-completeness precondition

`complete covered interval + no adverse event + matching current state` is only valid when every event/effect class required by the exact policy is covered by the source set. Otherwise expected output is `OBSERVABILITY_GAP`, even if every query succeeded.

Hostile fixture: source fully covers API requests for interval but does not cover app permission changes; request claims `coverage_complete=true`; adapter must reject the claim and return gap for the unobserved control-plane class.

### 2. F16 false-positive resolution is two-dimensional

A proven alert-mechanism defect can resolve the *alert*, but resuming effects also requires:

- current H13/H14/H18/activation state valid;
- no unresolved provider request/effect outcome for the implicated scope;
- no uncovered interval whose event classes could still contain an adverse mutation;
- exact target/provider state re-read where policy requires it.

Thus `FALSE_POSITIVE_RESOLVED` is an observer-event adjudication result, not by itself `EFFECT_ELIGIBLE`.

### 3. F17 + F22 must compose

Restoring the same immutable ref+digest proves current object identity/bytes and may move the evidence object's own lifecycle from `UNAVAILABLE -> REVALIDATE_REQUIRED -> VALID`.

It does **not** retroactively fill an interval in which the observer source was unavailable. The historical interval remains `OBSERVABILITY_GAP` unless an independent source with the required semantic coverage spans it. This prevents `same digest came back` from becoming time travel with better formatting.

### 4. Actor attribution and authorization remain separate

Known provider actor/token attribution must never imply the event was authorized. H24 already has this in F14; make it a global invariant so every fixture reuses the same rule:

`ATTRIBUTED_ACTOR != AUTHORIZED_EVENT`.

Authorization requires an exact prior/current authority/maintenance/effect receipt appropriate to that event class.

### 5. Quarantine scope should depend on effect overlap, not merely event severity

An adverse event that is independently proven non-controlling for the protected effect domain may yield `ADVERSE_EVENT_OBSERVED` with quarantine `NONE` for that domain while still requiring review. Conversely an apparently narrow event with unknown credential/effect transitivity must escalate. This preserves H20's separation between observation result and effect eligibility/quarantine scope.

### 6. Fixture inputs should carry explicit source-coverage topology

Add or require these sealed/provider-derived fields in the fixture contract:

- `required_effect_class_set`
- `required_event_class_set`
- `observed_source_set`
- `source_event_class_coverage`
- `source_temporal_coverage`
- `source_independence_class`
- `coverage_gap_intervals`
- `provider_outcome_state`

Keep them outside untrusted request control. The hostile request plane may request broader quarantine or abort, never claim stronger coverage, actor identity, authorization, or narrower effect scope.

---

## Recommended dispositions

- **H23:** `APPROVABLE_WITH_COVERAGE_CERTIFICATE_REFINEMENT`. Keep the current zero-paid ceiling and strengthen it with event-class coverage + manual-source/SLO honesty.
- **H24:** `APPROVABLE_WITH_RESTORATION_AND_FALSE_POSITIVE_COMPOSITION_REFINEMENT`. No redesign needed; add the semantic-coverage, restored-gap and false-alert/effect-eligibility hostiles.

## Sources checked

Current first-party documentation checked during this pass:

- Supabase Platform Audit Logs: Team/Enterprise only; Account Audit Logs show associated-user subset; provider action/actor/target metadata.
- Supabase pricing/logging: Free API/database log retention is 1 day; retention varies by plan.
- GitHub personal security log: personal-account actions involving the user for the last 90 days.
- OpenAI Apps: app permissions control when ChatGPT asks before app actions and do not grant new provider access.

These source facts constrain observation coverage; they do not prove Vera has a strong independent observer today.
