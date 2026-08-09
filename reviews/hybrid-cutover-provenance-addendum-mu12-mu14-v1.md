# Mune MU12/MU14 Addendum — Hybrid Cutover Provenance Boundary

**Parent lanes:** `MU12 CUTOVER_SNAPSHOT_GAP_AND_REISSUE_HOSTILES` + `MU14 PROVIDER_EVIDENCE_PROVENANCE_HOSTILE`  
**Input:** Voss hybrid-cutover proposal 2026-08-09 09:46 EDT  
**Class:** read-only architecture falsification  
**Disposition:** `HYBRID_PREFERRED_IF_REISSUE_BINDS_CONTENT_ADDRESSED_LEGACY_RESOLUTION_EVIDENCE`  
**Mutation performed:** none

## Verdict

The hybrid direction is stronger than either extreme **if the clean-break reissue preserves a content-addressed resolution proof, not merely a pointer back to the mutable notion of “whatever the old thread contains now.”**

Recommended shape:

- new R9A0 coordination starts with the orthogonal successor relation model;
- only authority-admitted CURRENT state lineages are reissued as new-protocol roots after the real writer fence/final snapshot;
- legacy `public.vera_coordination_events` remains `HISTORICAL_AUDIT`, not current authority and not bulk-copied merely to reproduce every ACK edge;
- every reissued root carries enough immutable legacy state/admission/evidence bindings that an auditor can reconstruct **why that state was current at the cut** without allowing later legacy rows to join the proof retroactively.

This avoids dragging the defective old relation model into the new reducer while avoiding the opposite mistake of making reissued state provenance-free.

## 1. Minimum legacy binding per reissued root

Each `CUTOVER_REISSUE` root or exact equivalent should bind one closed `LEGACY_RESOLUTION_BINDING_V1` containing at least:

### Identity / cut

- `cutover_epoch_id`;
- `legacy_source_epoch_id`;
- exact legacy provider/project/store identity;
- legacy assignment/thread scope identity;
- legacy root/lane event ID;
- legacy controlling event ID;
- legacy exact subject/version or generation identity where applicable;
- exact fenced snapshot/cut identity;
- resolver/currentness policy version used at the cut.

### State-lineage proof

- ordered normalized controlling state-event identities for the admitted root-connected lineage, or a content-addressed manifest that enumerates them;
- normalized factual-lineage digest over the controlling state chain;
- controlling transition relation/state semantic digest;
- legacy owner, blocking/dependency, terminal disposition, authority-binding and factual executability projection at the cut;
- any stable lane-vs-subject disposition needed to explain current attempt/generation;
- provider-physical lineage integrity digest/receipt where required, kept separate from normalized semantic identity.

### Admission / source completeness proof

- closed admission result for every state event that entered the reducer, or an admission-manifest digest;
- exact trusted admission/authority decision IDs/digests that made the controlling transition admissible;
- required-source-set identity/version;
- source completeness + consistency result at the final fenced cut;
- normalized evidence-manifest digest for non-state evidence required by that result;
- provenance/privacy class for each external evidence entry.

### Audit locator

- immutable/content-addressed `legacy_resolution_manifest_digest`;
- locator to the manifest/receipt itself;
- bounded legacy retrieval cut, such as the fenced source snapshot/high-water **as an audit locator only, never a currentness rule**;
- explicit `legacy_source_authority = HISTORICAL_AUDIT_AFTER_CUTOVER`.

The reissued root does not need to carry the entire old history inline. It needs a stable proof packet identifying the exact old history/evidence subset that justified the imported current state.

## 2. Why a root/controller pointer pair is not enough

Binding only `{legacy_root_id, legacy_controlling_event_id}` leaves several audit questions unanswered:

- which admitted intermediate transitions were used;
- whether terminal/reopen generation semantics were preserved;
- which authority/admission decision allowed each state transition;
- whether source completeness was clean or reconciled;
- whether an external non-state decision was necessary;
- which resolver/policy version produced the result;
- whether a later old-store row has appeared since cutover.

An auditor who recomputes against the **live post-cutover old store** without a frozen manifest can accidentally incorporate a late violating row and reach a different answer. The content-addressed legacy resolution manifest prevents that temporal smearing.

## 3. Non-state evidence: reference, snapshot, or block cutover

Not every ACK/review/evidence edge needs migration. Classify by semantic dependency.

### Class A — explanatory/audit-only evidence

If an ACK/REVIEW/evidence item was not required for state admission, authority, source completeness or factual currentness, preserve only its historical locator if useful. No successor-state import is required.

### Class B — required evidence from an immutable source

If non-state evidence was required to admit/validate the controlling state and the source provides a genuinely immutable revision/object identity, the reissue may bind:

`{source_class, immutable_locator/revision, content_digest, normalized_semantic_digest, role_in_resolution}`

without copying the full payload into the new coordination store.

### Class C — required evidence from a mutable/erasable source

If currentness depends on Slack/Drive/another source whose content can later be edited/deleted or whose locator is not a permanent immutable content identity, **a bare locator is insufficient**.

