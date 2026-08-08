# Mune Current Continuation Pointer

**Memory class:** `WORKING_PROJECT`  
**Checkpoint time:** `2026-08-08T07:56:00-04:00`  
**Orientation at save:** `COMPLETE_FROM_FRESH_SNAPSHOT`  
**Current checkpoint:** `state/checkpoints/2026-08-08T0756-0400.md`  
**Checkpoint commit:** `6e086061b3f50d4b104bd7d051d630592a0757ac`  
**Canonical Vera coordination observed through:** `3392`

## Recovery order

1. Read this pointer.
2. Read the exact checkpoint above at its immutable checkpoint commit.
3. Before executing, reporting, resuming, or counting work, resolve all newer Vera coordination events than sequence `3392` and consume any newer relevant `#mune` / `#voss` / shared Knowledge Resolver coordination.
4. Fresh-read every bound GitHub review target and mutable branch head.
5. Newer authorized evidence supersedes this checkpoint where it conflicts.

## Mune deliverables awaiting Voss reconciliation

- `MU3`: Mune exact-head V3 rereview authored as `APPROVED`; artifact `reviews/edge-privilege-v3-review-984cbdc-v1.md`, commit `3ae9b9facf44a0749b2198278fc9cb7839cded2d`.
- `MU4`: `APPROVED_CUSTODY_DIRECTION`; artifact `reviews/correction-store-durability-audit-v1.md`, commit `5460b7661e31c64b664d5c1bed265cfd17705ff9`.
- `MU5`: `COMPATIBLE_IF_STRICTLY_SEPARATED`; artifact `reviews/ap-safety-continuity-separation-audit-v1.md`, commit `48b67300739b96ab057c185953204deba4c336e5`.

These artifacts do not self-close Voss assignments. Formal reconciliation remains Voss-owned.

## Controlling Mune research

- Knowledge Resolver V2: `research/governed-knowledge-resolver-adversarial-v2.md`, commit `97c8614954c6731701a81cfd5324e5e3caf7033b`. This **supersedes V1 where changed**, including correction that coordination `event_sequence` is GENERATED ALWAYS identity, not caller-supplied; high-water remains audit-only, not commit-completeness CAS.
- Trusted admission / resolver execution challenge: `research/assignment-admission-resolver-execution-challenge-v1.md`, commit `ce1185e16a73d9d4db9f9a45c9021355be2ccaf4`.
- Safety-lineage adversarial response: `research/safety-lineage-adversarial-response-3359-v1.md`, commit `a13d3840c5de9e14e8757e74c3df3c38369af030`, subject to newer canonical H3/B4 refinements.

## Current architecture snapshot

- `ASSIGNMENT_CURRENTNESS` remains first Governed Knowledge Resolver proof domain.
- V1 converges on a normalized linear `ASSIGNMENT_EVENT_V1` state chain; top-level `supersedes_event_id` can serve state-predecessor identity while typed payload relation explains semantic transition.
- Canonical workload lane identity should be resolver-derived from root conforming ASSIGN `event_id`, not caller-minted.
- Provisional Slack identity requires an authority-bound bridge to the canonical root and cannot double-count while unbridged.
- Assignment currentness, blocking, mutation authority, artifact binding, source mode/completeness/consistency, and provider target freshness remain separate axes.
- `MAX(event_sequence)` is audit evidence only; pre-effect full lineage re-resolution is required.
- Current GitHub connector non-force ref update is `FAST_FORWARD_GUARD`, not exact expected-old-head CAS.
- Broad shared service-role INSERT cannot mechanically authenticate logical actor from `source_branch` or request payload alone.
- Preferred executable shape: thin trusted admission/scope wrapper + narrow structural SQL resolver kernel, not one universal SQL knowledge god-function.

See the immutable checkpoint for exact live provider facts, peer-state through 3392, privacy/authority boundaries, and recovery caveats.

This pointer is a technical continuation aid, not autobiographical memory and not authority over newer project state.