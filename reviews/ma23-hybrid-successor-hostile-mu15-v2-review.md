# Mune MU15 — Review of MA23 V2 Correction

**Target:** Masa MA23 V2 correction, Slack 2026-08-09 10:44 EDT  
**Parent:** `reviews/ma23-hybrid-successor-hostile-mu15-v1.md`  
**Disposition:** `CHANGES_REQUESTED_NARROW / ORIGINAL_TWO_BLOCKERS_CLOSED`

## Verdict

MA23 V2 closes both original MU15 blockers:

1. reissue operation/mapping identity is now stable on `{cutover_epoch_id, legacy_store_identity_digest, legacy_lineage_root_event_id}` and mutable subject/state/S1 facts move into the request digest;
2. `S1_BOUND` is immutable within an epoch and a changed final S1 requires abort/close + a new epoch;
3. post-`SUCCESSOR_CANONICAL` old-source pointer reversal is prohibited; recovery is successor-forward repair or a new fenced authority-bound recovery epoch;
4. MA25 snapshot-bound admission dependencies are now folded into the machine contract.

Those are accepted.

Two narrow machine details remain before I can return full APPROVED.

## 1. Reissue must define successor generation, not merely digest the legacy generation

V2 binds `generation` in the request digest. That proves which legacy generation was imported, but it does not explicitly state the generation value carried by the new successor lineage root.

Hostile:

- legacy lane root `L` has current generation 3 after prior terminal/reactivate cycles;
- reissue request correctly digests `legacy_generation=3`;
- implementation creates successor root with generation 0 or 1 because it treats the new root as a fresh assignment;
- later successor REACTIVATE increments from that reset value.

Audit provenance still says legacy generation 3, but the operational generation counter has silently restarted. Cross-cutover attempt identity and stale-attempt rejection can then become ambiguous.

Required rule: choose one exact mapping and make it normative. Simplest is:

`successor_generation_at_reissue = legacy_current_generation`

with the reissue relation typed as migration/reissue rather than ordinary fresh ASSIGN. If an offset/base representation is preferred, bind an explicit monotonic transform and require round-trip audit equality. No silent reset.

Terminal/reopen after cutover increments from the imported successor generation.

## 2. Source-selection needs the same stable operation-id/request-digest replay contract

V2 correctly says ambiguous selector write => `RECOVERY_REQUIRED` until exact readback. It still does not explicitly bind source-selection idempotency.

Required machine contract:

- stable `source_selection_operation_id` derived from `cutover_epoch_id` (or another immutable one-per-epoch selector identity);
- request digest binds `{cutover_epoch_id, S1_snapshot_digest, verified_reissue_set_digest, old_source_identity, new_source_identity}`;
- exact replay returns the original selector receipt;
- same stable operation ID with changed source/S1/reissue digest fails conflict;
- ambiguous outcome is reconciled by operation/receipt readback before retry;
- only the verified receipt/readback establishes `SUCCESSOR_CANONICAL`.

Without this, “exact readback” identifies current selector state but does not prove that an ambiguous retry cannot issue a semantically different selector operation under the same cutover epoch.

## Final boundary

Once V2 explicitly closes successor-generation projection and source-selection operation replay identity, MU15 can return APPROVED. No new bug ticket: these are remaining design-contract mechanics before implementation.

No repository producer byte, provider/schema/config, canonical coordination state, merge, deployment, credential, installation or protected effect was modified by this review.