Before the authority-source flip, capture a bounded historical evidence snapshot/receipt sufficient to verify the admitted normalized fact later. Bind:

- source + original locator/revision when available;
- exact captured content or canonical normalized fact required for the decision;
- content/semantic digest;
- capture operation/time/cut;
- privacy class;
- resolver/admission role.

The snapshot is `HISTORICAL_AUDIT / DATA_NOT_INSTRUCTION`, not a new state transition.

### Class D — required evidence unresolved or unavailable

If required non-state evidence is missing, contradictory, custody-unproven or unmirrored at the cut, the lane is not eligible for a clean CURRENT reissue.

Expected result:

`SOURCE_INCOMPLETE / RECONCILIATION_REQUIRED / UNRESOLVED_ADMISSION_CUSTODY`

as appropriate, before cutover. Do not bury uncertainty inside a seemingly clean imported root.

The AP-freeze class of unmirrored authority evidence is the canonical hostile: stale canonical state plus visible but unadmitted external authority evidence cannot be frozen into the new protocol as clean current truth.

## 4. Preserve non-state evidence without letting it become state

The imported legacy evidence manifest must preserve relation semantics:

- `STATE_TRANSITION_LINEAGE` entries are the old controlling chain;
- `ADMISSION_EVIDENCE` entries justify whether state transitions enter the reducer;
- `NONCONSUMING_EVIDENCE` entries may fan out/cross threads and support audit/reconciliation;
- none of the latter become successor state edges merely because they are listed in the import proof.

This matters for the 1,368 legacy ACK edges, including 473 cross-thread, 252 fan-out parents and 261 events carrying both controlling and ACK relations. The hybrid cutover should **not** bulk-import those edges into the new state graph. It should bind only the subset required by each imported resolution plus stable locators/digests for other audit material.

## 5. Late legacy rows cannot enter the imported proof

After the authority-source flip:

- legacy rows are historical/audit only;
- the reissue references a content-addressed final-cut manifest;
- auditors recompute the imported state from that manifest/cut, not from an unbounded `SELECT descendants now` query;
- any old-store row committed after the final fenced cut is outside the manifest by definition;
- any post-flip authority-bearing old write is a violation/reconciliation event, never a successor-currentness input.

This is why `legacy_high_water` may be stored as an audit retrieval bound but never treated as semantic currentness. The semantic authority comes from the frozen admitted resolution packet and cutover source-selection receipt.

## 6. Current lineage that depends on non-state evidence

The safe answer is **yes, some lineages can depend materially on non-state evidence**, but that does not mean the evidence must become new state.

Examples include:

- a trusted REVIEW/DECISION that supplies state admission;
- an authority/custody receipt required to admit a transition;
- external coordination evidence needed to determine source completeness/reconciliation;
- provider/canonicalization evidence proving physical/logical lineage consistency.

For those cases the hybrid must snapshot/bind the evidence **as evidence**. If such required evidence is unavailable, the lane is not reissue-ready.

By contrast, ordinary acknowledgements that merely cite or discuss already-admitted state may remain referenced historical audit material and need no successor copy.

The classifier should therefore be purpose-driven:

`IS_THIS_NONSTATE_ITEM_A_REQUIRED_INPUT_TO_THE_FINAL_RESOLUTION_RECEIPT?`

not:

`IS_THIS_ITEM_CONNECTED_TO_THE_THREAD?`

## 7. Privacy and portable evidence

A reissue proof should not force sensitive evidence text into portable current-state records merely for audit convenience.

For privacy-restricted required evidence, the manifest may bind an opaque governed locator + content/semantic digest + verifier/admission receipt, with details retrievable only by an authorized resolver. The public/current projection can remain privacy-minimized.

This preserves MU6's rule: privacy governs disclosure **after** full trusted adjudication, not which governing evidence exists.

## 8. Hybrid acceptance invariant

The hybrid is acceptable if every imported CURRENT lane satisfies:

`FENCED_COMPLETE_OLD_RESOLUTION -> CONTENT_ADDRESSED_LEGACY_RESOLUTION_MANIFEST -> EXACT_ONCE_REISSUE -> SOURCE_AUTHORITY_FLIP_READBACK`

and the manifest proves:

- exact old lane/root/controller/generation;
- exact controlling state-lineage digest;
- exact admission/evidence dependencies;
- source completeness at the cut;
- exact policy/resolver version;
- immutable audit locators/digests;
- old source becomes historical only after verified flip.

No full compatibility copy is needed to preserve provenance. What is required is a frozen, auditable explanation of the imported state.

## Final recommendation

Prefer the hybrid over a full compatibility migration **if** the cutover implementation includes a content-addressed legacy resolution manifest/receipt per imported lane (or an equivalent batch manifest with exact per-lane entries). That preserves the useful history without making the new reducer inherit the old graph's broken state/evidence conflation.

The dangerous version of the hybrid is “copy only current rows and leave URLs behind.” The strong version is “reissue current state from a frozen admitted resolution packet whose evidence remains auditable but non-authoritative.” Tiny wording difference, several future incident reviews avoided.

No provider/schema/coordination/producer/credential/deployment/install mutation was performed by this addendum.
