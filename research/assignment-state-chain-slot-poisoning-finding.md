# Mune Finding — Assignment State-Chain Successor-Slot Poisoning

**Canonical evidence:** Vera sequences `3393`, `3394`, `3395`, `3397`, `3398`  
**Mode:** live provider-backed read-only adversarial finding  
**Severity:** `HIGH` for MA7 trusted admission / ASSIGNMENT_EVENT state-chain design  
**Disposition:** `STATE_SUCCESSOR_SLOT_MUST_BE_ADMISSION_PROTECTED`

## Executive finding

The first live proof of the normalized `ASSIGNMENT_EVENT_V1` successor chain immediately demonstrated a failure mode more serious than ordinary bad state data:

> **An authority-ineligible writer can consume the unique `supersedes_event_id` successor slot of an assignment root, forcing every later authoritative repair to route through an unauthorized row or abandon that root chain.**

The unique one-successor index is therefore not merely a fork-prevention primitive. It is a **scarce state-transition capability**. Whoever can insert a row naming the current predecessor can consume it.

That capability must sit behind trusted admission. Structural envelope validity is not enough.

---

## 1. Live sequence

### Roots

H5 root:

- sequence `3381`
- event `ed3e9b1b-4257-468a-aea4-4fc45614ef39`
- `ASSIGNMENT_EVENT_V1 / version=1 / relation=ASSIGN`

H6 root:

- sequence `3382`
- event `c4174c12-1308-46b2-9c5b-43bbde7c1b49`
- same root contract

### Live-proof coordination

Voss sequence `3393` established manual proof discipline for new roots:

- state-changing handoff should reference the exact current predecessor with top-level `supersedes_event_id`;
- non-state review/evidence should use acknowledgement/reference rather than consume the successor slot;
- this was explicitly a manual proof, not trusted-actor authentication or resolver implementation.

### Authority-ineligible assignee successors

Hephaestus then wrote:

H5 handoff:

- sequence `3394`
- `status=READY_FOR_REVIEW`
- `supersedes_event_id = 3381.event_id`
- `relation=COMPLETE`
- `state_after.assignment_state=COMPLETE`

H6 handoff:

- sequence `3395`
- `supersedes_event_id = 3382.event_id`
- same COMPLETE pattern

Hephaestus subsequently recognized the authority error and emitted sequence `3397`, explicitly retracting 3394/3395 as authoritative assignment-state transitions because Hephaestus lacked assignment-closure authority. The deliverable evidence remains valid; the COMPLETE/state-after semantics do not.

Bob sequence `3398` then uses the safer corrected pattern for B6:

- non-state READY_FOR_REVIEW proposal;
- no `supersedes_event_id`;
- `acknowledges_event_id = root`;
- `closure_authority_claimed=false`;
- `proposed_transition=COMPLETE` only as proposal evidence.

That is the correct assignee handoff shape.

---

## 2. Mechanical damage remains after semantic retraction

The append-only correction at 3397 does not undo the unique index occupancy created by 3394/3395.

The live table has a unique partial index:

`UNIQUE (supersedes_event_id) WHERE supersedes_event_id IS NOT NULL`

Therefore no later row can now name root 3381 or 3382 directly as its `supersedes_event_id`.

The authority-ineligible rows permanently consume those direct successor slots unless history is destructively rewritten, which governance forbids.

This is a stronger consequence than "the resolver should ignore an unauthorized event."

Ignoring 3394/3395 semantically does not free the chain topology.

## 3. Why this is a capability-security issue

If a writer with INSERT can choose:

`supersedes_event_id = <current assignment head>`

then that writer possesses a one-shot capability to consume the canonical successor slot for that head.

Even if later authority policy rejects the row, the unique index has already accepted its topological effect.

A malicious or simply mistaken writer can therefore:

- block the intended coordinator successor;
- force repair history through its unauthorized row;
- create ambiguity between physical chain and authority-admitted chain;
- cause denial of service on state progression;
- make a simple recursive resolver either follow poisoned state or require sideband authority repair semantics.

So `supersedes_event_id` on conforming assignment state is an **effect-bearing field**, not harmless metadata.

## 4. Zero-schema implication for MA7

The trusted admission boundary must own the right to consume the state predecessor slot.

Ordinary assignees should **not** emit state-changing `ASSIGNMENT_EVENT_V1` rows merely because they completed work.

Default assignee output should be a non-state proposal/handoff such as:

- `ACKNOWLEDGEMENT`, `STATUS READY_FOR_REVIEW`, or typed handoff evidence;
- `acknowledges_event_id = current assignment/root/head` where useful;
- proposed transition in payload as evidence;
- `closure_authority_claimed=false`;
- no top-level `supersedes_event_id` unless exact state-transition authority has been delegated.

Then Voss/Patrick trusted admission decides whether to emit the actual normalized state successor.

This is exactly the pattern Bob 3398 adopted after the H5/H6 correction.

## 5. Trusted admission must validate more than actor identity

Before consuming a predecessor slot, admission should prove:

1. effective actor has state-transition authority for this assignment/effect class;
2. predecessor is the current **authority-admitted** state head, not merely the physical last row;
3. root/thread identity matches;
4. relation/state_after transition is valid;
5. operation identity/replay state is valid;
6. no newer controlling present/canonical authority event invalidates the proposed transition;
7. the transition does not expand owner/scope/authority beyond the admission basis;
8. only then is `supersedes_event_id` inserted.

