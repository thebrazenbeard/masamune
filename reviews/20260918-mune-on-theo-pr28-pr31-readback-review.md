# Mune Reproduction / Provenance Review — On-Theo PR #28 through PR #31

status: COMPLETE
execution_provenance: SAME_RUNTIME_ROLE_PASS
protocol_source:
  repo: thebrazenbeard/masamune
  head: 0091746bba7740632268fb590ce19512e371f508
  protocol: PROTOCOL_V2_CURRENT.md

This review applies Mune's current exact-subject reproduction, fix-verification, regression, and provenance discipline. It was run from Mune's isolated repository branch inside the current controlling ChatGPT runtime. It is not an independent runtime sample.

## Exact subjects

- #28 `99be7dd0e222480e0c82ed41c3d43383a759ab90`
- #29 `8234d3fcc2d5a0eda26e5c7d4c2211de067c600a`
- #30 `8e651851cdc1d1d4994784a69b961d87914a32e0`
- #31 `d81ab5ab58f326b0827dbc0f9903befb5580947e`

## #28 — PASS_WITH_LIMITATIONS

The consolidation is supported as a path/blob-preserving integration subject. The repository's README/branch map explicitly separate imported legacy prose from accepted/current epistemic state, preventing simple file presence from becoming supersession.

Limitation: mechanical losslessness is not scholarly re-verification of each claim.

## #29 — CHANGES_REQUIRED

The exact V2 validator can silently omit malformed non-mapping records because `records()` filters before validating. This was independently reproducible at the source/test level in GitHub Actions run `35380669318`.

That invalidates a full provenance PASS for frozen #29 even though its ordinary suite was green.

## #30 — CHANGES_REQUIRED

The rehearsal generated deterministic output and preserved source bytes, but:
- it inherited the V2 validation blind spots;
- its receipt did not include the manifest-required `unresolved_reference_count`.

The frozen generated registry digests remain valid as observed output bytes; the control/qualification claim was too strong.

## #31 — PASS_WITH_LIMITATIONS

Exact successor evidence:
- head `d81ab5ab58f326b0827dbc0f9903befb5580947e`
- tree `e6e94b7ed35551ca675fed64ce2a0999ea441628`
- push run `35381285810`: SUCCESS
- PR run `35381382184`: SUCCESS
- 53/53 tests PASS
- validator JSON: `ok=true`, errors/findings/warnings = 0/0/0
- rehearsal PASS
- `unresolved_reference_count=0`
- eight output-registry SHA-256 values are byte-identical to frozen #30.

Exact-subject rebase/provenance reread:
- subject: PR31 exact head, not inherited PR30 head
- audit head `ef93955a9a902bf2d8ce4256fed9b30126c8343f`
- Actions run `35381678450`
- 55/55 PASS
- 9 divergent extensions / 6 unique bases
- 8 have zero external pre-existing references
- sole external pre-existing ref is `SRC-CELSUS-TRUE-DOCTRINE`
- canonical record equality holds
- mismatch count 0
- dependency-closure violations 0.

Fix verification: the original malformed-record reproductions are covered by V3 regression tests, and the stricter current validator accepts the real repository data.

Nonblocking limitations:
1. a 40-hex `subject_sha` is structurally valid but remote repository existence/membership is an external-readback fact; promotion admission must verify it against GitHub;
2. receipt/path integrity does not prove historical proposition truth;
3. same-runtime role execution cannot be upgraded to INDEPENDENT_RUNTIME.

Rebase exception disposition under Mune's mechanical/provenance scope: the current PR31-bound evidence is sufficient for **candidate construction review**, because actual external preconditions are unchanged and dependency closure is explicit. It is not a historical-semantic endorsement and it does not authorize promotion.

Protected effects remain unperformed.
