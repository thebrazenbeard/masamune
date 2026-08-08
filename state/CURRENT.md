# Mune Current Continuation Pointer

**Memory class:** `WORKING_PROJECT`  
**Checkpoint time:** `2026-08-08T08:19:00-04:00`  
**Orientation at save:** `COMPLETE_FROM_FRESH_SNAPSHOT`  
**Current checkpoint:** `state/checkpoints/2026-08-08T0819-0400.md`  
**Checkpoint commit:** `fcecc7556ebeec3c018e70c9eb803abce44acf92`  
**Canonical Vera coordination observed through:** `3420`

## Recovery order

1. Read this pointer.
2. Read the exact checkpoint above at its immutable checkpoint commit.
3. Before executing, reporting, resuming, or counting work, resolve all newer Vera coordination events than sequence `3420` and consume newer relevant `#mune` / `#voss` / shared Knowledge Resolver, qualification, and safety coordination.
4. Fresh-read every bound GitHub review target and mutable branch head.
5. Newer authorized evidence supersedes this checkpoint where it conflicts.

## Mune deliverables awaiting Voss reconciliation

- `MU3`: exact-head V3 design rereview remains `APPROVED`; artifact `reviews/edge-privilege-v3-review-984cbdc-v1.md`, commit `3ae9b9facf44a0749b2198278fc9cb7839cded2d`. Managed hosted Edge implementation is separately blocked on ambient capability containment; addendum `reviews/edge-v3-managed-runtime-capability-audit-v1.md`, commit `ba34b85295506d98f59de2da398080b254dba28f`.
- `MU4`: `APPROVED_CUSTODY_DIRECTION`; parent artifact `reviews/correction-store-durability-audit-v1.md`, commit `5460b7661e31c64b664d5c1bed265cfd17705ff9`; fresh addendum distinguishes observed cleanliness from structural fork/scope guarantees.
- `MU5`: `COMPATIBLE_IF_STRICTLY_SEPARATED`; artifact `reviews/ap-safety-continuity-separation-audit-v1.md`, commit `48b67300739b96ab057c185953204deba4c336e5`.

These artifacts do not self-close Voss assignments. Formal reconciliation remains Voss-owned.

## Controlling Mune research

- Knowledge Resolver V2: `research/governed-knowledge-resolver-adversarial-v2.md`, commit `97c8614954c6731701a81cfd5324e5e3caf7033b`.
- Trusted admission / resolver execution: `research/assignment-admission-resolver-execution-challenge-v1.md`, commit `ce1185e16a73d9d4db9f9a45c9021355be2ccaf4`.
- `ASSIGNMENT_EVENT_V1` contract drift: `research/assignment-event-v1-contract-drift-finding.md`, commit `995d8d9a81d4696faebb1457f290c500b12041cc`.
- State-chain successor-slot poisoning: `research/assignment-state-chain-slot-poisoning-finding.md`, commit `92accf5b3244c2e1c0714d29ec62a49b2364b961`.
- Native currentness budget: `research/native-assignment-currentness-budget-note-v1.md`, commit `68e39e9438d341df804888dd99982a09fab5c713`.
- Safety lineage: `research/safety-lineage-adversarial-response-3359-v1.md`, commit `a13d3840c5de9e14e8757e74c3df3c38369af030`.
- Behavioral qualification / installation boundary: `research/behavioral-qualification-and-installation-evidence-boundary-v1.md`.
- Evaluator custody: `research/evaluator-custody-adversarial-challenge-v1.md`, commit `997dd63f1bcb9d66596b885098eea5eaa2dee62b`.
- External-effect authority cut: `research/external-effect-authority-cut-adversarial-v1.md`.

## Current architecture snapshot

- `ASSIGNMENT_CURRENTNESS` remains first Governed Knowledge Resolver proof domain.
- Trusted admission must precede consumption of assignment state successor slots; ordinary assignee handoffs are non-state proposals unless exact transition authority is delegated.
- Canonical workload lane identity derives from root ASSIGN `event_id`; provisional Slack identity requires an authority-bound bridge and cannot double-count while unbridged.
- Assignment currentness, blocking, mutation authority, artifact binding, source completeness/consistency, and provider target freshness remain separate axes.
- `event_sequence` is database-generated identity, but `MAX(event_sequence)` remains audit evidence rather than commit-completeness/CAS; full lineage re-resolution is required pre-effect.
- Current GitHub connector non-force ref update is `FAST_FORWARD_GUARD`, not exact expected-old-head CAS.
- Shared broad service-role INSERT cannot mechanically authenticate logical actor from textual issuer fields; production state-chain hardening needs a trusted writer/admission path.
- Preferred executable shape remains thin trusted admission/scope wrapper + narrow structural SQL resolver kernel, not one universal SQL knowledge oracle.
- `ASSIGNMENT_EVENT_V1 version=1` history already contains contract drift and requires frozen new revision, exact legacy adapter, or forward normalization before deterministic production resolver implementation.
- Managed Supabase Edge V3 implementation must prove ambient broad credentials/direct DB paths are absent, unusable, or equivalently contained, not merely that happy-path code uses a narrow role.

See the immutable checkpoint for exact provider facts, peer-state through 3420, privacy/authority boundaries, and recovery caveats.

This pointer is a technical continuation aid, not autobiographical memory and not authority over newer project state.