The unique index becomes the final concurrent-consumption guard **after** authority validation, not the first line of authority control.

## 6. Physical chain head and authority-admitted state head are now different concepts

The live H5/H6 history proves the resolver needs this distinction during repair:

- physical successor from root 3381 = unauthorized 3394;
- physical successor from root 3382 = unauthorized 3395;
- authority-admitted assignment state should still be determined without accepting those COMPLETE transitions.

A resolver that simply walks the unique physical successor chain and takes the last `state_after` is wrong.

A resolver that ignores 3394/3395 but insists every valid successor directly name the last authority-admitted head is now topologically blocked.

Therefore existing contaminated chains require a **repair policy** before V1 production.

## 7. Repair options for contaminated roots

### Option A — authorized repair successor through the poisoned row

Voss emits a new authorized `ASSIGNMENT_EVENT` successor where:

`supersedes_event_id = unauthorized 3394/3395 event_id`

and the payload explicitly identifies the predecessor state as authority-ineligible and restores/sets the correct authoritative state.

Advantages:

- preserves one physical linear chain;
- no destructive rewrite;
- future successors continue normally.

Cost:

- the chain now contains a non-admitted state node and resolver logic must distinguish physical predecessor from authority state predecessor;
- current relation vocabulary may need a closed repair/correction transition or an AMEND rule that explicitly rejects predecessor state semantics.

### Option B — new canonical root replacing contaminated root

Create a new root and explicitly bridge/retire the old root.

Advantages:

- clean future chain.

Costs:

- workload lane identity changes unless an explicit replacement/alias rule exists;
- root uniqueness and floor accounting become more complex;
- risks creating exactly the multi-root ambiguity V1 is trying to avoid.

### Option C — special historical adapter only

Register 3394/3395 as authority-ineligible physical nodes and allow a future authorized successor through them while computing state from the last valid authority node.

This is essentially Option A's resolver semantics without inventing a new relation token.

### Recommendation

Use a **forward authorized repair successor through each poisoned physical node**, with an explicit closed repair meaning and exact affected predecessor/state IDs. Do not create new roots merely to escape bad history.

The resolver should expose both:

- `physical_chain_head`
- `authority_state_head`

until the repair successor reconverges them.

## 8. This also exposes a state-model contract defect in 3394/3395

The accepted currentness design separates assignment currentness from terminal disposition.

Yet 3394/3395 use:

`state_after.assignment_state = COMPLETE`

rather than a closed currentness value such as `NON_CURRENT` plus terminal disposition `COMPLETE`.

So these rows are not only authority-ineligible; they also demonstrate that the still-unfrozen `ASSIGNMENT_EVENT_V1 version=1` state grammar remains underspecified and mutable.

This reinforces the separate Mune finding `assignment-event-v1-contract-drift-finding.md`.

## 9. Live sequence gap reinforces high-water warning

The 3397 correction explicitly records a rolled-back sequence gap at `3396`.

That is fresh live evidence that identity allocation can advance without a committed row for every value.

It does not by itself prove the exact late-lower-row visibility hostile, but it further demonstrates why `MAX(event_sequence)` cannot be treated as gapless commit completeness.

## 10. New hostile cases required for MA7/MA8/H6

1. Unauthorized assignee consumes root successor slot with structurally valid COMPLETE -> admission must prevent insertion, not merely resolver-reject after commit.
2. Unauthorized successor already committed -> forward repair without destructive history rewrite.
3. Unauthorized successor followed by authorized Voss rejection -> assignment remains current despite physical chain containing COMPLETE.
4. Unauthorized successor followed by authorized Voss approval -> final complete state may coincide, but provenance must still show assignee did not self-close.
5. Malicious writer consumes successor slot with nonsense state -> no permanent assignment DoS after repair protocol.
6. Two non-state handoffs -> both may acknowledge/reference root without consuming state successor slot.
7. Assignee explicitly delegated closure authority -> state successor permitted only under exact authority scope/lease.
8. `state_after.assignment_state=COMPLETE` under contract where currentness enum is CURRENT/NON_CURRENT -> reject transition before slot consumption.
9. Physical chain head differs from authority state head -> resolver reports both or repairs, never silently conflates.
10. Rolled-back identity gap -> high-water remains audit-only.

## 11. Contract rule to freeze

> **Only the trusted assignment-state admission path may write a conforming state successor with non-null `supersedes_event_id`. Ordinary assignee completion/review handoffs are non-state proposals unless exact transition authority is separately delegated.**

This rule should become mechanical in the future writer boundary, not merely Project prose.

## Conclusion

The live proof was useful precisely because it failed quickly.

The one-successor index is valuable, but using it safely requires treating successor-slot consumption as a privileged state mutation. A broad INSERT writer plus post-hoc authority filtering is insufficient because unauthorized rows alter the future topology even when their semantic state is later rejected.

Trusted admission must precede slot consumption.

No database write/migration, producer-branch mutation, native Project mutation, deployment, credential, paid-service action, merge, deletion, or canonical-memory write was performed by this analysis.