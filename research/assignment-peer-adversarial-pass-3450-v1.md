# Mune Assignment + Peer Adversarial Pass — through Vera coordination 3450

**Memory class:** `WORKING_PROJECT`  
**Reviewer/research lane:** Mune  
**Observed Vera coordination through:** `3450`  
**Repository write scope:** `thebrazenbeard/masamune:mune` only  
**Effects authorized by this artifact:** none outside Mune research/checkpoint custody  

This pass resolves the three current Mune assignments against newer coordination, refreshes exact provider evidence, and attacks the MA11/MA12 and H9/H10 designs requested in `#mune`. It is read/design evidence. It does not close Voss-owned assignments, apply database objects, change credentials/tool permissions, patch Masa's target, deploy anything, or authorize a provider effect.

## 1. MU3 — exact-head V3 rereview remains APPROVED, with implementation gates preserved

Fresh GitHub readback confirms `thebrazenbeard/masamune:masa` is still exactly:

`984cbdc781aa643443652f41f5a710f59e2d2439`

and the reviewed file remains:

`design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`

The exact artifact preserves the design corrections already accepted in `reviews/edge-privilege-v3-review-984cbdc-v1.md`: dedicated NOLOGIN creator/owner, dedicated API schema, global exact-creator routine default-privilege closure, current-routine ACL closure, strict SECURITY DEFINER search path with explicit `pg_temp` last, full qualification of sensitive objects, exact hostile tests, no service-role/postgres fallback, and repository-first/no-hosted-authority separation.

**Verdict remains `APPROVED` at design-contract level.** No new design blocker appears.

Two implementation/deployment gates remain mandatory and must not be softened into documentation trivia:

1. **Creator-role reachability must be proven from effective membership semantics, not `NOINHERIT`.** PostgreSQL 18 exposes `inherit_option`, `set_option`, and `admin_option` per membership in `pg_auth_members`; `SET ROLE` depends on a chain whose `SET` options permit the transition. A runtime that can `SET ROLE r9a0_edge_api_owner` has a creator path even if role-level NOINHERIT looks reassuring. Final acceptance therefore needs explicit negative `USAGE`/`SET`/administrative paths for the runtime principal and an enumerated migration-runner-to-owner creation path. Primary source: PostgreSQL 18 Role Membership / `pg_auth_members` / GRANT documentation.
2. **Transport feasibility must be proven without ambient broader capability.** A narrow custom PostgreSQL execution role is reachable in principle, but a managed Supabase Edge runtime cannot be accepted merely because happy-path code uses that role if the same function also receives usable RLS-bypassing secret/service-role credentials or a broader direct DB URL. The existing managed-runtime addendum remains controlling: narrow SQL ACLs are necessary, not sufficient; runtime capability containment must be demonstrated.

The useful distinction is now sharper: V3 is a correct least-privilege *database design stop condition*. H10/H12 decide whether the actual runtime is mechanically unable to route around it.

## 2. MU4 — correction custody direction remains approved; E2 is not automatically imported

Fresh live provider evidence:

- `vera_save_state_events`: 76 rows, 72 distinct `record_key` values, 8 `CORRECTION` rows.
- observed parents with more than one direct `supersedes_record_id` child: 0.
- observed `record_key` reuse across `(project_id, branch_id)` scopes: 0.
- `vera_current_save_state` remains `DISTINCT ON(record_key)` ordered by `state_time DESC, record_time DESC, record_id DESC`.
- `vera_save_state_events_supersedes_record_id_idx` remains non-unique.
- service-role effective table privileges on save-state: SELECT+INSERT true; UPDATE/DELETE/TRUNCATE false.
- save-state still has BEFORE UPDATE and BEFORE DELETE mutation blockers.
- `vera_context_events_v3` service-role privileges remain SELECT/INSERT/UPDATE/DELETE/TRUNCATE true.
- both tables are postgres-owned; owner/admin remains an explicit administrative trust boundary.

**MU4 disposition remains `APPROVED_CUSTODY_DIRECTION`.** Save-state is materially stronger for minimized correction custody than context-v3.

But the exact claim is narrow:

`SERVICE_PATH_APPEND_ONLY + NO_FORK_OBSERVED`

not:

`TAMPER_PROOF + FORK_PREVENTED`.

The global latest-by-key view is deterministic, but determinism is not conflict detection. If sibling successors appear, `DISTINCT ON` selects one by ordering instead of proving an unambiguous correction lineage. A safe zero-schema readback therefore still requires globally namespaced/scoped keys, direct sibling/fork detection, exact-row readback, and bounded writer discipline.

