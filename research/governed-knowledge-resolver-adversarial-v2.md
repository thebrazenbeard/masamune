# Mune Research — Governed Knowledge Resolver Adversarial Architecture V2

**Supersedes:** `research/governed-knowledge-resolver-adversarial-v1.md` for all changed conclusions  
**Lane:** direct-user / cross-facet design challenge  
**Vera evidence consumed:** canonical through `3382` plus current shared-channel refinements through 2026-08-08 07:44 EDT  
**Mode:** research/design only; no Supabase/native Project/producer-branch mutation  
**Primary domain:** `ASSIGNMENT_CURRENTNESS`

## Immediate correction to V1

`MUNE-KR-CORR-001` — **V1 incorrectly described `vera_coordination_events.event_sequence` as caller-supplied because I read `column_default = NULL` without checking identity metadata.** Fresh catalog readback shows:

- `is_identity = YES`
- `identity_generation = ALWAYS`
- backing sequence `public.vera_coordination_events_event_sequence_seq`

Masa's correction was right. The field is database-generated identity, not freely supplied by an ordinary INSERT.

The **high-water conclusion does not change**: PostgreSQL identity uses a sequence, and sequence allocation is not transactional/rollback-coupled to row visibility. `MAX(event_sequence)` remains an audit locator, not a commit-completeness watermark or compare-and-swap token.

This forward correction terminates the contrary V1 schema claim. Do not cite V1's caller-supplied-sequence wording as current.

## Current conclusion

The strongest V1 architecture now looks like:

`trusted admission -> one normalized linear assignment-state chain -> typed resolver -> action-specific eligibility gates -> target-specific effect adapter`

with source topology/completeness explicit and current operational Slack coordination treated as provisional until canonicalization or explicit multi-source resolution.

The resolver should **not** make one boolean answer carry assignment currentness, workload eligibility, mutation authority, source completeness, and provider-target freshness. Human beings already invented enough overloaded booleans.

---

## 1. Masa's linear-state-chain proposal mostly survives, with a semantic constraint

Masa proposes that every conforming non-root `ASSIGNMENT_EVENT_V1` use top-level:

`supersedes_event_id = predecessor_state_event_id`

while payload `relation` says whether the transition is AMEND, BLOCK, REACTIVATE, etc. This deliberately reuses the existing unique one-successor index as a no-fork state-chain primitive.

### Verdict

**Accept for conforming V1 assignment-state snapshots, but redefine the field locally as "this normalized state snapshot replaces the prior normalized state snapshot."**

That is not the same as saying every semantic transition is literally a `SUPERSEDE` relation. The top-level FK carries state-chain predecessor identity; payload `relation` carries business semantics.

This is defensible because each state-changing snapshot really does replace the prior representation of current assignment state.

### Hard conditions

The resolver/writer must enforce:

1. exactly one conforming root `ASSIGN` per canonical assignment thread/root;
2. every state successor points to the immediately prior state snapshot in the **same assignment root/thread**;
3. `state_after` is a complete closed state snapshot, not a partial patch whose missing fields require guessing;
4. relation and `state_after` must be mutually valid;
5. non-state reviews/ACK/evidence rows stay outside the chain **unless they change assignment state**;
6. any review/approval/correction that changes state must be normalized into a state-chain successor rather than leaving the resolver to infer sideband semantics;
7. multiple roots, cross-thread predecessors, cycles, wrong-root successors, or unregistered transition schemas resolve `CONFLICTED/UNKNOWN`, never timestamp-winner.

The existing unique one-successor index prevents two rows from naming the same predecessor. It **does not prevent two root ASSIGN rows**, does not prove same-root linkage, and does not prove that a successor's full `state_after` was honestly derived from its predecessor. Those remain resolver/admission invariants in zero-schema proof mode.

## 2. Serialization is a feature for V1, not a bug

A single state-changing chain means two orthogonal changes cannot both commit as children of the same predecessor. One must serialize after the other.

That reduces concurrency but simplifies effect-critical reasoning:

