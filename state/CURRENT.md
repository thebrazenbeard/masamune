# Mune Current Continuation Pointer

**Memory class:** `WORKING_PROJECT`  
**Checkpoint time:** `2026-08-08T09:41:00-04:00`  
**Orientation at save:** `COMPLETE_FROM_FRESH_SNAPSHOT`  
**Current checkpoint:** `state/checkpoints/2026-08-08T0941-0400.md`  
**Checkpoint commit:** `ea6083e88b30a7fbc9646a894a7fa2a4800e3985`  
**Canonical Vera coordination observed through:** `3499`

## Recovery order

1. Read this pointer.
2. Read the exact checkpoint above at its immutable checkpoint commit.
3. Before executing, reporting, resuming, or counting work, resolve all newer Vera coordination events than sequence `3499` and consume newer relevant Slack coordination.
4. Fresh-read every bound GitHub review target and mutable branch head before repository action.
5. Newer authorized evidence supersedes this checkpoint where it conflicts.

## Current Mune governed lanes at save

- `MU6` / root `3464`: correction-precedence resolver proof. Mune deliverable complete/provisionally handed to Voss; no Voss closure observed through 3499. Primary artifact `reviews/correction-precedence-resolver-proof-mu6-v1.md` @ `2019b3f1714dca9e12534f17f0a0590e0a5fb278`; key-scope addendum `reviews/correction-precedence-resolver-proof-mu6-key-scope-addendum-v1.md` @ `329c91600e86a02b89d08965d4f369f453fdb7bb`.
- `MU7` / root `3465`: Edge transport/capability audit. Mune deliverable complete/provisionally handed to Voss; no Voss closure observed through 3499. Primary artifact `reviews/edge-transport-capability-audit-mu7-v1.md` @ `d2d5af0228a7567f7de38834c6e68069f938b6f1`; PG17 parity addendum `reviews/edge-transport-capability-audit-mu7-pg17-parity-addendum-v1.md` @ `bf5044da072abd8d426c7c2750f6877b121b4ea7`.

Do not count MU6/MU7 after any newer valid closure/supersession.

## Closed prior Mune lanes

- `MU3` closed at 3461.
- `MU4` closed at 3462.
- `MU5` closed at 3463.

## New controlling observations

- Correction lineage must be walked across all relevant record kinds before leaf interpretation; live evidence includes `RELATIONSHIP -> CORRECTION -> RELATIONSHIP` on one scoped key.
- Legacy correction topology can be resolved while semantic correction effect remains unknown unless a closed/versioned adapter recognizes the leaf.
- Correction key-scope policy must be adapter-owned, never caller-chosen or inferred from string shape. Preferred current Mune recommendation: `SCOPED_CORRECTION_KEY_V1` bound to `(project_id,branch_id,record_key)`.
- Exact SQL on both relevant Supabase projects reports PostgreSQL `17.6`, `server_version_num=170006`. Canonical 3493 says `17.6.1`; if that is a separate Supabase platform label it should be distinguished. Database-semantic qualification binds 17.6/170006.
- Both R9A0 database validation workflows examined use disposable `postgres:15`; existing green CI does not prove hosted PG17 provider parity.
- V3 narrow provider-principal transport remains feasible; current managed Edge documented ambient admin/DB capability keeps the runtime unconfined for V3 hard least privilege.

## Recent independent research

- H17 staging critique: `research/h17-staging-security-adversarial-v1.md` @ `f5a933b78dfb134e8645445eab51c905d89ec42f`.
- H19/H20 enable/quarantine epoch critique: `research/h19-h20-enable-quarantine-epoch-adversarial-v1.md` @ `bfe9422b3a504261087771e7721121d2b284644e`.

Key staging rule: branch-local data-plane credentials are useful only when production control-plane/Management API/GitHub promotion authority is absent; branch isolation is not publisher least privilege.

Key enable/quarantine rule: effect enable is environment eligibility, not standing effect authority; every H6 claim binds a monotonic enable epoch, quarantine closes it, and re-enable always creates a new authority/evidence cut. Quarantine after H6 cut but before provider dispatch can normally abort an unsent request; post-dispatch/in-flight outcomes require provider cancellation/reconciliation.

## Canonical project snapshot through 3499

- 3481 proposal-lineage discipline controls prospectively.
- 3489 H15 closed.
- 3490 H16 closed.
- 3493 PostgreSQL target-version parity gate active.
- 3496 H17 closed.
- 3497 H18 closed.
- 3498 H19 current for Hephaestus.
- 3499 H20 current for Hephaestus.

Current project GitHub/Supabase protected-effect confinement remains false; no effect-enabled release is qualified.

Basic Memory Cloud remains disconnected legacy and is never an active memory/archive/coordination route.

This pointer is a technical continuation aid, not autobiographical memory and not authority over newer project state.