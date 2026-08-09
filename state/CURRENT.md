# Mune Current Continuation Pointer

**Memory class:** `WORKING_PROJECT`  
**Checkpoint time:** `2026-08-09T10:39:28-04:00`  
**Orientation at save:** `COMPLETE_FROM_FRESH_SNAPSHOT`  
**Canonical Vera coordination observed through:** `3699`

## Recovery order

1. Query Vera coordination after sequence `3699`; canonical DB currently lags Patrick's direct B15 authority and must not override that newer user instruction.
2. Fresh-read `#mune`, `#voss`, `#masa`, and `#bob` for MU15/MU16 amendments and producer progress.
3. Fresh-read producer branch before reviewing any new Bob checkpoint; expected last verified Bob head at this save is `70a76f46be1954dbc9789b1a5d1cc7ea2663f222`.
4. Fresh-read `mune` before any Mune branch write. Newer authorized evidence supersedes this pointer where it conflicts.

## Current authority / producer state

Patrick directly authorized B15 execution at 2026-08-09 10:01 EDT: Bob is sole writer for `feature/r9a0-combined-native-implementation-v1`, exact current ceiling `20 MODIFY + 54 CREATE = 74`, non-force commits only. Voss may coordinate implementation/review/CI/testing on the already-authorized BT2 nonproduction ground. Merge, deploy, production Vera DB mutation, credentials, paid services, Project installation, deletion, model training and canonical-memory writes remain forbidden. Scope expansion or unexpected branch movement returns to Patrick.

This direct user authority supersedes the old canonical 3579 repository-write pause for current authority purposes. Fresh Vera query still shows no coordination event above 3699, so canonical lag is observed but not controlling over Patrick's newer direct instruction.

Bob checkpoint 1 is now committed:
- head `70a76f46be1954dbc9789b1a5d1cc7ea2663f222`;
- exactly one commit after `ddcd98b4e61df09f06886f2073ecbdfad21c8f12`;
- only `.github/workflows/r9a0-native-project.yml` changed, +1/-0;
- exact change: add combined implementation branch to `push.branches`;
- current workflow blob `39639b56a87024c0189417d6f48f32ddb7a3442a`, matching the previously admitted candidate.
Any CI from this checkpoint is intermediate evidence only, never final `BUILT_AND_VALIDATED` evidence. Current connector's commit-status route returned no status records and its commit-workflow-run route is PR-filtered, so no push-run PASS/FAIL claim is made here.

Independent H41/B22 pathset audit converges on exactly 74 unique paths with sorted-newline SHA-256 `4b3179af492630b3b9a4cac28bce0984012b3c8f47ea67779ed639d127e2e2b9`. Package is included, Voice remains no-touch, DB workflow remains outside native74 absent separate authority.

## Current Mune lanes

- `MU6 / VOSS-20260808-MU6`: canonical CURRENT read-only; final integrated resolver proof remains READY_FOR_REVIEW. Core: full governed graph before privacy, controlling state vs non-consuming evidence relation classes, fan-out/cross-thread evidence, admission/custody uncertainty, terminal absorption, separate mutation CAS/path confinement and retry-idempotency.
- `MU7 / VOSS-20260808-MU7`: canonical CURRENT read-only; final edge-transport capability audit READY_FOR_REVIEW. Preferred hard boundary remains dedicated narrow PostgreSQL LOGIN; Data API conditional/provider-unqualified; protected activation still needs end-to-end confinement.
- `MU10 / VOSS-20260809-MU10`: canonical CURRENT read-only; Package REQUIRED_NOW / Voice NO_TOUCH / exact 74-path footprint. Await canonical disposition.
- `MU11`: provisional read-only install-machine hostile READY_FOR_REVIEW. One immutable install-attempt identity, fixed route per attempt, closed/versioned qualification environment, acyclic post-effect receipt ordering, isolated pre-release vs in-situ post-install split.
- `MU12`: provisional read-only cutover hostile READY_FOR_REVIEW. Old-writer fence -> fenced admitted snapshot -> exact-once reissue -> verify -> authority-source-flip readback.
- `MU13`: provisional historical review artifact. Its former “B15 not ready for authority” conclusion is superseded by Patrick's 10:01 direct authorization; its pre-byte vs external post-commit evidence split remains valid.
- `MU14`: provisional provider-evidence provenance hostile READY_FOR_REVIEW. Hosted BT2 proves only foundation applied; provider environment observation never proves later candidate application.
- `MU15 / MA23_HYBRID_SUCCESSOR_HOSTILE`: provisional read-only, current verdict `CHANGES_REQUESTED`. Artifact `reviews/ma23-hybrid-successor-hostile-mu15-v1.md` @ `3e3e026894866485426cf6c97187b7435714e527`, blob `50af7766700b47c64ee41d86d8177e8a949d6223`. Two blockers: reissue operation identity wrongly includes semantic-state digest, allowing changed S1 under same epoch to mint a second op/root; and post-flip rollback semantics could reactivate legacy late rows. Require stable op/mapping key `{epoch,legacy subject,legacy root}`, semantic/S1 state in request digest, immutable `S1_BOUND` per epoch, and no post-flip old-source pointer rollback. Masa independently corroborated both at Slack TS `1786286121.432159`. Await integrated MA23 amendment before changing verdict.
- `MU16 / B15_FIRST_AUTHORING_EPOCH_HOSTILE`: provisional read-only, READY_FOR_REVIEW. Artifact `reviews/b15-first-authoring-epoch-hostile-mu16-v1.md` @ `c316915109634ba4445db7a3b2eb66f9c1198e98`, blob `3bf04018f36a9208b5e43167721504559d7d3354`. Safe narrow work: checksum parser hardening, manifest path/symlink confinement, already-frozen AP scaffolding, and admitted workflow route delta. Schema enforcement is required but external `jsonschema` is not currently an admitted/hermetic dependency; a new requirements/vendor file would be path75. Defer MA23/MA24/currentness/install/final-PASS dependent bytes.
- `MU9`: Voss-closed at 3669.
- `MU8`: Voss-closed at 3616.

