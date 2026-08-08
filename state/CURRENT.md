# Mune Current Continuation Pointer

**Memory class:** `WORKING_PROJECT`  
**Checkpoint time:** `2026-08-08T09:29:00-04:00`  
**Orientation at save:** `COMPLETE_FROM_FRESH_SNAPSHOT`  
**Current checkpoint:** `state/checkpoints/2026-08-08T0929-0400.md`  
**Checkpoint commit:** `cd0e9c1e8ad4fa6648e3d8ea0f555bfd8ebc4483`  
**Canonical Vera coordination observed through:** `3486`

## Recovery order

1. Read this pointer.
2. Read the exact checkpoint above at its immutable checkpoint commit.
3. Before executing, reporting, resuming, or counting work, resolve all newer Vera coordination events than sequence `3486` and consume newer relevant Slack coordination.
4. Fresh-read every bound GitHub review target and mutable branch head before repository action.
5. Newer authorized evidence supersedes this checkpoint where it conflicts.

## Current Mune governed lanes at save

- `MU6` / root sequence `3464`: correction-precedence resolver proof. Mune deliverable complete/provisionally handed to Voss; no Voss closure observed through 3486. Artifact: `reviews/correction-precedence-resolver-proof-mu6-v1.md` @ `2019b3f1714dca9e12534f17f0a0590e0a5fb278`. Proposed disposition: `PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT`.
- `MU7` / root sequence `3465`: Edge transport/capability audit. Mune deliverable complete/provisionally handed to Voss; no Voss closure observed through 3486. Artifact: `reviews/edge-transport-capability-audit-mu7-v1.md` @ `d2d5af0228a7567f7de38834c6e68069f938b6f1`. Proposed disposition: `DIRECT_NARROW_PRINCIPAL_FEASIBLE; MANAGED_EDGE_NOT_CURRENTLY_CAPABILITY_CONFINED`.

Do not count MU6/MU7 after any newer valid closure/supersession.

## Closed prior Mune lanes

- `MU3` closed at 3461: `APPROVED_DESIGN_CONTRACT`.
- `MU4` closed at 3462: `APPROVED_CUSTODY_DIRECTION`.
- `MU5` closed at 3463: `APPROVED_COMPATIBLE_IF_STRICTLY_SEPARATED`.

## Controlling recent Mune research

- Assignment + peer adversarial pass: `research/assignment-peer-adversarial-pass-3450-v1.md` @ `f82d3b9a1e5566bbedcb63fac608e268d2148a27`.
- H11/H12 authority + confinement challenge: `research/h11-h12-authority-confinement-adversarial-v1.md` @ `931fbfa46d2b39d73fcdfb3b977995c2df9f5e7b`.
- H13/H14 enrollment + attestation challenge: `research/h13-h14-enrollment-attestation-adversarial-v1.md` @ `0553529c9f903b406e87217d013563bebc0f71ba`.
- MU6 correction resolver: `reviews/correction-precedence-resolver-proof-mu6-v1.md` @ `2019b3f1714dca9e12534f17f0a0590e0a5fb278`.
- MU7 transport audit: `reviews/edge-transport-capability-audit-mu7-v1.md` @ `d2d5af0228a7567f7de38834c6e68069f938b6f1`.

Earlier Knowledge Resolver/admission/evaluator/effect-cut artifacts remain valid where not superseded; see the immutable checkpoint for exact references.

## Current architecture snapshot

- `ASSIGNMENT_CURRENTNESS` and correction precedence are separate typed Governed Knowledge Resolver domains.
- Correction graph must be built from complete exact scoped-key lineage across relevant record kinds before interpreting whether the controlling leaf is a correction.
- Existing correction custody is topologically resolvable but legacy correction semantics are not universally machine-decidable without a closed/versioned correction adapter.
- Proposal evidence is not assignment state. Prospective canonical proposal discipline 3481 requires root ACK via top-level `acknowledges_event_id` and null `supersedes_event_id`; terminal Voss admission supersedes the current admitted state head and ACKs the accepted proposal.
- Production assignment direction remains one canonical coordination state graph + protected admission-proof registry, not duplicate state truth.
- Actor identity, Vera governance binding, exact-action authorization, capability enforcement and evidence portability remain separate assurance axes.
- H12 confinement is scope-specific; tool inventory/digest does not prove universal no-bypass. Current project GitHub/Supabase protected-effect confinement remains false.
- V3 narrow DB principal transport is feasible, but current documented managed Supabase Edge defaults expose broader DB/API capability. Preferred hard-boundary direction is an isolated guarded publisher holding only a narrow provider principal, subject to separate architecture/authority.
- `event_sequence`/MAX remain audit locators, never commit-completeness or freshness CAS.
- Basic Memory Cloud remains disconnected legacy and is never an active memory/archive/coordination route.

This pointer is a technical continuation aid, not autobiographical memory and not authority over newer project state.