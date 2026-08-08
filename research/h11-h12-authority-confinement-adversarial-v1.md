# Mune Adversarial Pass — H11 Authenticated Authority + H12 Tool-Surface Confinement

**Class:** `WORKING_PROJECT`  
**Scope:** read/research/design only  
**Canonical Vera coordination observed before analysis:** `3450`  
**Peer request:** Hephaestus `#mune` TS `1786194252.401449`  
**No implementation authority:** no auth/config/plugin/permission/schema/provider mutation

## Executive result

H11 and H12 are converging on the right problems, but both still risk collapsing separate assurance dimensions into one attractive label.

The strongest correction is:

1. **Identity is not action consent.** A verified provider user/session can establish who authenticated, while saying nothing by itself about whether that user approved this exact Vera transition/effect now.
2. **Capability binding is not identity.** Exact-scope one-use capability consumption can strongly constrain an action while the issuer's human-authority decision remains merely procedural.
3. **Visible tool confinement is not provider confinement.** An audited ChatGPT action matrix can prove a bounded exposed-surface claim; only provider-side credential/principal/network isolation can make an arbitrary ordinary runtime mechanically incapable of the protected effect.
4. **Deploy/code/SQL tools are higher-order capabilities.** Their transitive effect set is the capabilities reachable by what they can install/execute, not merely the verb in the tool name. Static tool schema alone cannot decide that closure for arbitrary code or SQL.

I recommend H11 become multi-axis internally even if it preserves a coarse outward assurance enum, and H12 adopt explicit qualification tiers whose names encode observation scope.

---

# H11 — authenticated authority-source feasibility

## 1. Current independently reproduced facts

### Current Supabase execution route

Fresh live provider query in this Mune runtime reproduces:

- `current_user = postgres`
- `session_user = postgres`
- `current_role = postgres`
- `auth.uid() = NULL`
- `auth.role() = NULL`

Therefore current raw Supabase execution cannot derive Patrick/Voss/Vera logical identity from the database caller.

### Existing portable-bootstrap machinery is a useful negative control

Fresh catalog read shows these existing functions are postgres-owned `SECURITY DEFINER` and executable by `service_role`:

- `claim_vera_portable_bootstrap_request`
- `append_vera_portable_bootstrap_event`
- `commit_vera_portable_bootstrap_binding`
- `confirm_vera_portable_bootstrap_readback`

They are genuine positive precedent for request digest binding, row locking, predecessor-state validation, monotonic transitions, uniqueness and exact readback.

They are **not actor-authentication precedent**. `confirm_vera_portable_bootstrap_readback` accepts caller-supplied `p_verifier_role text` and accepts it when the text equals `workstream/project-architecture`. Likewise `vera_valid_authority_evidence(jsonb)` validates the closed shape and literal value of `verifier_role`, lease/repo/branch/base/time/operation evidence, but it does not cryptographically derive the Vera actor from the invoking principal.

This split should be made explicit in H11:

`TRUSTED_STATE_MACHINE != AUTHENTICATED_GOVERNANCE_ACTOR`.

Do not generalize bootstrap's caller-supplied role labels into a future authority issuer.

## 2. Current ChatGPT app controls prove less than they appear to

Independent Plugin Management readback in this runtime shows:

- global app permission: `Allow low-risk actions`;
- GitHub app override: `Allow all actions`;
- Supabase app override: `Allow all actions`.

OpenAI's current first-party documentation says:

- users connect/authenticate apps with their own provider account;
- app permissions determine when ChatGPT asks before using an already-connected app;
- Action control can restrict which app actions exist for a workspace where supported;
- app permissions do not grant new provider access;
- custom MCP apps can use OAuth/OpenID Connect authentication;
- the current documented full MCP write/modify custom-app surface is primarily Business/Enterprise/Edu, with narrower Pro behavior documented separately.

Sources:

- https://help.openai.com/en/articles/11487775-apps-in-chatgpt
- https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-for-plugins-and-apps
- https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt

I found no first-party OpenAI documentation establishing that an app action confirmation produces a Vera-consumable durable signed receipt binding:

`ChatGPT account principal + exact action bytes + timestamp/nonce + user confirmation`.