## Fresh semantic/provider inputs

MA23 final chooses orthogonal `events` + consuming `state_transitions` + non-consuming `evidence_links`, hybrid reissue of admitted CURRENT lineages only, explicit reviewed mapping for the two hosted foundation rows, terminal/generation correctness, workload CAS, and auth family B direction. MU15 accepts those directions after its two mechanical amendments.

MA25 provenance minimum is substantively accepted as a required MA23 amendment: evidence is snapshot-bound iff removing it changes admitted current state or drops authority/source-completeness assurance below threshold. Admission-critical mutable-source evidence requires captured content/normalized-fact digest; locator-only evidence must be proven non-required.

MA24 final defines the PG17/PostgREST qualification execution packet, including exact immutable N/D/T identities, provider-like non-super migration actor, pinned PostgREST HTTP lane, rollback->prestate/reapply fingerprints, and one-run P3+P5 only when exact final native N and corrected DB D are composed. Hosted P4 and DB admission P6 remain separate.

MA26 selects auth family B: single exposed SECURITY DEFINER RPC + exact EXECUTE ACL + connector session/modern `request.jwt.claims` provenance; actual HTTP qualification required. This does not claim transport exclusivity or eliminate direct authenticator-credential trust.

H43 independently confirms Native Contract schema must be recursively closed by temporal/semantic field class before enforcement. Current schema closes top level but leaves six major nested objects as naked `type: object`. Do not copy stale B12 constants. Contract/schema closure should wait for MA23/MA24/B17/B18 byte-shaping closure; checksum/manifest parser hardening may proceed now.

## Verified bugs / bug-ops notes

New connector-quality bug:
- `122fd060-5672-48f6-9ca6-08a61d29b8d9` / `SUPABASE-ADVISOR-RLS-ACL-EXPOSURE-FALSEPOSITIVE-001`, LOW, now TRIAGED v2.
- Supabase `list_tables` correctly warned that seven `bug_ops` tables have RLS disabled, but falsely asserted they are fully exposed to anon/authenticated. Fresh catalog readback proves anon/authenticated have no USAGE on `bug_ops` and no SELECT/INSERT/UPDATE/DELETE on the seven tables. Treat RLS-disabled as defense-in-depth hardening, not current public exposure. Reported via bug_ops and `#chat-bug-reports` TS `1786285693.544689`.

Current validator defects remain TRIAGED:
- `69eaf34b...` checksum duplicate last-write-wins;
- `c69a2051...` manifest traversal/out-of-project membership;
- `819654d7...` schema parsed but not enforced;
- `85182817...` nested schema remains open/underspecified;
- `9094453e...` final installation receipt lacks immutable effect-time authority evidence binding.

No new MU15 bug ticket was created because its findings are pre-implementation contract corrections rather than a deployed distinct defect.

## Exact hosted/provenance facts retained

BT2 `r9a0_coordination.events` currently contains exactly two foundation-era rows: seq2 foundation REVIEW/READY_FOR_REVIEW with no relation edge, and seq3 Mune REVIEW/CHANGES_REQUESTED acknowledging seq2. They require explicit reviewed historical/evidence mapping, never heuristic state typing.

Legacy Vera `public.vera_coordination_events` has insert record-time, UPDATE blocker and DELETE blocker triggers but no BEFORE TRUNCATE guard. Therefore admission-critical legacy evidence cannot be preserved for successor audit by live-pointer-only semantics.

Hosted BT2 migration-application provenance still proves only foundation `20260806133152/e394132f...` applied. Later 58a integrity/owner/read-policy migrations remain repository/disposable-CI evidence, not hosted application proof.

## Effect boundary

Mune performed authorized read-only provider/source inspection, bug reporting, Slack coordination, and writes only to Mune's own `masamune:mune` research/checkpoint branch. Mune did not modify the Vera-R9A0 producer branch, canonical coordination state, BT2/Vera schema/roles/grants, provider config, credentials, merge/deployment state, installation state, production data, or canonical memory.