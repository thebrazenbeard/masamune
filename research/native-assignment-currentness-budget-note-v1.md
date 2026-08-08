# Mune Research — Native Assignment-Currentness Budget Compression Note V1

**Peer context:** Voss V4 native instruction/enforcement budget; Bob B4 AP+safety preflight 3387/3389  
**Native base:** `thebrazenbeard/vera-R9A0@6a568d35c142dc37ea41a0209cdb1f295949f767`  
**Current native instructions blob:** `f95f7390d6a081a1ca3bdd087a7dec1f4d3b170a`  
**Mode:** read-only design/budget challenge; no native/repo producer mutation

## Finding

Bob's accepted AP+safety composition is reported at:

- `7776` characters
- existing validator ceiling `8000`
- remaining margin `224` characters

That is extremely tight, but **it does not prove assignment-currentness cannot fit**.

The mistake would be to append a miniature resolver specification to the native instructions. Native Settings only need the normative trigger/fail-closed rule; detailed enums, lineage semantics, adapter behavior, and provider precondition classes belong in Runtime/contract/schema/validator/tests.

## A standalone trigger can almost fit by itself

A compact but materially complete normative sentence can be around 215 characters:

```text
Before start/resume/report/count/effect, resolve current assignment. SOURCE_INCOMPLETE/CONFLICTED/UNKNOWN/UNAVAILABLE blocks action/count; dependency-blocked never counts. Re-resolve pre-effect; target CAS separate.
```

This demonstrates feasibility, but appending it to a 7776-character candidate would leave essentially no maintenance margin after newline/formatting and is therefore not the preferred integration.

## Better: absorb currentness into the existing freshness/authority paragraph

The exact native base already contains a roughly 407-character paragraph requiring source refresh and abstention for project-history/authority/recovery/unfinished-work claims.

A compressed combined paragraph can carry both the existing evidence rule and assignment-currentness trigger with only a small net increase, conceptually:

```text
For history, correction, authority, recovery, or unfinished work, refresh relevant sources and bind evidence; abstain if unresolved. Never claim recovery, provenance, consumption, or readback without exposed evidence. Before start/resume/report/count/effect, resolve assignment currentness; incomplete/conflicted/unknown/unavailable blocks action/count; dependency-blocked never counts. Re-resolve pre-effect; target CAS is separate.
```

Measured against the current base paragraph, this construction is only about **26 characters longer**, despite adding the full currentness trigger concept.

The exact future wording should be reviewed against the AP+safety composed candidate, not copied blindly. The point is architectural: **refactor overlapping freshness prose instead of stacking three independent instruction packets.**

## What must remain in native Settings

Minimum normative behavior:

1. start/resume/report/count/effect are currentness triggers;
2. unresolved/incomplete/conflicted/unknown/unavailable currentness fails closed for the gated action/count;
3. dependency-blocked can remain assigned but does not satisfy executable workload floor;
4. re-resolve immediately before effect;
5. provider target freshness/CAS is separate from assignment resolution.

Everything else should live in the strict runtime/contract/test surfaces.

## What should not be crammed into Settings

Do not spend scarce native characters listing:

- the complete ASSIGNMENT_EVENT transition matrix;
- source-mode/completeness/consistency enum definitions;
- root lane-ID derivation algorithm;
- provisional canonicalization bridge grammar;
- controlling/rejected event trace fields;
- lineage-digest construction;
- provider precondition-strength enum;
- recursive SQL behavior;
- trusted admission internals.

Those belong in Runtime/native contract/schema/validator/tests and can be referenced by the compact normative trigger.

## Validator strategy

Brevity creates a different risk: an overcompressed instruction can accidentally lose one hard invariant.

The validator/contract tests should therefore assert behavior structurally rather than require a verbose prose recital.

At minimum fail if the combined candidate lacks evidence that:

- assignment currentness is mandatory for all five trigger classes;
- dependency-blocked does not count toward executable floor;
- incomplete/conflicted/unknown/unavailable states fail closed;
- effect path requires fresh re-resolution;
- target CAS/precondition remains independent;
- AP cannot alter protected currentness/safety/authority outcomes;
- safety correction precedence and provenance gate remain intact.

## Budget conclusion

`224 characters remaining` is a warning, not a proof of impossibility.

A naive append is brittle. A coherent rewrite that merges overlapping freshness/currentness language can plausibly fit while preserving the 8000-character ceiling.

The correct V4 question is therefore not:

> "Can we squeeze another paragraph into 224 characters?"

It is:

> "Can one compact native control statement point to a strict runtime/contract/schema/validator implementation without duplicating its details?"

I think the answer is yes, but only after measuring the exact final AP+safety+currentness candidate and preserving some nonzero margin. A candidate that lands at 7999 because every concept was compressed into punctuation is technically valid and operationally ridiculous.

No native Project file, producer repository branch, database, deployment, credential, paid service, merge, or canonical memory was modified.