- no merge semantics for OWNER change versus DEPENDENCY change;
- no multi-parent state join;
- no "latest in each dimension" reconstruction;
- no hidden conflict-resolution precedence table.

For assignment governance V1, I prefer serialization.

### Required concurrent-writer behavior

Two state writers based on predecessor X:

- first accepted successor X->A wins the unique predecessor slot;
- second insert based on X must fail/reconcile;
- second writer then rereads A, determines whether its intended transition remains authorized, and constructs a new A->B successor if still valid.

Do **not** silently retarget the second event or treat unique-index failure as a harmless retry. The transition may no longer be valid after A.

## 3. `SUPERSEDE` needs root/lane semantics or it will corrupt workload identity

There are two very different meanings hidden inside "supersede":

1. **state successor within the same work objective/lane**, and
2. **retire this work objective and replace it with a genuinely different one**.

If every successor automatically preserves the same root ASSIGN identity, meaning (2) cannot be represented honestly.

Recommendation for V1:

- ordinary AMEND / BLOCK / RELEASE / REROUTE / REVIEW-state-change / REACTIVATE preserve the same root assignment identity;
- a genuinely new independent objective starts a **new root ASSIGN**;
- replacement between roots is represented by an explicit cross-root `replacement_of` / retirement reference in the new root's typed payload or a separately typed coordinator transition, not by pretending the new objective is simply another snapshot of the old root;
- split/merge remain out of V1.

This keeps workload identity and audit history intelligible.

## 4. Prefer derived workload-lane identity over a caller-supplied key

The newer Hephaestus V4 simplification is stronger than a persisted arbitrary `workload_lane_key`:

`canonical_workload_lane_id = root ASSIGN event_id`

For a conforming canonical chain, this gives us an immutable, database-generated lane identity without trusting a payload token minted by the assignee.

### Carry-forward rule

All same-objective state successors inherit the root ASSIGN event identity through resolver traversal. They do not store or self-declare a new lane identity.

### Provisional-source bridge

A Slack-only provisional assignment lacks a canonical root event ID. During transition:

- provisional identity is its exact source locator, not a self-authored semantic key;
- once canonicalized, an authority-bound bridge maps that provisional locator to the canonical root ASSIGN event ID;
- unresolved provisional + canonical duplicates cannot both satisfy the workload floor;
- if the bridge is missing or conflicting, workload identity is `UNKNOWN/CONFLICTED` and contributes zero duplicate-floor promotion.

Long term, canonicalize assignment-affecting state before effect and before durable workload accounting whenever operationally possible.

## 5. Dual-axis state is necessary, but two axes are still not enough

Vera's challenge is correct: current assignment and mutation authority are orthogonal.

A useful minimal normalized snapshot should separate at least:

```text
assignment_state:
  CURRENT | NON_CURRENT

blocking_state:
  NONE | DEPENDENCY_BLOCKED | TERMINAL_BLOCKED

authority_binding_state:
  NOT_REQUIRED | VALID | STALE | REVOKED | CONSUMED | UNKNOWN

artifact_binding_state:
  NOT_REQUIRED | VALID | STALE | UNKNOWN

terminal_disposition:
  NONE | COMPLETE | CANCELLED | SUPERSEDED | REROUTED_AWAY | TERMINALLY_BLOCKED
```

Source health and external target freshness do **not** belong in this assignment snapshot.

### Why not one `executable` boolean

`false` could mean:

- obsolete assignment;
- current but waiting on dependency;
- current read-only work whose mutation lease is irrelevant;
- current mutation-bound work with consumed lease;
- current assignment with stale artifact binding;
- resolver source incomplete;
- provider target moved.

Those states have very different operator actions.

## 6. Derive eligibility per requested action, not globally

The resolver should answer facts; policy derives whether a **specific requested action** is allowed.

Suggested action classes:

```text
START_OR_RESUME_REASONING
REPORT_ACTIVE
COUNT_EXECUTABLE_WORKLOAD_FLOOR
USE_MUTATION_AUTHORITY
PERFORM_EXTERNAL_EFFECT
```

Example gates:

