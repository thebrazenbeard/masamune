# Mune Adversarial Pass — H13 Authority Enrollment/Recovery + H14 Confinement Attestation Harness

**Class:** `WORKING_PROJECT`  
**Canonical Vera coordination observed before analysis:** `3460`  
**Scope:** read/research/design only  
**No implementation authority:** no auth/config/plugin/permission/schema/provider mutation

## Executive result

H13 and H14 are the correct next problems, but each has a bootstrap trap:

- H13 can authenticate a provider subject without proving that the *initial Vera role assignment* was authentically authorized. Do not bootstrap `ACTOR_AUTHENTICATED` by attaching a strong login to a procedurally asserted role.
- H14 can hash an inspection matrix without proving the matrix was complete. Do not bootstrap `MECHANICALLY_CONFINED` by making incomplete observations immutable.

The architecture should preserve these origins instead of laundering them away.

---

# H13 — authority enrollment and recovery

## 1. Genesis enrollment is a distinct trust event

Suppose Patrick authenticates to a future Supabase/OIDC authority service and presents a valid provider subject `sub=P` with strong session assurance.

A server can now prove:

`this request came from authenticated provider subject P`.

It still needs a reason to conclude:

`P is Vera Creator Patrick with authority class X`.

If the only reason is a current ChatGPT instruction saying "bind this account to Patrick/Creator," the provider identity is authenticated but the **role assignment root remains procedural**.

Do not upgrade the genesis mapping to fully actor-authenticated merely because all later requests use a signed JWT.

Recommended genesis classification:

`PROCEDURAL_GENESIS_AUTHORITY_BOUND_TO_AUTHENTICATED_SUBJECT`

unless a separately authenticated/out-of-band authority root proves the initial mapping.

This is still a major improvement: future requests can be tied to one stable authenticated subject and cannot be made by arbitrary chat runtimes. But its origin claim remains honest.

## 2. Separate human identity enrollment from logical Vera role delegation

Patrick can be a provider-authenticated human subject.

`Voss` is different. In Vera, Voss is a governed logical role/persona/authority function, not automatically a separately authenticated human account.

Do not create a fake provider user called `Voss` and call that actor authentication.

Recommended distinction:

- `HUMAN_AUTHORITY_SUBJECT`: provider-authenticated person/account enrolled to Vera governance roles;
- `LOGICAL_GOVERNANCE_ROLE`: Voss/other Vera role whose authority derives from an admitted delegation/capability/policy, not from pretending the role is a human identity;
- `EXECUTION_RUNTIME`: the chat/service that consumes the role's admitted capability.

A Voss action may therefore have:

- human root: Patrick authenticated/enrolled;
- delegated logical authority: Voss scope/lease/capability;
- execution principal: service/runtime identity;

without claiming the runtime itself is Patrick or that `Voss` has a provider human identity.

## 3. JWT custom role claims must not become stale authority snapshots

Supabase custom claims can carry role/permission data, but JWTs are time-bounded snapshots.

If Vera authority is revocable/reroutable faster than token expiration, a JWT claim like:

`vera_role=CREATOR`

must not be the sole live authority check for protected effects.

Use JWT for **identity/session assurance**, then resolve the current Vera authority mapping from protected server-side state at issuance/consume time.

If a role/version hint is carried in the JWT, bind an `authority_mapping_version` and require current-server equality. A revoked mapping makes the token identity-valid but authority-stale.

This preserves:

`AUTHENTICATED_IDENTITY != CURRENT_AUTHORITY`.

## 4. Enrollment record should be append-only/evented, not a mutable role string

Minimum conceptual record/event fields:

- `authority_subject_id` random stable Vera ID;
- `provider_issuer` exact OIDC/Auth issuer;
- `provider_subject` protected exact subject or privacy-preserving keyed representation;
- `subject_kind = HUMAN | SERVICE | LOGICAL_ROLE`;
- `role_or_scope` closed Vera authority class;
- `project_scope` / optional assignment/effect ceiling;
- `admission_source_ref + digest`;
- `genesis_assurance` / current assurance class;
- `effective_from`, optional `expires_at`;
- `supersedes/revokes` lineage;
- `issuer_epoch` / enrollment policy version;
- privacy classification.

Do not overwrite the old mapping on revocation/rebind. Preserve why a prior capability was valid at the time.

Forked concurrent role mappings of equal authority should resolve `CONFLICTED`, not latest-timestamp-wins.

## 5. Provider subject identifiers, not usernames/emails

Use provider-stable subject identity as the primary enrollment key.

Do not bind Vera authority to mutable display names, email text or GitHub username strings where a stable provider subject/user ID exists.

If provider identity is replaced/rotated, require an explicit re-enrollment transition linking old and new subjects. Do not semantic-match accounts by email/name.

## 6. Present Patrick authority remains a proposal until authenticated enrollment consumes it

Under current architecture, Patrick's present-chat instruction is the strongest procedural authority evidence but not a cryptographically isolated actor root.

A future enrollment flow can treat present-turn authority as a **proposal/source binding**:

1. normalize exact requested enrollment/scope;
2. bind present-turn authority evidence digest/locator;
3. independently authenticate provider subject through authority service;
4. require explicit enrollment confirmation under the service's policy;
5. emit admitted enrollment event.

The authenticated service should not accept caller fields `actor=Patrick`, `role=Creator` as sufficient.

## 7. Recovery and compromise semantics

### Lost ordinary session/device

No authority change. New authenticated session for same provider subject re-resolves current mapping.

### Provider account recovery

Provider authentication may restore account access, but if recovery weakens assurance or changes subject identity, Vera must follow its own recovery policy. Provider recovery is not automatically Vera-role recovery.

### Subject rotation/replacement

Old mapping remains historical. New subject gets explicit successor enrollment. Until linked by authorized recovery, new identity is authenticated but has `NO_CURRENT_VERA_AUTHORITY`.

### Issuer state loss

Existing enrollment/capability verification must depend on durable protected records/public verification material, not issuer process memory. New issuance fails closed if required issuer state/key epoch is unavailable.

### Issuer compromise

Disable compromised issuer epoch. Unconsumed capabilities/enrollment changes from affected epoch become unusable/review-required. Historical actions are not deleted. If compromise start time is uncertain, affected authority evidence becomes `ASSURANCE_COMPROMISED_REVIEW_REQUIRED`.

### Delegation loss/revocation

Delegated logical role/capability resolves current ancestor validity at use. Revocation is prospective relative to the documented H6 authority cut; it does not rewrite already admitted historical state.

## 8. Break-glass enrollment/recovery cannot silently become normal authority

Emergency authority repair should use a separate human/admin principal and produce:

`OUT_OF_BAND_AUTHORITY_RECOVERY`

with explicit reason, target subject, scope, incident and reconciliation requirement.

Break-glass may restore availability but should not silently erase provenance or upgrade assurance. If break-glass is callable by an ordinary runtime, it is not break-glass.

## 9. Privacy

Public/native receipts should not expose raw provider subject/email/account identifiers unnecessarily.

Protected authority store may need exact issuer+subject for validation. External receipts can bind opaque `authority_subject_id` + evidence digest + assurance/scope/version.

Avoid storing reusable OAuth/JWT/bearer credentials in authority records or chat.

## 10. H13 hostile cases

1. valid provider JWT + no Vera mapping -> authenticated identity, no authority;
2. stale JWT custom claim says Creator after server-side mapping revoked -> deny current authority;
3. caller sets `role=Voss`/`actor=Patrick` -> ignored as authority;
4. Patrick subject mapped procedurally at genesis -> future identity authenticated but genesis origin remains procedural-bound;
5. same human logs in on new device -> same subject, mapping survives;
6. email/name changes -> no role change;
7. provider returns different subject after account migration -> explicit recovery/re-enrollment required;
8. two concurrent equal-authority mappings for same subject/scope -> conflict, no timestamp winner;
9. Voss logical role executes through different runtime -> authority comes from current delegation/capability, not runtime self-label;
10. parent Patrick/Voss delegation revoked before consume -> child denied;
11. issuer offline -> existing verification may work; new issuance fails closed;
12. issuer compromised with uncertain start -> affected history review-required;
13. break-glass mapping created -> out-of-band classification and post-recovery reconciliation required.

---

# H14 — confinement attestation harness

## 11. Observation classes must be evidence-typed

One harness should not treat all matrix fields as equally proven.

Recommended observation provenance per cell:

- `DECLARED_SCHEMA`: tool/action definition says capability exists;
- `CONTROL_PLANE_READBACK`: app/plugin/action permission state read from platform control plane;
- `PROVIDER_PRINCIPAL_INTROSPECTION`: provider reports principal/scopes/permissions;
- `ROUTE_PROBE_READ_ONLY`: safe route invocation proves connector/service reachable, not necessarily write action reachable;
- `NEGATIVE_EFFECT_PROBE`: dedicated canary mutation attempt proves denial; requires separately authorized disposable target because success would mutate;
- `POSITIVE_CANARY_PROBE`: dedicated disposable mutation proves capability; separately authorized test effect;
- `HISTORICAL_EFFECT_RECEIPT`: prior exact provider effect proves capability existed then, not necessarily now.

The H14 read-only stage can design these probes but must not perform a write-denial test on a real target. A supposedly negative write test can succeed, which is still a write.

## 12. Route invokability cannot always be inferred safely

A read-only call through an app proves the connection/principal can perform that read operation. It does not necessarily prove a specific write action is enabled.

Conversely, registered tool schema does not prove live route.

Therefore write-route qualification needs one of:

- control-plane/provider introspection that specifically binds the action/scope;
- historical recent exact effect evidence plus no material change, bounded by freshness policy;
- separately authorized disposable canary probe.

Without one, write invokability remains `UNKNOWN`, which blocks a positive strong confinement claim if that unknown route could be an alternate protected mutator.

## 13. Capability closure is conservative and effect-based

Each action contributes:

- direct effects;
- delegated/meta effects;
- downstream automation effects;
- privilege-escalation/capability-generating effects;
- unknown effects.