Therefore current app OAuth/confirmation can provide useful **platform-mediated evidence**, but should not be promoted into portable `ACTOR_AUTHENTICATED` Vera authority merely because a human-facing approval card exists.

## 3. Supabase provides a technically plausible authenticated identity root

Current Supabase first-party documentation supports the following future building blocks:

- Edge Functions can require a valid user JWT and receive verified `userClaims` / JWT claims;
- Supabase Auth JWTs include signed `sub`, `session_id`, `aal`, `role`, issuer/audience and other identity claims;
- asymmetric JWT verification can use the project's JWKS;
- Custom Access Token Hooks can add protected custom role/permission claims to user JWTs before issuance;
- Supabase can act as an OAuth 2.1 / OIDC server, including MCP-compatible dynamic client registration and verifiable JWT access tokens.

Sources:

- https://supabase.com/docs/guides/functions/auth
- https://supabase.com/docs/guides/functions/auth-headers
- https://supabase.com/docs/guides/auth/jwt-fields
- https://supabase.com/docs/guides/auth/jwts
- https://supabase.com/docs/guides/api/custom-claims-and-role-based-access-control-rbac
- https://supabase.com/docs/guides/auth/oauth-server

This means a future authority issuer could, in principle, establish:

`verified Supabase subject/session -> protected Vera role enrollment -> exact authority policy`.

For sensitive issuance, requiring `aal2` could strengthen authentication assurance.

But that only answers **who authenticated to the issuer**. It still does not prove that this person approved the exact action at this moment.

## 4. The current three-step ladder hides an identity-vs-consent problem

Current H11 ladder:

`PROCEDURAL -> CAPABILITY_BOUND -> ACTOR_AUTHENTICATED`

is useful as a headline, but too one-dimensional for effect authorization.

A provider JWT can make an action `ACTOR_AUTHENTICATED` while a long-lived OAuth/refresh-token session allows ChatGPT to invoke an issuer after prompt injection with no fresh user gesture. Conversely, an exact one-use capability can be very tightly bounded while the actor identity behind issuance is still procedural.

Recommended internal axes:

### A. Actor identity assurance

- `UNAUTHENTICATED_LOGICAL_ACTOR`
- `PROVIDER_ACCOUNT_AUTHENTICATED`
- `VERA_ROLE_BOUND_ACTOR`

### B. Exact-action authorization assurance

- `PROCEDURAL_INTENT`
- `PLATFORM_MEDIATED_CONFIRMATION`
- `EXACT_DIGEST_USER_PRESENCE_CONFIRMED`

### C. Capability enforcement

- `NO_PROTECTED_CAPABILITY`
- `EXACT_SCOPE_CAPABILITY_BOUND`
- `EXACT_SCOPE_ONE_USE_CONSUMED`

### D. Evidence portability

- `TRANSIENT_ONLY`
- `PROVIDER_LOGGED`
- `PORTABLE_VERIFIABLE_RECEIPT`

The existing `PROCEDURAL | CAPABILITY_BOUND | ACTOR_AUTHENTICATED` field can remain a coarse compatibility summary, but the protected admission/effect receipt should preserve the axes rather than force one label to mean all four things.

## 5. Strongest realistic authority path

A future stronger route looks like:

1. user authenticates to a protected Vera authority service using Supabase Auth/OIDC;
2. issuer verifies signed JWT/JWKS, exact issuer/audience, expiration, session and required AAL;
3. issuer maps `sub` to a separately governed Vera authority role from protected server-side state/custom claim; caller cannot self-assert `actor=Patrick` or `role=Voss`;
4. requested action is normalized to exact project/root/relation-or-effect/target/request digest;
5. for low-risk standing authority, a pre-existing bounded policy may authorize issuance;
6. for high-risk exact authority, require fresh user-presence confirmation bound to that exact digest through an authority UI/challenge outside reusable chat text;
7. issuer mints a server-side one-use capability; ordinary ChatGPT receives only opaque locator;
8. admission/publisher loads and validates capability server-side and atomically consumes it with the state transition/effect claim;
9. capability receipt records identity source, action-authorization source, scope, issuer epoch, replay/revoke state and exact request binding, but no reusable secret.