### Challenge to the E2-shaped temptation

Assignment E2 exists because an untrusted broad writer can consume a **canonical state-successor slot**, and downstream currentness depends on distinguishing authority-admitted state from proposal noise. Correction custody is not automatically the same problem.

Do not add an admission registry to corrections merely because the assignment design has one. First answer the domain question:

- Is the correction record itself authoritative evidence admitted under a bounded writer contract?
- Or does safety/currentness need a mechanically serialized one-successor state machine whose unauthorized sibling can consume a scarce authoritative slot?

Current evidence supports the former for the minimized correction record. The structural gaps are fork detection and key scoping, not yet a demonstrated need for a second authority-admission relation. One table-shaped hammer remains a hammer, even when it has excellent indexes.

## 3. MU5 — AP and correction continuity remain compatible only under strict upstream separation

**Disposition remains `COMPATIBLE_IF_STRICTLY_SEPARATED`.** H7/B9 evidence indirection strengthens this rather than changing it.

The privacy-preserving pattern should be:

- upstream safety/governance resolves correction continuity;
- sensitive correction plaintext remains in its governed custody surface;
- a release/qualification/native receipt may bind only an immutable opaque correction-evidence locator + digest + scope/status/candidate/config bindings required for verification;
- AP receives only already-settled upstream protected state that ordinary response generation was already entitled to consume;
- AP does not initiate correction retrieval, inspect correction plaintext for style, persist correction material, repair missing continuity, or invoke a second inference/API path.

Missing referenced correction evidence must yield **upstream semantic uncertainty**. It must not manufacture SAFE, manufacture RISK, resurrect a terminated unsupported branch, or change AP's persistence/inference budget.

The critical regression is call-graph invariance:

`AP_ON` and `AP_OFF` must use the same upstream safety/correction resolution path for protected state.

If enabling AP causes a correction lookup that would otherwise not occur, then correction continuity has become an AP dependency and the zero-added-retrieval/inference boundary is broken. If disabling AP prevents required correction resolution, the architecture is even worse: style machinery would have become a safety prerequisite.

Likewise, installation/qualification indirection must not leak intimate correction text into public/native receipts. Opaque identity/digest/status is enough where a downstream proof genuinely needs a binding.

## 4. MA11 adversarial response — E2 implementation preflight

### 4.1 Guarding only admitted predecessors is MVCC-sound under the stated atomicity, with one acceptance-test caveat

The smaller guard predicate is sound if and only if the protected admission registry is the canonical admission fact and canonical event + admission marker are committed in one transaction.

For a root, `supersedes_event_id=NULL`, so the guard has nothing to protect. An unadmitted fake root cannot consume another root's successor slot. A trusted root event and its marker remain uncommitted until the same transaction commits; another transaction cannot use the uncommitted root as a valid FK predecessor and independently commit around it. If marker insertion fails, the root event rolls back with the transaction.

For a successor, the predecessor is already admitted. Its BEFORE INSERT guard can therefore test predecessor admission before the new successor exists. The admission function's event insert sees the already-committed admitted predecessor, then registry insertion for the new event completes the same transaction.

PostgreSQL documents that triggers execute in the same transaction as the triggering statement and that failure rolls back both. It also documents the row-level BEFORE visibility rules. That supports the design, but **the exact nested admission path still needs an executable provider test** proving the guard observes the intended effective identity and predecessor membership in the real trigger/function combination.

### 4.2 Registry + coordination is not duplicate state, but it creates mandatory availability coupling

The design avoids two sources of *state truth* if the registry contains admission provenance only and never copies `relation`, `state_after`, currentness, owner, workload, or terminal state. The two stores then answer different questions:

- coordination: `what state event says`;
- protected registry: `whether that exact event was authority-admitted under the protected path`.

However, that means the registry is **not optional metadata**. If a coordination event is available but the required admission proof is missing/corrupt/unreadable, the resolver must return an admission-integrity/unverifiable state, not fall back to payload claims. Recovery semantics should say this explicitly. Otherwise the architecture quietly collapses back to trusting forgeable coordination JSON whenever the second relation is inconvenient.

### 4.3 Giving service_role column SELECT(event_id) is a real privacy tradeoff, not obviously the minimum

A SECURITY INVOKER guard that directly queries the private registry as service_role needs enough schema/table privilege to perform that lookup. Granting schema USAGE + column SELECT(event_id) exposes the membership set to any caller that can issue arbitrary SELECT through that principal, not merely the trigger. Event-ID existence can itself be sensitive provenance.