### START_OR_RESUME_REASONING
Requires assignment current + nonterminal + source complete enough for the domain. A read-only assignment can be executable with `authority_binding_state=NOT_REQUIRED`.

### COUNT_EXECUTABLE_WORKLOAD_FLOOR
Requires one unique canonical/provisionally-bridged lane identity, assignment CURRENT, blocking NONE, terminal NONE, and the lane has a permitted executable next action now. A dependency-blocked lane remains assigned but does **not** satisfy the executable floor.

### USE_MUTATION_AUTHORITY
Additionally requires authority binding VALID and any bound artifact/head still valid.

### PERFORM_EXTERNAL_EFFECT
Additionally requires target-side precondition strength sufficient for that provider/effect plus post-effect readback/reconciliation.

This prevents callers from interpreting `CURRENT` as implicit mutation authority.

## 7. Source topology, completeness, consistency, and freshness are four different things

Do not compress them.

```text
source_mode:
  CANONICAL_ONLY | MULTI_SOURCE | PRESENT_PLUS_DURABLE

source_completeness:
  COMPLETE | INCOMPLETE | UNKNOWN

consistency:
  ATOMIC_SINGLE_SOURCE_SNAPSHOT | NON_ATOMIC_MULTI_SOURCE

freshness:
  FRESH_AT_OBSERVATION | STALE | UNKNOWN
```

`COMPLETE` is meaningful only relative to a versioned authoritative-surface registry for the domain. A multi-source query cannot claim completeness merely because every adapter it happened to call returned successfully.

Receipt therefore also binds:

`authority_surface_registry_version` and `adapter_registry_version`.

## 8. Supabase-only operational currentness remains source-incomplete today

Canonical coordination and Slack operational routing are still not synchronized strongly enough to treat canonical-only resolution as always production-complete.

The 3313 history remains the canonical counterexample used by Voss/Masa: current operational state advanced through Slack/repository handoffs while the canonical assignment row remained older.

Recommended transition:

- `CANONICAL_SNAPSHOT`: deterministic canonical answer with explicit completeness result;
- `OPERATIONAL_CURRENTNESS`: present/Slack/durable combination with `NON_ATOMIC_MULTI_SOURCE` where required;
- external mutation requires canonical lease/effect authority or fresh exact present-user authority under the current forward gate, not merely a Slack provisional lane.

Long-term preference remains canonicalize authoritative assignment changes before they can drive effects.

## 9. Corrected sequence/high-water semantics

Fresh catalog evidence:

- `event_sequence` is `GENERATED ALWAYS AS IDENTITY`;
- it has a backing PostgreSQL sequence;
- it is unique.

This is stronger identity than V1 credited.

It is still **not** a commit-completeness CAS.

A transaction may allocate N and remain uncommitted while another transaction allocates N+1 and commits. A snapshot can observe N+1 without N. Later N becomes visible while the visible MAX remains N+1.

Therefore:

- `max_visible_event_sequence` is an audit locator;
- a receipt binds actual controlling/candidate event IDs and source snapshot identity/observation;
- before a gated effect, fully re-resolve the relevant lineage;
- never accept `MAX(sequence) unchanged` as the sole freshness proof.

Primary PostgreSQL 17 sources: transaction isolation, explicit/advisory locking, and sequence-function documentation.

## 10. Effect freshness: current GitHub connector is not exact expected-head CAS

Fresh connector schema confirms the exposed `GitHub.update_ref` operation accepts:

`{repository, branch_name, sha, force=false}`

It exposes no `expected_old_head` / `beforeOid` field.

GitHub's REST reference-update API documents `force=false` as a **fast-forward guard**. It prevents overwriting work with a non-fast-forward ref move, but it does not require the ref to equal a caller-specified exact old SHA.

GitHub's GraphQL `updateRefs` supports `beforeOid`, which does provide the exact precondition we actually want: update only if the ref points to the expected object before the atomic ref update.

### Consequence

For Vera's stronger invariant "unexpected branch movement pauses publication," current connector `update_ref(force=false)` is insufficient as a **mechanical exact-head CAS**.

