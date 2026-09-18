# Masa Hostile Review — On-Theo PR #28 through PR #31

status: COMPLETE
execution_provenance: SAME_RUNTIME_ROLE_PASS
protocol_source:
  repo: thebrazenbeard/masamune
  head: 0091746bba7740632268fb590ce19512e371f508
  protocol: PROTOCOL_V2_CURRENT.md

This review applies the current Masa root-cause / falsification discipline from the Masamune repository. It was executed in the current controlling ChatGPT runtime from Masa's isolated review branch. It is **not** an independent model sample and must not be recorded as INDEPENDENT_RUNTIME.

## Subjects

- PR #28 consolidation: `99be7dd0e222480e0c82ed41c3d43383a759ab90`
- PR #29 validator V2: `8234d3fcc2d5a0eda26e5c7d4c2211de067c600a`
- PR #30 rehearsal: `8e651851cdc1d1d4994784a69b961d87914a32e0`
- PR #31 validator/materializer V3 successor: `d81ab5ab58f326b0827dbc0f9903befb5580947e`

## PR #28 — PASS_WITH_LIMITATIONS

Hostile target: silent semantic promotion or branch-history laundering.

The consolidation candidate explicitly states in both `README.md` and `docs/BRANCH_MAP.md` that:
- main remains canonical until an authorized merge;
- branches/PRs are work/review/provenance surfaces;
- imported legacy thematic files remain provenance/review material;
- inclusion does not make older prose supersede newer packets or vice versa.

The mechanical consolidation receipt reports zero missing paths and zero unexpected differences across the audited source heads. The legacy-currentness ambiguity is therefore bounded by explicit architecture rather than silently resolved by file presence.

Limitation: lossless inclusion and provenance labeling do not independently revalidate the historical truth of every imported research claim.

## PR #29 — CHANGES_REQUIRED

Hostile reproduction exposed a fail-open parser pattern.

Frozen V2 uses a generic `records()` helper that filters non-mapping members. A malformed entry can therefore disappear before the relevant validator sees it.

Executable reproduction:
- audit branch: `audit/masamune-malformed-record-rejection-v1-20260918`
- GitHub Actions run: `35380669318`
- observed failures: malformed review receipt, malformed source-access record, malformed pending-witness record were silently ignored.

Further source review found the same class reachable in nested claim evidence, transmission evidence, concept relations/source refs, missing required source references, manifest dependency/entity fields, and review receipts whose required fields existed but were not structurally valid exact-head bindings.

This is a real integrity defect because the manifest contract says unresolved/malformed materialization inputs fail closed.

## PR #30 — CHANGES_REQUIRED

The materialization engine itself is deterministic and its source/output byte-isolation tests are strong, but it depends on the PR #29 validator and therefore inherits its fail-open validation surface.

PR #30 also omitted `unresolved_reference_count` from the successful rehearsal receipt even though the manifest's `receipt_rule` explicitly requires it.

The rehearsal's historical byte set remains useful evidence; this disposition does not claim the generated registry bytes are wrong.

## PR #31 — PASS_WITH_LIMITATIONS

Exact head: `d81ab5ab58f326b0827dbc0f9903befb5580947e`
Tree: `e6e94b7ed35551ca675fed64ce2a0999ea441628`

Repair evidence:
- push run `35381285810`: PASS
- PR run `35381382184`: PASS
- exact PR-head suite: 53/53 PASS
- registry validator: 0 errors / 0 findings / 0 warnings
- rehearsal: PASS
- `unresolved_reference_count: 0`
- all eight materialized registry SHA-256 values unchanged from frozen PR #30.

Successor-bound rebase/dependency reread:
- audit branch: `audit/v3-rebase-and-dependency-reread-20260918`
- audit head: `ef93955a9a902bf2d8ce4256fed9b30126c8343f`
- run: `35381678450`
- 55/55 PASS
- PR31-bound rebase-precondition mismatches: 0
- cross-extension dependency closure: PASS.

Hostile conclusion: the demonstrated V2/V30 blockers are repaired on PR #31, and I did not find a remaining HIGH/MEDIUM source-integrity defect in the reviewed delta.

Nonblocking limitations:
1. local registry validation proves SHA syntax, not that an arbitrary review receipt's subject SHA actually exists in the named remote repository; consequential review admission still needs repository readback;
2. these checks establish structural/provenance integrity, not historical truth;
3. this is a same-runtime role pass, not independent sampling.

Protected boundary: no merge or canonical materialization is authorized.