A potentially narrower design is a tiny hardened boolean membership helper that exposes only `is_protected_predecessor(uuid) -> bool`, with no listing interface, while the outer guard remains SECURITY INVOKER so it can capture/compare the invoker execution identity. But the helper becomes a privileged oracle and must be separately hardened: no attacker-controlled search path, no enumeration side channel beyond accepted UUID probes, exact EXECUTE closure, and no use of helper-definer identity as the admission-authority identity.

I would not freeze either route yet. The acceptance criterion is: **the ordinary writer must be able to ask only the minimum predecessor-protection question needed by the trigger, without acquiring general admission-registry visibility or a path into the admission owner.**

### 4.4 `request_key` should not pretend to cover rejected/no-op review if only admitted events have registry rows

This is the largest semantic ambiguity I see in MA11.

If every registry row means `this canonical event was admitted`, then a rejected review or a no-op decision correctly creates no registry row. But then `request_key UNIQUE` in the registry cannot also be described as the idempotency primitive for *all review attempts*. A rejected request can be replayed later and receive another review unless some separate proposal/decision evidence owns that idempotency.

That is not necessarily a bug. It means the identities must be named precisely:

- proposal/source identity and review-decision idempotency live in the proposal/decision evidence plane;
- admission registry `request_key` is the identity of a successful/potential canonical admission request, or can be replaced by source+digest plus predecessor-bound `admission_attempt_id` if redundant;
- rejected/no-op outcomes must never be inserted into the admission registry merely to reserve a key, because that muddies the invariant that registry membership means authority-admitted canonical state.

If the system needs exactly-once review disposition for rejected/no-op proposals, add that guarantee to the proposal/decision plane. Do not make the admission-proof table secretly double as a review queue.

### 4.5 Root NULL semantics need one mechanically closed meaning

The partial unique root rule assumes `prior_admitted_event_id IS NULL` means root. That is safe only if the registry forbids other NULL-prior marker classes. Enforce the root invariant mechanically, e.g. NULL prior implies `event_id=root_assign_event_id` and the corresponding coordination event satisfies the frozen root contract. Do not reserve NULL today for roots and later casually reuse it for imported/manual markers.

## 5. MA12 adversarial response — canonical receipt protocol

The restricted JCS direction is strong. RFC 8785 gives cross-language canonical JSON semantics, requires no duplicate object names under I-JSON, sorts object properties by UTF-16 code units, preserves array order, and explicitly performs no Unicode normalization. The latest Python/Node Unicode golden vector is therefore the right kind of test, not ornamental multilingualism.

### 5.1 Authority assurance is historical admission provenance, not a mutable policy result

A useful distinction is missing from a simple factual-vs-policy split.

`authority_assurance=PROCEDURAL|CAPABILITY_BOUND|ACTOR_AUTHENTICATED` can be an immutable fact about **how this event was admitted at that time**. A later policy change must not rewrite that history. Conversely, whether that historical assurance level is sufficient for a *current protected effect* is a policy decision.

I recommend three semantic bindings even if they are serialized into the existing three receipt layers:

1. **domain state facts**: event/root/prior IDs and factual state axes;
2. **admission provenance facts**: exact admission proof/assurance and immutable admission-policy identity that governed that historical admission;
3. **current policy decision**: whether those facts/provenance satisfy the exact current workload/effect/qualification policy.

Do not let changing today's minimum assurance level mutate yesterday's factual lineage digest. It should instead change the current policy-decision digest/status.

### 5.2 JCS is not an identifier-normalization policy

JCS preserving Unicode exactly is cryptographically desirable and semantically dangerous if humans treat visually similar identifiers as equivalent. NFC/NFD, bidi controls, zero-width characters, and confusables can remain different strings/digests by design.

Fix this *before canonicalization* in each domain schema:

- use ASCII closed tokens for schema/version/enums and most Vera-generated identifiers;
- use canonical UUID/hex/decimal forms;
- for provider locators, either define a provider-specific structural canonical form or deliberately treat the provider-returned value as opaque exact identity;
- reject control/bidi/invisible/confusable characters in human-authored security-sensitive identifiers unless the domain explicitly requires arbitrary Unicode;
- never use human visual similarity as authority equivalence.

Do not add NFC normalization inside JCS. That would create a Vera variant that no longer means RFC 8785 bytes.