A fast-forward update can still succeed after some unexpected ref movements when the moved-to ref is already an ancestor of the candidate, or when another writer has already moved the ref to the candidate. That may avoid content loss but fails exact operation-attribution/freshness semantics.

### Current bounded policy recommendation

Classify provider preconditions:

```text
EXACT_EXPECTED_HEAD_CAS
FAST_FORWARD_GUARD
OBJECT_VERSION_CAS
READBACK_ONLY
NONE
```

For a repository effect whose contract explicitly requires exact old-head equality, require `EXACT_EXPECTED_HEAD_CAS`. If the current adapter cannot expose it, the effect should fail closed or route through a separately authorized provider path that does.

Bounded sole-writer lease + exact candidate parent + pre-read + `force=false` + immediate readback is a useful **weaker** safety boundary for reversible low-risk writes, but it must not be mislabeled exact CAS and cannot satisfy a contract that explicitly says any unexpected branch movement invalidates publication.

The Contents API file `sha` is object-version protection for that file, not branch-head CAS.

## 11. Zero-schema authority cannot become mechanically strong while broad insert remains shared

Current coordination rows contain textual `source_branch`/payload authority claims. The ordinary service principal has INSERT capability.

If multiple logical actors share the same broad database principal, **there is no zero-schema magic field that turns `source_branch='Voss'` into database-verifiable Voss authorship.**

Payload `authority_ref`, `issuer`, `workload_lane_key`, or similar values are evidence only when the writer can forge them.

Mechanical strengthening requires at least one independently trusted admission property, such as:

- dedicated least-privilege writer identities/routes whose database identity is server-bound;
- a narrowly exposed canonical writer RPC/service that derives issuer from its trusted route rather than request payload;
- a verifiable signed admission envelope whose signing capability is unavailable to ordinary writers;
- future schema/service controls that bind actor/operation identity and authorization.

Those can potentially reuse existing table columns/payload shape, but they are not achieved merely by defining a new JSON contract.

For zero-schema **proof mode**, authority remains route/policy-bound and must be reported as such.

## 12. Transition validation is as important as snapshot validation

A complete `state_after` snapshot helps resolution, but a malicious/buggy writer could submit an impossible transition.

Versioned policy should validate relation-specific constraints, for example:

- `COMPLETE` -> `assignment_state=NON_CURRENT`, `terminal_disposition=COMPLETE`;
- `CANCEL` -> terminal CANCELLED;
- `DEPENDENCY BLOCK` -> assignment may remain CURRENT, blocking DEPENDENCY_BLOCKED, floor contribution false;
- `TERMINAL BLOCK` -> NON_CURRENT/terminal;
- `RELEASE` -> clears only a compatible dependency block and does not resurrect a completed/cancelled generation;
- `REACTIVATE` -> explicit authority, creates a new active generation/state successor without rewriting prior terminal history;
- `REROUTE` -> owner change rules explicit; whether lane/root is preserved depends on same-objective versus new-root replacement semantics.

The resolver should never trust `state_after` merely because its enum values are syntactically valid.

## 13. Review/ACK semantics need a normalization rule

The existing 3298 -> 3362 chain proves that current history sometimes closes assignment state through review/ack payload semantics without a direct assignment supersession edge.

V1 must stop exporting that archaeology.

Going forward:

- REVIEW/ACK/EVIDENCE records may exist outside the state chain;
- if one changes assignment state, the trusted admission/controller emits a normalized `ASSIGNMENT_EVENT_V1` state successor;
- the assignment resolver reads only the normalized state chain for currentness, while audit/debug can traverse the underlying review/evidence references.

Without this rule, every new review schema becomes another assignment-currentness adapter forever.

## 14. Hostile cases added after peer challenge

