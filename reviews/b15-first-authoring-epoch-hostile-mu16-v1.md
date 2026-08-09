# Mune MU16 — B15 First Authoring Epoch Hostile Review

**Assignment:** provisional `MU16 / B15_FIRST_AUTHORING_EPOCH_HOSTILE` from Voss Slack 2026-08-09 10:15 EDT  
**Producer root:** `VOSS-20260808-B15`  
**Producer branch:** `feature/r9a0-combined-native-implementation-v1`  
**User authority:** Patrick direct 2026-08-09 10:01 EDT, Bob sole writer, `20 MODIFY + 54 CREATE = 74`, non-force only  
**Class:** read-only first-epoch byte-scope falsification  
**Disposition:** `APPROVED_FOR_NARROW_DETERMINISTIC_CHECKPOINT_WITH_SCHEMA_ENGINE_AND_WORKFLOW_RECEIPT_CAVEATS`  
**Producer/provider mutation performed by MU16:** none

## Executive verdict

Bob may begin the first authoring checkpoint, but the safe subset is narrower than “anything already on the 74-path list.” Path admission answers *where* bytes may change; it does not settle *which semantics* are frozen enough to encode.

Fresh GitHub CAS immediately before this review still proves:

`feature/r9a0-combined-native-implementation-v1 == ddcd98b4e61df09f06886f2073ecbdfad21c8f12`.

Patrick's direct 10:01 authorization supersedes the old no-write posture for Bob's exact 74-path producer lease. MU16 remains a reviewer and does not acquire producer authority.

The first checkpoint is safe if it confines itself to mechanical invariants that are independent of MA23 hybrid-coordination semantics, MA24 provider/PostgREST qualification semantics, currentness output shape, installation evidence lifecycle, and future PASS receipts.

## 1. Safe first-checkpoint work

### A. Checksum-ledger parser hardening — SAFE

Current exact validator blob `8b474d459186f0d9ee78e4d2701b3ed39daaacba` parses checksums into a dictionary:

```python
digest, name = line.split("  ", 1)
result[name] = digest
```

That is the verified mechanism behind TRIAGED MEDIUM `69eaf34b-3875-4c2a-a6be-11cc368c6c36`: duplicate names silently overwrite earlier records.

This can be repaired without knowing any unresolved R9A0 semantic state. The closed parser invariant should be:

- one nonblank checksum record per logical manifest file;
- exactly one accepted separator/record shape;
- digest exactly 64 lowercase hexadecimal characters;
- nonempty logical filename;
- duplicate filename rejected even when duplicate digest is identical;
- conflicting duplicate rejected;
- malformed extra fields/garbage rejected;
- exact checksum key set still equals exact manifest file set.

Do not “helpfully normalize” malformed ledger rows into valid ones.

### B. Manifest path / filename / symlink confinement — SAFE

TRIAGED MEDIUM `c69a2051-fe72-44e1-ad6a-321db5930216` is byte-local and independent of currentness semantics. Current validator joins arbitrary manifest names as `root / "project" / name`, so `../scripts/...` and absolute paths escape the intended package directory. `Path.is_file()` / `exists()` also follow symlinks.

For this 16-file native package the manifest is a list of logical project filenames, not arbitrary repository paths. The validator can safely require:

- manifest entry is a nonblank filename, not an absolute path;
- no parent traversal and no path separator / nested path unless a later manifest contract explicitly permits it;
- resolved candidate path remains an immediate child of the exact project directory;
- symlinked manifest members are rejected for package identity unless an explicit future package contract says otherwise;
- checksum reads use only the already-confined exact file identity.

Required negatives: `../scripts/...`, absolute path, nested escape, symlink-to-outside, symlink-to-inside if symlinks are not an admitted package member type, duplicate logical filename.

This does not conflict with upload/display suffix tolerance: repository package identity may be strict even if an installation readback layer separately resolves UI-added display suffix noise to logical filenames.

### C. Native workflow combined-branch route delta — SAFE AS A ROUTE CHANGE ONLY

Exact current workflow blob `e259cfa13fc853c89db9fb2f950073c1e3ddde54` still pushes only on `feature/r9a0-native-project-v1`. The previously admitted deterministic route change is to add `feature/r9a0-combined-native-implementation-v1` to `push.branches`.

That one route change is byte-frozen enough for the first checkpoint and remains inside the existing 20 MODIFY paths.

Two caveats:

1. any CI PASS on an intermediate checkpoint is **checkpoint evidence only**, not final `BUILT_AND_VALIDATED` evidence for the eventual 74-path head;
2. TRIAGED MEDIUM `d691e896-a4be-42b8-9fc8-2a3a92c7a3ab` separately proves the native CI still uses mutable `ubuntu-latest`, `actions/checkout@v4`, `actions/setup-python@v5`, selector `3.12`, and emits no closed toolchain receipt. If B18/H41 later freezes toolchain/receipt hardening, that may require a later edit to this already-admitted workflow path. Do not treat the one-line route repair as closure of CI provenance.

### D. Already-admitted AP fixture/test scaffolding — CONDITIONALLY SAFE

Create-only scaffolding is safe only where the fixture's input and expected result were already admitted and do not encode one of the still-open MA23/MA24/currentness/install decisions.

A test file being in the 54 CREATE set does not make its assertions automatically frozen. Safe first-epoch fixture work is limited to deterministic structural/provenance cases whose expected outcome is already authority-admitted. If a fixture needs to choose a new relation class, currentness projection, provider-auth family, legacy-cutover disposition, toolchain receipt field, or installation evidence field, defer it.