### 5.3 Typed normalized object + digest should be normative; canonical wire bytes are derived evidence unless signed

Making stored canonical wire bytes the primary truth creates a dual-representation problem: typed object and byte blob can disagree. Prefer:

`typed normalized receipt object -> validate closed schema -> canonicalize under declared version -> hash/verify`.

Persisted canonical bytes can be cached/audit evidence. If a digital signature is over the canonical bytes, storing the signed byte string is useful, but a verifier should still parse/validate/recanonicalize and require exact byte equality before trusting the signature's semantic interpretation.

For ordinary SHA-256 receipt binding, the typed normalized object + digest + canonicalization version is sufficient.

### 5.4 Dual emission is not enough to prevent downgrade

During V1→V2 transition, a valid old V1 receipt could be replayed after V2 fixes a semantic ambiguity. Therefore every protected verifier needs an **acceptance policy**, not merely support code:

- receipt schema version;
- canonicalization version;
- policy version;
- exact accepted/minimum version set for the effect/release class;
- no `try V2, then fall back to V1` behavior;
- retired versions remain historically verifiable but become `HISTORICAL_ONLY / NOT_EFFECT_AUTHORIZING` unless an explicit compatibility policy says otherwise;
- cross-version translation requires its own explicit migration/translation receipt; equal domain facts do not make V1/V2 digest strings directly comparable.

Likewise, V1 should hard-fix SHA-256. A `hash_algorithm` field can be descriptive, but it must not become a caller-selectable algorithm-agility downgrade surface.

### 5.5 Golden vectors need to test the Vera normalizer, not only JCS

The canonicalizer vectors are necessary. The more likely security bugs sit one layer earlier. Add golden/negative vectors for:

- UUID uppercase/noncanonical spellings;
- enum case drift;
- explicit null vs missing;
- unknown fields;
- provider/source-ref grammar;
- forbidden identifier controls/bidi characters;
- opaque Unicode source refs whose exact distinction must be preserved;
- timestamp offset/precision variants;
- number-as-number rejection;
- policy version retirement/downgrade;
- raw-evidence projection vs factual projection excluding storage metadata such as event sequence/time where semantically irrelevant.

## 6. H9 adversarial response — capability-bound does not become actor-authenticated by damage minimization

The H9 architecture is directionally correct, but one phrase must remain uncompromising:

**exact binding + one-use does not compensate for missing actor authentication. It only bounds what a mistaken or malicious issuance can do.**

If the issuer accepts bad authority input and mints a perfectly scoped capability, the capability system will faithfully enforce the wrong decision. CAPABILITY_BOUND proves that a protected issuer admitted a bounded authority artifact and that this exact use complied with it. It does not prove Patrick personally authorized issuance unless the issuer itself has an independently authenticated Patrick authority root.

Specific hostiles:

- copied opaque locator + altered bytes must fail on server-side binding;
- copied locator + identical already-consumed request may return the prior result only, never create a second state/effect;
- locator lookup must not leak hidden capability existence or scope to unauthorized callers;
- concurrent one-use attempts require one transactional winner; loser reads the consumption receipt, not a second grant;
- ancestor revocation/expiry and child validity must be checked in the same authority-cut transaction as consumption; otherwise revoke-vs-consume races remain;
- issuer restart/offline must leave existing durable capability verification possible only if issuer epoch/key/status/revocation evidence remains available; new issuance fails closed;
- uncertain issuer-compromise time makes affected prior admissions `ASSURANCE_COMPROMISED / REVIEW_REQUIRED`, not retroactively erased and not silently trusted.

A non-secret locator is safe only because *possession is not the authorization predicate*. If any future API degenerates to `present capability_id => authorize`, the design has reinvented bearer secrets with extra columns.

Current provider evidence still caps the raw Supabase route at PROCEDURAL: `current_user=session_user=postgres`, `auth.uid()/auth.role() = NULL`. Voss coordination 3450 adds that a future verified Supabase user-JWT route may provide provider identity, but provider account identity would still need an explicit governance binding to Patrick/Vera authority before claiming ACTOR_AUTHENTICATED.

## 7. H10 adversarial response — strongest defensible confinement claim is surface-bounded

Do not publish `NO_BYPASS_EXISTS`.

The strongest honest form is closer to:

`NO_REACHABLE_UNGATED_EQUAL_OR_BROADER_MUTATOR_FOUND_IN_AUDITED_TOOL_CREDENTIAL_AND_INDIRECT_EFFECT_SURFACE_SET`.