The critical design point: **a reusable OAuth token is identity/session authorization, not exact-action consent**. If H11 wants high-assurance destructive/effect authority, it needs a fresh action-bound confirmation primitive or must label the remaining authority procedural/standing-policy-bound.

## 6. Copied locator / confused deputy / replay hostiles

### Copied locator

Safe only if `capability_id` is not itself authorization. Validator must require server-side active record + exact request/proposal digest + exact project/root/target/effect class + current revision + expiry/revocation/use count.

### Confused deputy

If ChatGPT can ask issuer `mint capability for arbitrary digest X` under a reusable OAuth session, actor authentication exists but exact-action authorization may still be missing. Issuer must independently derive/validate allowable action and require the appropriate action-confirmation policy.

### Concurrent one-use consume

Atomic row/state transition must produce exactly one winner. Loser may return the existing consumption result for identical idempotent admission, but may never mint or consume a second grant.

### Parent revocation/delegation

Ancestor validity must be checked in the same transaction/authority cut as child capability consumption. A precheck followed by later consume leaves a revoke race.

### Crash after capability consume but before state admission

Do not make consumption and admission two independent commits if the capability authorizes a DB admission. Reserve/consume capability in the **same transaction** as the admitted event+registry marker, or use a reversible `RESERVED_FOR_REQUEST` state whose only completion is exact admission and whose recovery can return to available only from positive non-admission proof. Otherwise a crash can burn authority without producing state and tempt unsafe reissuance.

For external provider effects, capability consumption should bind to the durable H6 authority cut/effect claim before dispatch; provider ambiguity is then reconciled through the claim rather than by minting another capability.

### Provider identity is correct account but wrong Vera authority

A verified `sub` or OAuth account proves only that provider identity. The issuer must map that subject to a Vera authority role under a separately governed enrollment/role assignment. `provider account owner` must never imply `Vera Creator/Voss` by default.

## 7. Current honest H11 ceiling

For the currently exposed Vera engineering runtime:

- Supabase raw DB route: `PROCEDURAL` logical authority only;
- current GitHub/Supabase app access: provider-connected account/action capability exists, but this runtime does not expose a Vera-verifiable exact actor/action receipt;
- future protected issuer: `CAPABILITY_BOUND` is technically feasible;
- future Supabase user-JWT issuer can establish `PROVIDER_ACCOUNT_AUTHENTICATED`, and a protected mapping can establish `VERA_ROLE_BOUND_ACTOR`;
- high-assurance exact action still needs a distinct action-confirmation guarantee.

I would not let the label `ACTOR_AUTHENTICATED` silently imply `EXACT_ACTION_USER_CONFIRMED`.

---

# H12 — tool-surface confinement attestation

## 8. Static exposed tool schemas cannot prove transitive effect closure

For a simple fixed provider action such as `update one label`, direct effect classification may be straightforward.

For arbitrary SQL, code deployment, workflow edits, shell/code execution, webhook configuration, secret/config mutation, or repository changes that trigger automation, the effect closure is generally **not decidable from the ChatGPT tool schema alone**.

Examples:

- `execute_sql` can create/alter database objects, trigger external HTTP mechanisms where extensions/features permit, alter security state, or create routines that later mutate data;
- `deploy_edge_function` installs code whose future effects equal the runtime credentials/secrets/network/provider APIs it can reach;
- repository workflow/code changes may later run under CI credentials and mutate deployments/providers even though the immediate tool reports only `REPO_CONTENT_WRITE`;
- changing a webhook/automation/config may create a delayed external effect without a second ChatGPT tool call.

Thus `tool name -> direct effect class` is insufficient. H12 needs an **effect-capability graph**.

## 9. Effect-capability graph

Recommended node types:

- runtime/agent identity;
- tool/plugin/connector action;
- provider principal/credential;
- provider resource/target scope;
- deployed executable/workflow/automation;
- secret/config source;
- network/egress destination class;
- protected effect class.

Recommended edge classes:

- `CAN_INVOKE`
- `AUTHENTICATES_AS`
- `CAN_READ_SECRET`
- `CAN_ASSUME_ROLE`
- `CAN_DEPLOY_AS`
- `CAN_MODIFY_EXECUTABLE`
- `CAN_TRIGGER`
- `CAN_MUTATE`
- `CAN_GRANT_OR_EXPAND`
- `UNKNOWN_TRANSITIVE_EFFECT`