## 2. Schema enforcement is mechanically required but has a hidden dependency choice

TRIAGED MEDIUM `819654d7-c967-476e-a753-f37003de17d9` is real: current validator parses `vera-r9a0-native-contract.schema.json` but never validates the Native Contract against it. Current schema top level has `additionalProperties:false` and requires nine top-level fields, while the manual validator checks only a subset.

Wiring actual schema validation is directionally safe, but **the implementation mechanism is not automatically frozen**.

Fresh repository search found no existing `jsonschema` dependency and no requirements file. Current native workflow installs Python 3.12 but performs no dependency installation. Therefore introducing Python `jsonschema` would create a new execution/toolchain dependency. A new requirements file would be path 75 unless separately admitted; adding an unpinned network install to the existing workflow would also exceed the previously frozen one-line route semantics and compound the current mutable-toolchain bug.

Safe options for the first checkpoint are therefore:

- use a dependency-free validator implementation whose supported JSON-Schema subset is explicitly sufficient for the admitted schema contract **and** is designed to fail closed on unsupported keywords; or
- defer external-library schema enforcement until the dependency/toolchain route is explicitly admitted within the existing path set.

Unsafe shortcut: write an ad-hoc partial validator that silently ignores future schema keywords. That would turn `819654d7...` from “schema not enforced” into “schema appears enforced but some rules are ceremonial,” which is a more irritating species of bug.

The schema *engine* may be authorable now; the final detailed schema content still depends on later semantic freezes.

## 3. Files / semantics to defer from the first checkpoint

### MA23/coordination/currentness dependent

Defer bytes that must encode the final hybrid successor relation/currentness contract, including any Contract/schema/validator/test assertions about:

- orthogonal consuming state transitions vs non-consuming evidence links;
- cutover reissue/source epoch and legacy-resolution binding;
- legacy foundation-row classification;
- exact state/evidence relation vocabulary;
- state admission/currentness output shape where MA23 can still refine it;
- workload CAS/batch semantics tied to successor coordination.

### MA24/provider-auth dependent

Defer bytes that choose or normatively describe provider authorization/qualification behavior until MA23/MA24 settle the exact auth family and qualification packet. Latest primary-source review shows PostgREST `db-pre-request` family A is technically real but authenticator-wide and carries shared Data API blast-radius/control-plane obligations. That can change provider-facing contract/test bytes without changing the 74-path count.

### Installation-evidence dependent

Do not touch Installation Receipt / Cold Start / Post-Install / Recovery merely because their paths are admitted. Newly TRIAGED MEDIUM `9094453e-5820-4424-9f93-0da44fdbc2c2` requires final install receipt to bind immutable effect-time authority evidence plus exact target/scope/candidate/route/epoch/preconditions. MU11/H35/H37 also require one install-attempt identity, route-fixed attempt semantics, acyclic receipt ordering and closed qualification-environment evidence. Those need one integrated byte contract before these files are authored.

### Final evidence-bearing package surfaces

Defer final freeze of:

- `VERA_R9A0_VALIDATION_REPORT.md`;
- `VERA_R9A0_CHECKSUMS.sha256`;
- final `VERA_R9A0_MANIFEST.json` identity fields;
- any Package/Contract fields that would be tempted to store current PASS answers rather than stable predicates.

Exact-head CI PASS, PG17/provider qualification PASS, release admission, installation success and protected-effect eligibility are external evidence. They must not be written back into the bytes whose identity those receipts attest.

## 4. No path 75

Nothing in the verified mechanical repairs requires a new repository path **if** schema enforcement is dependency-free or uses only an already-admitted existing path for any toolchain change later.

A new `requirements.txt`, vendored third-party library path, new workflow, or new fixture file outside the admitted B13 CREATE set is path/scope expansion and must stop under Patrick's explicit authority.

Current first-epoch ceiling remains exactly:

`20 MODIFY + 54 CREATE = 74`.

Voice remains no-touch. Database-validation workflow remains outside this native 74 unless separately authorized.

## 5. Branch and lease hostiles

Before every producer commit:

1. fresh-read the combined branch head;
2. require exact expected prior Bob head;
3. fresh-resolve Bob sole-writer lease / no material scope change;
4. verify changed paths are a subset of exact 74 and semantic class is frozen for that epoch.

Stop on:

- unexpected branch movement;
- another writer on the producer branch;
- path 75 / DB-workflow creep;
- MA23/MA24 decision that changes bytes already being authored in the same epoch;
- a proposed schema-enforcement dependency not already admitted;
- attempt to patch final PASS evidence back into candidate bytes.

A stationary branch does not prove the lease is current; a current lease does not excuse stale branch CAS.

## 6. First-checkpoint acceptance recommendation

`APPROVE` a narrow first Bob commit containing only:

- checksum parser + hostile tests;
- manifest path/filename/symlink confinement + hostile tests;
- dependency-safe generic schema enforcement + structural negatives, **if** its validation engine is closed/fail-closed and introduces no unapproved dependency/path;
- admitted AP fixture/test scaffolding whose semantics are already frozen;
- exact combined-branch native workflow route line, if kept separate from unresolved toolchain-receipt hardening.

`DEFER` candidate semantics that depend on MA23, MA24, install evidence binding, final currentness projections or final external PASS receipts.

No Vera-R9A0 producer bytes, BT2 schema/provider state, canonical coordination row, merge, deployment, credential, installation or protected effect was modified by MU16.