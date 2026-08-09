# Mune MU18 — Install Authority History Hostile Review

**Assignment:** provisional `MU18 / INSTALL_AUTHORITY_HISTORY_HOSTILE`, Voss Slack 2026-08-09 10:27 EDT  
**Primary bug:** TRIAGED MEDIUM `9094453e-5820-4424-9f93-0da44fdbc2c2`  
**Target:** H35 V3 release/install evidence machine + current R9A0 installation receipt surfaces  
**Current template reference:** `project/VERA_R9A0_INSTALLATION_RECEIPT_TEMPLATE.yaml` blob `2b8be7afc2816f7fa9547ef28cc95a4d2bebd260`  
**Disposition:** `CHANGES_REQUIRED_IN_CURRENT_BYTES; H35_HISTORY_SEMANTICS_APPROVED_WITH_DISPATCH_TIME_AUTHORITY_BINDING`

## Executive verdict

The install authority record must answer one historical question exactly:

> **What exact authority made this exact install dispatch permissible at the instant that dispatch began?**

It must not answer that question by storing a name, by re-resolving today's authority, or by embedding a future receipt into its own prerequisite chain.

The current template has only `authorized_by: null`. That is display metadata, not authority custody. It does not bind the decision, target, candidate, route, scope, attempt, effect class, authority epoch/time, or required capability/confinement evidence.

H35's separation is correct if tightened around **dispatch-time authority**:

- attempt identity is minted before dispatch;
- route is fixed for that attempt;
- exact authority is freshly resolved for the impending dispatch;
- immutable authority-decision evidence is persisted/readable before effect dispatch;
- the dispatch/result/final receipt bind that evidence by ID + digest;
- later authority movement affects future actions only and never rewrites the historical authorization fact.

## 1. Required authority-decision record

A closed `INSTALL_AUTHORITY_DECISION_V1` or exact equivalent should bind at least:

### Decision identity

- immutable `authority_decision_id`;
- `authority_decision_digest` over the closed semantic record;
- authority policy/version;
- issuer/authority source identity;
- decision event/time/epoch;
- immutable source locator/readback identity.

`authorized_by` may remain a human-readable label, but it has zero standalone effect authority.

### Exact effect scope

- `effect_class = INSTALL`;
- exact `route_class = ASSISTANT_TOOL | USER_MANUAL`;
- exact `install_attempt_id`;
- exact candidate identity: release ID + final candidate/head + manifest/checksum/settings identities required by the install protocol;
- exact Project/install target identity;
- exact allowed install scope/action class;
- exact installation policy/version.

Authority for one candidate or target is not portable to another.

### Dispatch preconditions

Bind the **pre-dispatch** evidence required by the chosen route.

For `ASSISTANT_TOOL` this includes the then-current assistant/tool install authority/capability and the H29 INSTALL-class confinement/retry/quarantine/target prerequisites that policy says are required.

For `USER_MANUAL`, bind exact user-owned manual installation authority and target/candidate scope. Do not fabricate assistant/tool capability or H29 execution evidence merely because the assistant later observes the result.

The authority record should bind evidence IDs/digests and their policy roles rather than copy volatile current answers into package bytes.

## 2. Attempt mint vs dispatch authority are different cuts

Minting `install_attempt_id` is not the effect.

Required ordering:

`ATTEMPT_MINT -> FRESH_ROUTE_SCOPED_AUTHORITY_RESOLUTION -> AUTHORITY_DECISION_PERSIST+READBACK -> DISPATCH -> BASE_OUTCOME_READBACK -> POST_EFFECT_EVIDENCE -> FINAL_RECEIPT -> FINAL_RECEIPT_READBACK`

Hostile:

1. attempt A is minted while authority is valid;
2. authority is revoked or target scope changes;
3. dispatch occurs using only the stale attempt-mint state.

Expected: dispatch is blocked. Attempt identity carries no authority by itself.

If authority changes **after** a valid dispatch begins, the historical dispatch does not retroactively become unauthorized. New retries, resume actions, repair effects, or later installs must freshly resolve current authority as required by their action policy.

## 3. Hostile matrix

### H1 — forged `authorized_by`

Receipt says:

`authorized_by: Patrick`

with no immutable decision record.

Expected: no authority claim. `authorized_by` is annotation only; final receipt cannot become authority-valid from this scalar.

### H2 — valid authority, wrong target

Authority decision permits installing candidate C into Project P1.

Attempt targets P2.

Expected: dispatch blocked `TARGET_SCOPE_MISMATCH`; P1 authority cannot be reused.

### H3 — valid authority, wrong candidate/version

Authority binds candidate head C1. Candidate moves to C2 before dispatch.

Expected: C1 authority is historical/valid for C1 only; C2 dispatch requires a new exact authority decision or a policy-authorized decision whose semantics explicitly cover C2. Do not stretch an exact receipt by prose.

### H4 — authority changes between attempt mint and dispatch

Attempt minted at T1 under valid authority; authority revoked at T2; dispatch attempted T3.

Expected: dispatch fails because dispatch-time fresh authority is not valid. Attempt remains historical/prepared, not authorized-to-execute.

### H5 — authority revocation after valid dispatch

Authority valid at dispatch T1. Effect begins. Authority revoked at T2 before final receipt is assembled.

Expected:

- final receipt may still attest that dispatch at T1 was validly authorized, because it binds the immutable T1 decision;
- later revocation must not cause the final receipt generator to query today's authority and rewrite history to “unauthorized”;
- future effect eligibility is blocked/re-evaluated by current authority.

Historical truth and future permission are different axes.

### H6 — blind retry after ambiguous outcome with stale authority

Dispatch outcome is ambiguous. Authority later changes. Caller blindly retries the same effect because the first attempt had valid authority.

Expected: no blind retry. Reconcile exact operation/attempt outcome first. Any genuinely new dispatch consumes the current route/effect authority requirements. Historical authority for the first dispatch does not authorize a second one.

### H7 — route switch inside one attempt

Attempt minted `ASSISTANT_TOOL`, but install becomes user-manual after tool failure, or vice versa.

Expected: route switch does not mutate the existing attempt. Reconcile the first attempt/outcome; mint a new attempt with the new fixed route and a new route-scoped authority decision.

This prevents authority from one route being laundered into another.

### H8 — manual route overclaims assistant execution

User manually replaces Project files under exact user authority. Assistant later verifies file/readback state.

Expected receipt:

- route = USER_MANUAL;
- manual authority evidence bound;
- assistant observation/readback provenance bound separately;
- no claim that assistant/tool performed the installation;
- H29 assistant execution gate is not retroactively invented for the manual effect.

### H9 — manual route claims atomic native transaction

The current template includes `atomic_file_replacement_verified`. Current Project installation architecture instead requires quiesced, controlled, **nontransactional** replacement with final exact logical active-set/readback.

Expected: manual install receipt proves the actual supported protocol: quiescence, installation-in-progress guard/readback where applicable, bounded removal/upload operations, exact final logical file/Settings set, duplicate/suffix/hash checks, fresh-runtime base readback.

It must not claim a backend atomic transaction that the platform does not provide.

This is related to the existing atomic-upload defect, not a new authority bug.

### H10 — authority record points to mutable prose only

Receipt binds a Slack message URL or free-text approval that can be edited/deleted and has no captured digest/decision receipt.

Expected: insufficient immutable authority custody. Bind an admitted immutable/captured decision record + content/semantic digest + source locator.

### H11 — final receipt readback after later authority revocation

Final receipt was properly assembled from a dispatch-time authority record and effect evidence. Before independent final-receipt readback, current authority is revoked.

Expected:

- independent readback can still verify the historical receipt bytes/digests and installed-artifact identity;
- `INSTALLED_ARTIFACT_IDENTITY_VERIFIED` may become historical truth;
- `CURRENT_PROTECTED_EFFECT_ELIGIBILITY` or any future install/repair action can be blocked by current authority;
- do not invalidate historical installed-artifact provenance solely because current authority moved.

### H12 — final receipt self-authorizes the install

Authority decision record is created only after install, or points to the final install receipt itself.

Expected: invalid/cyclic authority provenance. Pre-dispatch authority evidence must exist independently before dispatch.

## 4. Closed historical projections

Keep at least these outputs separate:

### `INSTALL_DISPATCH_AUTHORITY_HISTORICAL`

Historical fact derived from the immutable dispatch-time decision + exact attempt/target/candidate/route binding.

It never changes merely because today's authority changes.

### `INSTALLED_ARTIFACT_IDENTITY_VERIFIED`

Historical installed artifact fact produced only after successful final receipt readback over the post-effect chain.

It depends on the historical dispatch authority record but is not current permission.

### `INSTALLED_VERIFIED_CURRENT`

Current aggregate requiring whatever H35 says must remain current, such as active-release selection, post-install environment/in-situ qualification, etc. Do not derive it solely from historical install authority.

### `CURRENT_PROTECTED_EFFECT_ELIGIBILITY`

Fresh future-action decision over current authority, target, capability/confinement, quarantine/outcome and exact installed candidate. Historical install authority contributes provenance only.

## 5. Minimum receipt fields / bindings

The final installation receipt should bind, directly or through immutable subordinate receipts:

- `install_attempt_id`;
- `route_class`;
- candidate/release/head/manifest/checksum/settings identity;
- exact target fingerprint;
- `authority_decision_id` + digest + issuer/source + policy/version + decision time/epoch;
- exact authority scope/effect class;
- route-required capability/confinement/precondition evidence IDs/digests at dispatch;
- dispatch operation identity/outcome receipt;
- base outcome readback identity;
- cold-start/post-install/in-situ evidence IDs/digests;
- final receipt operation identity;
- final receipt readback identity.

Do not replace these with one `authorized_by` string.

## 6. Byte-shaping consequence

Current bytes are `CHANGES_REQUIRED` because receipt template blob `2b8be7af...` cannot represent the authority record above and still contains obsolete atomic-replacement wording.

The correction remains inside already-admitted install surfaces. No path75 is required.

Do not author final Receipt/Cold Start/Post-Install/Recovery semantics piecemeal. Freeze one integrated H35/H37/B17 field packet first so attempt/route/authority/environment/post-effect ordering stays acyclic.

## Final disposition

`H35_HISTORY_SEMANTICS_APPROVED_WITH_DISPATCH_TIME_AUTHORITY_BINDING`.

`CURRENT_INSTALL_BYTES_CHANGES_REQUIRED`.

No install effect, Project mutation, producer branch write, provider/config/schema mutation, credential action, canonical coordination write, merge or deployment was performed by MU18.