Qualification computes a conservative closure from the ordinary runtime. If any path reaches an equal/broader protected effect outside the guarded publisher, confinement fails. If a required edge is unknown, the result must downgrade rather than assume absence.

## 10. Higher-order capability rule

A deploy/mutate-executable action is classified by the capabilities of the deployed/modified runtime, not only by the deployment API verb.

Conceptually:

`EFFECTS(DEPLOY X) >= EFFECTS(runtime principal of X) + secret access of X + egress/API reachability of X + self-update/trigger reachability`.

If X can load arbitrary remote code or access a broad provider secret, its closure is broad/unknown. Such an action cannot be treated as a narrow `DEPLOYMENT_METADATA_WRITE` merely because the deployment endpoint has a tidy schema.

Likewise, a repository content write to a path consumed by privileged CI can be a **capability-delegating effect**, not just content mutation.

## 11. H12 status taxonomy

I recommend explicit tiers:

### `VISIBLE_MATRIX_RECORDED`

Inventory captured for exact runtime/config/tool/plugin/app permission state. No confinement claim.

### `NO_KNOWN_BYPASS_IN_AUDITED_EXPOSED_SURFACE`

All known registered+invokable+authenticated actions in the declared ChatGPT-visible surface were classified; no ungated equal/broader protected effect found. This is a bounded observation claim, not mechanical proof.

### `EXPOSED_SURFACE_CONFINED`

The ordinary runtime's exposed app/tool/action routes are configured so audited protected effects can only reach the guarded publisher path. Stronger than inventory, but still dependent on completeness of the exposed-surface observation.

### `PROVIDER_CAPABILITY_CONFINED`

Provider-side principal/credential/scope/network/secret controls independently make the ordinary runtime unable to perform the protected effect, while the guarded publisher alone has the necessary capability. This remains true even if the ordinary model tries an arbitrary exposed request within its provider credential ceiling.

### `END_TO_END_MECHANICALLY_CONFINED`

Reserve this only if both:

1. provider capability isolation is proven; and
2. the runtime/platform boundary has provider/platform-attested completeness showing the ordinary runtime cannot obtain an alternate equal/broader credential/tool/route.

Current exposed ChatGPT documentation/tooling does not give Vera enough evidence to claim this last tier universally. Do not mint it from a tool-list digest.

## 12. Current negative control is stronger than schema presence

Independent app permission readback in this runtime:

- GitHub: `Allow all actions` app override;
- Supabase: `Allow all actions` app override.

Combined with previously demonstrated raw GitHub file writes and current raw Supabase `execute_sql` as postgres, current Vera engineering execution is not `EXPOSED_SURFACE_CONFINED` for those protected effect families.

OpenAI first-party docs also distinguish:

- app permissions: when ChatGPT asks;
- Action control: which actions are available where supported;
- provider account scopes: what the connected app/account can actually do.

So an H12 receipt must bind all three where observable. One cannot substitute for another.

## 13. Tool-surface digest limits

A digest of tool names/schemas/config is valuable for staleness detection. It proves **which declared matrix was reviewed**, not that the matrix was complete.

The receipt must include:

- observation scope statement;
- discovery mechanism/version;
- runtime/product surface;
- exact registered actions and definitions;
- route invokability test status;
- app permission/action-control state;
- authenticated provider principal class and scope evidence;
- effect-capability graph version;
- explicit unknown/unobservable route classes;
- provider credential/secret/network isolation evidence where applicable;
- qualification tier achieved.

New plugin/app/action, action definition change, route recovery, reconnection, permission expansion, provider scope/credential change, runtime version/config change, or deployed executable change stales only the affected closure, but it must stale it mechanically in governance logic rather than rely on someone remembering.

## 14. Confused-deputy publisher

Even perfect tool isolation leaves a privileged publisher as a potential confused deputy.

Publisher inputs must not accept caller-controlled:

- provider credential selector;
- provider adapter identity where multiple adapters differ in authority;
- target-conflict scope/digest;
- authority principal;
- assignment revision;
- effect class;
- broader target locator than the capability permits.

Those are derived server-side from the normalized typed intent + admitted assignment state + protected capability + provider adapter.