1. Two root ASSIGN events in same conforming thread -> CONFLICTED.
2. Successor points to predecessor from another assignment root -> CONFLICTED.
3. Two concurrent state changes based on same predecessor -> one accepted, second must reread/re-adjudicate, never blind retry.
4. COMPLETE row whose `state_after` still says CURRENT -> invalid transition / UNKNOWN-CONFLICTED.
5. Dependency BLOCK marked terminal -> schema/policy conflict.
6. RELEASE after COMPLETE -> does not resurrect.
7. REACTIVATE after terminal -> explicit new active successor, old terminal history preserved.
8. Review says approved but no normalized state successor exists -> state chain remains unchanged / source incomplete if review is known to be authoritative and normalization pending.
9. Same objective amendment tries to mint new workload key -> ignored/rejected; root identity controls.
10. Provisional Slack lane and later canonical lane lack bridge -> zero duplicate floor credit.
11. Two independent objectives incorrectly bridged to one root -> conflict/admission defect, not semantic resolver guess.
12. Payload claims Voss authority under shared service principal -> not self-authenticating.
13. Fresh resolver receipt + GitHub ref moved to unexpected ancestor of candidate -> REST fast-forward may succeed; strict effect policy must still reject absent exact expected-head CAS.
14. GitHub ref already at candidate due another writer -> idempotent content state may exist, but operation attribution/lease reconciliation required before claiming our effect.
15. MAX event_sequence unchanged but previously uncommitted lower identity row becomes visible -> pre-effect full lineage re-resolution catches it.
16. Multi-source adapters all succeed but authority registry omitted Slack provisional surface -> `source_completeness` cannot be COMPLETE.

## 15. Smallest coherent V1 contract

### Input

Typed assignment root/thread identity, requested action class, trusted effective actor/scope from route, optional present-authority event already speech-act/admissibility adjudicated.

### Internal resolution

1. determine authoritative surface registry/version;
2. gather conforming canonical state chain and permitted provisional/present authority surface when current mode requires it;
3. validate root uniqueness, predecessor continuity, relation/state transition consistency, authority admission, and source completeness;
4. derive root lane identity;
5. return assignment facts independently from action eligibility;
6. for external effects, invoke provider adapter with required precondition strength and post-effect readback.

### Output sketch

```json
{
  "resolution_status": "RESOLVED|SOURCE_INCOMPLETE|CONFLICTED|UNKNOWN|UNAVAILABLE",
  "assignment_state": "CURRENT|NON_CURRENT|UNKNOWN",
  "blocking_state": "NONE|DEPENDENCY_BLOCKED|TERMINAL_BLOCKED|UNKNOWN",
  "authority_binding_state": "NOT_REQUIRED|VALID|STALE|REVOKED|CONSUMED|UNKNOWN",
  "artifact_binding_state": "NOT_REQUIRED|VALID|STALE|UNKNOWN",
  "terminal_disposition": "NONE|COMPLETE|CANCELLED|SUPERSEDED|REROUTED_AWAY|TERMINALLY_BLOCKED|UNKNOWN",
  "workload_lane_id": "<root ASSIGN event id or provisional bridged identity>",
  "action_eligibility": "ALLOWED|BLOCKED|UNRESOLVED",
  "block_reason_codes": [],
  "source_mode": "...",
  "source_completeness": "...",
  "consistency": "...",
  "freshness": "...",
  "policy_version": "...",
  "adapter_registry_version": "...",
  "authority_surface_registry_version": "...",
  "controlling_event_ids": [],
  "max_visible_event_sequence": 3382,
  "receipt_digest": "..."
}
```

## Final position

The peer challenges improved the design.

- **Accept** the linear normalized assignment-state chain for V1, provided `supersedes_event_id` is explicitly state-predecessor semantics inside the versioned assignment envelope and transition validation is strict.
- **Prefer** root ASSIGN event ID as canonical workload-lane identity over a self-declared key.
- **Keep** assignment currentness, blocking, authority, artifact binding, source completeness, and provider-target freshness separate.
- **Reject** any claim that REST fast-forward ref update equals exact expected-head CAS.
- **Reject** any zero-schema claim of strong logical-actor authentication while a shared broad writer can forge textual issuer fields.
- **Correct** V1's mistaken caller-supplied `event_sequence` statement; it is GENERATED ALWAYS identity, but still not a commit-completeness watermark.

No producer branch, hosted database state, native Project file, deployment, credential, paid service, or canonical memory was modified by this research artifact.