A tool labeled read-only by metadata is not automatically harmless if its actual provider semantics can trigger refresh/webhooks/jobs. Tool hints are evidence, not authority.

For arbitrary SQL/code/deploy/workflow mutation, over-approximate the closure. False positives are preferable to a false mechanical-confinement claim.

## 14. Control-plane expansion capability belongs in the graph

Ask whether the ordinary runtime can itself:

- install/connect a plugin/app;
- enable a disabled action;
- change app permission/action control;
- reconnect to a broader provider account;
- create/read credentials;
- alter publisher configuration.

If the runtime can expand its own effect surface without a separately authenticated human/admin gate, current confinement is unstable even if the starting tool set is narrow.

If install/permission changes require external user/admin confirmation and the ordinary runtime cannot complete them alone, model that boundary explicitly rather than treating the existence of a settings UI as runtime capability.

## 15. Staleness requires both event invalidation and bounded lifetime

Some changes are observable/eventful; some are not exposed to Vera.

Attestation should carry:

- `observed_at`;
- `valid_until` / maximum age per evidence class;
- exact tool/action schema digests;
- app/plugin permission/control-plane digest;
- provider principal/credential identifier + scope digest;
- runtime/config/environment digest;
- effect-graph policy/version;
- explicit `unknowns`;
- evidence refs/digests.

Known material changes immediately stale affected closure. Unobservable drift is bounded by expiration so a receipt never becomes timeless proof.

Provider-principal confinement may justify longer validity than exposed-surface enumeration if provider permissions are independently versioned/read back.

## 16. MA12 dependency

H14 can define typed normalized attestation facts now, but production cross-runtime digest/signature binding should not freeze until MA12's canonicalization contract is admitted.

Until then:

- local/proof hashes are evidence artifacts only;
- attestation schema/version fields are stable design inputs;
- persisted effect-authorizing receipt should not claim portable canonical digest semantics prematurely.

Once MA12 is admitted, H14 should publish golden vectors for the attestation normalizer, including unordered matrix inputs producing one canonical sorted representation.

## 17. Current negative controls

Current project evidence remains deliberately hostile:

- GitHub app permission override: `Allow all actions`;
- Supabase app permission override: `Allow all actions`;
- raw Supabase SQL reaches `postgres`;
- GitHub write has been demonstrated in Voss runtime.

H14 harness should be able to ingest these facts and deterministically return a non-confined result without relying on prose interpretation.

## 18. Recommended H14 result shape

Conceptual fields:

`attestation_status`:
- `MATRIX_RECORDED`
- `EXPOSED_SURFACE_CONFINED`
- `PROVIDER_PRINCIPAL_CONFINED`
- `END_TO_END_DECLARED_RUNTIME_CONFINED`
- `CONFLICTED`
- `UNKNOWN`
- `STALE`

Plus:

- `runtime_scope_id`
- `observation_scope`
- `protected_effect_classes`
- `ordinary_runtime_principals`
- `guarded_publisher_principal`
- `break_glass_principal`
- `matrix_digest` (after MA12)
- `capability_graph_digest` (after MA12)
- `evidence_by_cell`
- `unknown_edges`
- `bypass_paths`
- `provider_scope_residuals`
- `observed_at`
- `valid_until`
- `staleness_causes`

A positive result with non-empty material `unknown_edges` that could reach protected effects is invalid.

## 19. H14 hostile cases

1. tool registered but write route disabled -> do not mark invokable;
2. read route works, write route unknown -> write capability remains unknown;
3. action-control denies named write but alternate plugin uses same provider principal/effect -> bypass path;
4. raw tool hidden, provider credential broad -> provider-principal confinement fails;
5. deploy action narrow in schema, deployed runtime has broad secret -> transitive closure broad;
6. repo write touches privileged CI -> downstream provider effect included;
7. action permission changes after attestation -> stale;
8. provider scope changes with same tool schemas -> stale;
9. plugin version/action set changes -> stale;
10. unobservable platform route remains possible -> cannot exceed declared exposed/provider boundary;
11. `NEGATIVE_EFFECT_PROBE` unexpectedly succeeds -> record effect, qualification fails, do not retry;
12. MA12 canonicalization version changes -> receipt digest layer requalified, not silently reinterpreted;
13. ordinary runtime can enable/install equivalent mutator without external admin gate -> confinement fails;
14. break-glass callable by ordinary runtime -> confinement fails;
15. attestation expires with no refresh -> STALE, never historical PASS carried forward.

---

# Combined consequence

H13 should establish **who/which logical role currently holds authority** without making identity tokens into stale role snapshots.

H14 should establish **what a declared runtime can mechanically do** without making a tool inventory into universal capability proof.

They meet at the publisher/issuer boundary:

- H13 authenticates/maps human authority and delegates logical governance capability;
- H14 proves the ordinary runtime cannot bypass that guarded capability path within the achieved boundary;
- H6/E2 decide when the capability is consumed relative to assignment state/effect cut;
- MA12 makes the resulting receipt portable/reproducible.

No database, auth hook, OAuth client, role, plugin permission, provider credential, tool setting, producer repository branch, deployment, or native Project state was modified during this pass.