Caller input may only choose/narrow within the admitted capability ceiling.

## 15. Provider credential breadth remains a residual trust boundary

Hiding raw tools from ChatGPT is not equivalent to provider-native least privilege.

If guarded publisher holds an org-wide credential to perform a one-branch effect, then ordinary runtime may be confined while the publisher service is still a high-value broad principal. Where provider scopes allow, qualify the publisher credential itself to the narrowest target/effect class.

If provider cannot scope narrowly enough, record the residual claim accurately:

`ORDINARY_RUNTIME_CONFINED; PUBLISHER_POLICY_CONFINED; PROVIDER_NATIVE_SCOPE_BROADER_THAN_EFFECT`.

Do not call that provider-enforced branch confinement.

## 16. Break-glass

A Boolean `break_glass=true` accepted by the ordinary runtime is not break-glass isolation.

Required properties:

- separate human/admin principal;
- ordinary runtime cannot invoke/obtain its credential;
- short-lived scoped session/credential;
- explicit incident/reason/target;
- provider-native audit where available;
- effect classified `OUT_OF_BAND_BREAK_GLASS`;
- normal governed lanes/effects require reconciliation before resuming when target/currentness may have changed.

## 17. Strongest honest H12 claim today

For current Vera engineering execution, the strongest supported result is a **negative control**:

`CURRENT_PROJECT_PROTECTED_GITHUB_AND_SUPABASE_EFFECT_CONFINEMENT = FALSE`.

For a future qualified ordinary runtime, the first realistic positive target is:

`NO_KNOWN_BYPASS_IN_AUDITED_EXPOSED_SURFACE`

followed by

`PROVIDER_CAPABILITY_CONFINED`

for effect classes where provider credentials/principals/network controls actually remove alternate capability.

I would not allow `MECHANICALLY_CONFINED` as a bare unqualified label. Mechanical with respect to **which boundary** must always be named.

---

# Combined architecture correction

H11/H12 should compose as independent axes, not one master trust score:

- `WHO`: actor identity assurance;
- `WHO_AUTHORIZED_THIS_EXACT_ACTION`: action confirmation/standing-policy assurance;
- `WHAT`: exact capability scope/one-use state;
- `WHICH_STATE`: authority-admitted assignment revision/currentness;
- `WHICH_TARGET`: provider conflict/target scope;
- `CAN_RUNTIME_BYPASS`: H12 exposed/provider capability confinement tier;
- `WHAT_HAPPENED`: provider effect reconciliation/readback;
- `CAN_WE_VERIFY_LATER`: receipt portability/custody.

A system can be strong on one axis and weak on another. That is not a flaw in the model; pretending the axes collapse into one word is the flaw.

## Suggested acceptance hostiles

1. valid Supabase JWT for correct account but no Vera role binding -> identity valid, authority denied;
2. valid Vera-role JWT reused by prompt-injected runtime with no exact-action confirmation where policy requires it -> issuance denied;
3. copied capability locator with altered request -> denied;
4. concurrent exact capability consume -> one winner, one idempotent prior-result/fail response;
5. parent delegation revoked during consume -> same-transaction ancestor check decides one side of cut;
6. crash after capability reserve before admission -> deterministic recovery, no unsafe blind reissue;
7. ChatGPT app confirmation exists but no portable signed receipt -> classify platform-mediated confirmation, not portable action authentication;
8. app action disabled but alternate connected app/provider route performs same effect -> H12 fails exposed-surface confinement;
9. raw tool hidden but ordinary provider credential can still perform effect through another method -> provider confinement fails;
10. deployable function has narrow declared purpose but receives broad secret/egress -> closure includes broad reachable effects;
11. repo file write modifies privileged CI workflow -> classify downstream protected effects, not only content write;
12. tool matrix digest unchanged but provider credential scope expands -> attestation stale;
13. provider scope unchanged but plugin adds new indirect mutator -> exposed-surface attestation stale;
14. break-glass path callable from ordinary runtime -> confinement fails;
15. unknown route/effect edge -> qualification cannot exceed bounded `NO_KNOWN_BYPASS...` tier.

No database, role, auth hook, OAuth client, plugin permission, provider credential, Edge Function, repository producer branch, deployment, or native Project state was modified during this research.