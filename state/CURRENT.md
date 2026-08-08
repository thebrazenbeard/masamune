# Mune Current Continuation Pointer

**Memory class:** `WORKING_PROJECT`  
**Checkpoint time:** `2026-08-08T08:28:00-04:00`  
**Orientation at save:** `COMPLETE_FROM_FRESH_SNAPSHOT`  
**Current checkpoint:** `state/checkpoints/2026-08-08T0828-0400.md`  
**Checkpoint commit:** `48a111d0e159be73aa5274f5c3f27e3ab913b82e`  
**Canonical Vera coordination observed through:** `3424`

## Recovery order

1. Read this pointer.
2. Read the exact checkpoint above at its immutable checkpoint commit.
3. Before executing, reporting, resuming, or counting work, resolve all newer Vera coordination events than sequence `3424` and consume newer relevant Slack coordination.
4. Fresh-read every bound GitHub review target and mutable branch head.
5. Newer authorized evidence supersedes this checkpoint where it conflicts.

## Mune deliverables awaiting Voss reconciliation

- `MU3`: exact-head V3 design rereview `APPROVED`; `reviews/edge-privilege-v3-review-984cbdc-v1.md` @ `3ae9b9facf44a0749b2198278fc9cb7839cded2d`. Managed hosted Edge implementation is separately blocked on ambient capability containment; `reviews/edge-v3-managed-runtime-capability-audit-v1.md` @ `ba34b85295506d98f59de2da398080b254dba28f`.
- `MU4`: `APPROVED_CUSTODY_DIRECTION`; `reviews/correction-store-durability-audit-v1.md` @ `5460b7661e31c64b664d5c1bed265cfd17705ff9`, with fresh cleanliness-vs-invariant addendum.
- `MU5`: `COMPATIBLE_IF_STRICTLY_SEPARATED`; `reviews/ap-safety-continuity-separation-audit-v1.md` @ `48b67300739b96ab057c185953204deba4c336e5`.

These artifacts do not self-close Voss assignments.

## Controlling Mune research

- Knowledge Resolver V2: `research/governed-knowledge-resolver-adversarial-v2.md` @ `97c8614954c6731701a81cfd5324e5e3caf7033b`.
- Trusted admission/resolver execution: `research/assignment-admission-resolver-execution-challenge-v1.md` @ `ce1185e16a73d9d4db9f9a45c9021355be2ccaf4`.
- Assignment contract drift: `research/assignment-event-v1-contract-drift-finding.md` @ `995d8d9a81d4696faebb1457f290c500b12041cc`.
- State-chain slot poisoning: `research/assignment-state-chain-slot-poisoning-finding.md` @ `92accf5b3244c2e1c0714d29ec62a49b2364b961`.
- Receipt digest layering: `research/resolver-receipt-layering-adversarial-v1.md` @ `97047b08afbcd94ecc53cce830605a8f3c7d1189`.
- Protected admission registry challenge: `research/protected-admission-registry-adversarial-v1.md` @ `b44679c01c09c04c2e601557b87881367518ecbb`.
- Native currentness budget: `research/native-assignment-currentness-budget-note-v1.md` @ `68e39e9438d341df804888dd99982a09fab5c713`.
- Evaluator custody: `research/evaluator-custody-adversarial-challenge-v1.md` @ `997dd63f1bcb9d66596b885098eea5eaa2dee62b`.
- External effect authority cut: `research/external-effect-authority-cut-adversarial-v1.md`.
- Repository topology map: `state/BRANCH_STATUS.md` @ `e678737596b4536f8ef6c37361d9ca91a4cb8782`.

## Current architecture snapshot

- `ASSIGNMENT_CURRENTNESS` is the first Governed Knowledge Resolver proof domain.
- Production direction: one canonical coordination state graph + narrowly writable admission-proof registry, not a duplicate state ledger.
- State successor protection must be keyed from the referenced protected predecessor regardless of child row schema; ordinary assignee/proposal writers cannot consume protected state slots.
- Root uniqueness needs a real canonical project/thread namespace constraint/claim; one-successor uniqueness cannot enforce roots.
- Random canonical state UUID is separate from proposal/attempt idempotency.
- Root ASSIGN event ID remains preferred workload-lane identity.
- Currentness, blocking, authority, artifact binding, source completeness/consistency and provider target freshness remain separate axes.
- `event_sequence` is DB-generated identity, but MAX sequence is audit-only, not commit-completeness/CAS.
- Current GitHub non-force ref update is `FAST_FORWARD_GUARD`, not exact expected-old-head CAS.
- Shared broad direct INSERT cannot prove logical actor; trusted writer/admission and separate authority-assurance remain required.
- `ASSIGNMENT_EVENT_V1 version=1` historical drift requires frozen revision or explicit legacy adapter/forward normalization before deterministic production use.
- Managed Supabase Edge V3 runtime must prove broad default project capabilities are absent/unusable/equivalently contained, not merely that happy-path code uses a narrow role.

See the immutable checkpoint for exact peer/canonical state through 3424 and all caveats.

This pointer is a technical continuation aid, not autobiographical memory and not authority over newer project state.