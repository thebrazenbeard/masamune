# Masa Hostile Review — On-Theo PR #32

execution_provenance: SAME_RUNTIME_ROLE_PASS
subject: thebrazenbeard/on-theo@093e8067bc9654fcef70f2ac13a68bc3f800fd22
tree: 0c4280f1739d5eda57b421957edf38f85da89a50
result: PASS_EXACT
scope:
- tests/test_materialization_rehearsal.py

The delta removes the false assumption that the repository always has 20 active extensions and instead binds the expected application count to the actual source manifest.

The new regression constructs a materialized registry root and re-runs the rehearsal against it, requiring:
- zero active extensions applied;
- zero collisions;
- zero unresolved references;
- valid source/output registries;
- before-counts equal after-counts.

Hostile check: the change does not relax registry validation, output digest checks, archive requirements, or the canonical-effect boundary. It makes the suite correctly represent both sides of the intended state transition.

Exact evidence:
- push run 35382166205: SUCCESS
- PR run 35382241824: SUCCESS
- 54/54 tests PASS
- validator clean
- rehearsal clean
- reviewed output registry digests unchanged.

No blocking finding.

This is a same-runtime role pass, not an independent runtime sample.