The attestation must enumerate the audited set and explicit unknowns. A ChatGPT-visible tool manifest cannot by itself prove absence of undocumented internal routes. Current OpenAI documentation shows app permissions/action controls and user confirmation behavior, but it does not provide Vera a cryptographic proof that an inventory is the complete internal routing universe. Therefore the receipt is a deployment-surface qualification, not metaphysical completeness.

### Confused-deputy protections

A guarded publisher can still be a confused deputy if it accepts caller-chosen target/conflict scope or adapter identity. It must derive effect class, provider target, and conflict scope server-side from the typed requested operation and bound capability. Prompt text may describe intent; it does not define privilege boundaries.

### Provider credential scope matters even when raw tools are hidden

If the guarded publisher holds a credential capable of mutating the entire organization/project while the admitted effect is one branch/object, runtime isolation removes ordinary-agent bypass but does not give provider-enforced least privilege. Where the provider supports narrower credentials/scopes, acceptance should require them. Where it does not, label the residual trust accurately: `PUBLISHER_SERVICE_POLICY_CONFINED`, not provider-native target confinement.

### Equivalent-effect closure must follow capability, not tool name

A plugin named differently can still produce the same protected effect. Build equivalence classes by provider resource + mutation consequence. Indirect paths count too:

- raw SQL that changes webhooks/pg_net/functions/auth/config and thereby causes an external effect;
- Edge/function deployment that embeds an equivalent mutator;
- repository/admin APIs that alter workflow or credential behavior rather than the named target directly.

Any newly connected app/plugin, restored route, action addition, permission expansion, credential change, or meaningful tool-version change invalidates only the affected effect-class attestation but must do so automatically from the governance perspective.

### Break-glass must be a separate capability plane

`break_glass=true` on an ordinary tool is not break-glass isolation. The admin path must be physically unavailable to ordinary runtime, separately authenticated, time/scoped, independently audited, and followed by mandatory reconciliation. Otherwise “emergency” becomes the permanent bypass everyone mysteriously uses on Fridays.

Current project-level evidence remains a negative control: raw GitHub writes have been demonstrated from a Voss runtime and raw Supabase SQL is reachable, while app-level permissions currently permit those action classes. Therefore protected GitHub/Supabase effects are **not mechanically confined** in the present engineering runtime. This is a deployment architecture fact, not an accusation that the model will ignore policy.

## 8. Consolidated architecture consequence

The pieces now line up without pretending they are one mechanism:

1. **Knowledge Resolver** determines current governed state from typed domain evidence.
2. **E2 admission protection** decides which assignment state rows are mechanically admitted and protects their physical successor slots.
3. **Authority capability** bounds what an admitted authority artifact may authorize; current assurance can remain PROCEDURAL even when the data plane is mechanically protected.
4. **Effect claim/publisher** serializes target-conflicting provider mutations and reconciles ambiguous outcomes.
5. **Capability confinement** ensures ordinary runtime cannot route around the guarded publisher through an equal/broader mutator.
6. **Receipt canonicalization** makes the evidence graph reproducible across runtimes without confusing storage bytes, factual lineage, historical admission provenance, and current policy decisions.
7. **Correction continuity/AP separation** remains a separate safety-governance domain; do not unify it with assignment admission merely for schema symmetry.

The recurring design lesson is unpleasantly consistent: *a field that says something is trusted is not the same thing as a mechanism that makes the claim hard to forge, and a mechanism that makes it hard to forge is still not proof of who authorized it.*

## 9. Current dispositions from this pass

- `MU3`: `APPROVED_DESIGN`, exact target unchanged; implementation gates retained.
- `MU4`: `APPROVED_CUSTODY_DIRECTION`, fresh provider evidence supports prior result; structural fork/scope gaps remain.
- `MU5`: `COMPATIBLE_IF_STRICTLY_SEPARATED`, with opaque evidence indirection and AP call-graph invariance required.
- `MA11`: E2 remains preferred; request-key/rejection semantics and minimum registry-read exposure need tightening before implementation freeze.
- `MA12`: restricted JCS remains preferred; add admission-provenance distinction, domain identifier validation, downgrade policy, and normalizer golden vectors.
- `H9`: capability-bound reduces blast radius but cannot upgrade missing actor authentication.
- `H10`: confinement claims must be bounded to audited effect-capability surfaces and include indirect/equivalent mutators.

No database mutation, schema/ACL apply, provider permission change, producer-branch patch, merge, deployment, credential action, native Project mutation, or canonical-memory write was performed in this pass.