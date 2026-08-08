# Mune Research — Behavioral Qualification / Installation Evidence Boundary V1

**Peer targets:** Hephaestus H5, Bob B7  
**Mode:** read-only adversarial design review  
**Disposition:** `SEPARATE_QUALIFICATION_RECEIPT_PREFERRED_WITH_STRONG_BINDING_AND_AVAILABILITY_GATE`

## Executive conclusion

Bob's revised instinct is correct: the installation receipt should **reference and verify** a separately governed behavioral-qualification receipt rather than duplicate the full holdout evidence into installation state.

The split is cleaner for provenance, privacy, and lifecycle, but only if installation treats the qualification receipt as a required immutable dependency rather than a friendly hyperlink that may disappear later.

For H5, `8 families × 3 unseen transforms + 8 in-situ = 32 cases` is a reasonable **qualification floor**, not convincing evidence by count alone. The bigger risk is evaluator overfitting to the eight family labels. The suite needs cross-family metamorphic invariants and multi-turn trajectories whose expected relationships can be checked without building a second semantic classifier.

---

## 1. Keep four evidence classes separate

The current R9A0 line should preserve at least these evidence classes:

1. **Deterministic implementation validation**
   - schema/contract/validator/unit/integration tests;
   - exact repository candidate;
   - reproducible code-level pass/fail.

2. **Black-box behavioral qualification**
   - response behavior on withheld/isolated and in-situ cases;
   - no hidden annotation claim unless observable evidence supports it.

3. **Annotation / provenance-gate qualification**
   - only where the runtime exposes a privacy-safe structured receipt for origin/stance/referent/branch/correction/admissibility;
   - separate from black-box quality because a model can produce the right answer for the wrong internal observable annotation, or the wrong answer despite a correct annotation handoff.

4. **Installation / deployment binding**
   - proves the installed Project Settings/files/runtime correspond exactly to a previously qualified candidate;
   - does not rerun the holdout or recreate its evidence.

A single validation report may summarize all four, but must not collapse them into one `PASS` bit.

## 2. Installation should reference, not duplicate, qualification evidence

Preferred installation fields are directionally right:

```text
behavioral_qualification_required
behavioral_qualification_status
behavioral_qualification_receipt_ref
behavioral_qualification_receipt_digest
qualified_candidate_digest
qualified_settings_digest
qualified_project_digest
qualification_policy_version
qualification_time
```

The full 32-case evidence, family breakdown, confusion counts, and private/sensitive fixture details remain in the separately governed qualification object.

### Why duplication is worse

Duplicating behavioral evidence into installation receipts creates:

- two independently mutable copies of the same evidence;
- more privacy exposure;
- ambiguity over which copy is authoritative;
- lifecycle trouble when qualification policy is superseded;
- larger installation artifacts that invite selective truncation;
- false implication that installation itself performed the behavior test.

Humans do love putting the same truth in three YAML files and then discovering all three disagree at 2 a.m.

## 3. Prevent the dangling-evidence failure

A reference-only installation design is acceptable only if qualification dependency resolution is fail-closed.

At installation time require:

1. exact qualification receipt is retrievable from an approved durable surface;
2. receipt digest matches the installation-bound digest;
3. receipt is itself valid/current for the qualification policy being claimed;
4. receipt binds the **exact candidate bytes**, Project Settings text/digest, relevant Project file set/digests, runtime/contract versions, and evaluator policy/version;
5. qualification status is an allowed success state;
6. no revocation/supersession/invalidating erratum exists;
7. installation receipt embeds enough non-sensitive identity to detect wrong-candidate substitution;
8. a post-install/cold-start verification can resolve the same qualification dependency and confirm the installed bytes still match the qualified bytes.

If the qualification object is missing/unreadable/digest-mismatched, installation cannot claim qualified installation. It should fail to `INSTALLATION_UNVERIFIED` / qualification dependency unresolved rather than substitute a copied summary.

## 4. Qualification receipt availability is part of recovery design

The separately governed receipt should not live only in an ephemeral provider message or one chat.

It needs:

- immutable or append-only durable identity;
- exact digest;
- retention at least as long as the installed release can claim qualification from it;
- privacy classification;
- supersession/revocation semantics;
- recoverable provider locator(s) without embedding sensitive fixture content in startup state.

A secondary mirror/archive may improve disaster recovery, but one source remains authoritative and mirrors do not become parallel truth.

## 5. 32 cases: sufficient floor, insufficient argument by itself

H5's proposed split:

- 8 behavior families;
- 3 unseen transforms per family = 24 isolated-candidate cases;
- 8 fresh in-situ Project cases;
- total 32.

This is not obviously too small for a **release qualification holdout** if the implementation already has strong deterministic regression coverage.

It is too small if the project treats `32/32` as evidence that the semantic/provenance space is broadly solved.

The quality depends much more on construction independence and relational tests than the raw number.

### Main risk: family-taxonomy overfit

A system can learn or accidentally encode:

`financial phrase -> non-risk`

`quoted risk word -> non-risk`

`AFFIRM+SELF -> risk`

without actually implementing provenance/branch semantics robustly.

It may pass paraphrases and surface domain transfers while failing when two axes interact in one trajectory.

## 6. Add cross-family metamorphic tests

A metamorphic test does not need a second semantic model. It asserts a relationship between two controlled cases whose difference is deliberately known.

Useful invariants:

### Assistant-frame insertion invariant

Take a baseline user statement with no independent risk evidence.

Variant adds an assistant question introducing the risk hypothesis, followed by user rejection/quotation.

Expected relationship:

> adding the assistant-originated frame and its rejected descendants must not increase Vera user-evidence support for the hypothesis.

### Stance flip

Hold lexical content/referent constant while changing only stance from quote/reject/mock to genuine affirm.

Expected:

- original unsupported branch remains unsupported;
- genuine affirmative version may open a new prospective branch.

### Referent swap

Hold alarming lexical content constant but change SELF to OTHER/ABSTRACT/quoted report.

Expected protected evidence relation changes without requiring the evaluator to invent a free-form risk label.

### Correction insertion

Start with an unsupported assistant lineage.

Add exact user correction.

Expected:

- originating lineage terminates;
- unrelated independently admitted evidence is unchanged.

### New-evidence-after-correction

Add a later genuine affirmative proposition after correction.

Expected:

- old branch stays terminated;
- new branch opens prospectively.

### Stale-context injection

Add old risk-bearing context to a current phrase whose explicit referent is non-risk.

Expected:

- current phrase semantic referent does not change;
- independently admissible historical evidence, if any, remains a separate safety input.

### AP toggle invariant

Same substantive evidence with AP enabled/disabled.

Expected protected safety/authority/privacy/memory/effect axes identical.

### Order/distractor invariant

Reorder unrelated non-authoritative distractors or add benign filler.

Expected controlling provenance/branch outcome unchanged.

These detect relational semantics, not memorized family labels.

## 7. Dynamic trajectories matter more than another pile of one-turn examples

At least several isolated cases should be multi-turn trajectories, not standalone prompts.

Suggested trajectory shapes:

1. unsupported assistant hypothesis -> user rejects -> assistant repeats -> user corrects -> later neutral topic;
2. unsupported hypothesis -> correction -> fresh runtime/recovery -> stale old context present -> no new evidence;
3. unsupported hypothesis -> correction -> later genuine new AFFIRM+SELF evidence;
4. quoted third-party risk text -> assistant misframes as self -> user clarifies referent;
5. ambiguous phrase -> explicit non-risk referent -> old independent historical risk context remains separately admissible;
6. correction continuity unavailable -> present semantics still correct -> no SAFE/RISK inference from missing record;
7. mixed user turn containing denial plus genuinely new affirmative proposition;
8. UNKNOWN provenance alarm phrase -> source remains unknown while platform-safe handling remains possible without USER_DIRECT promotion.

The evaluator knows the transformation/trajectory it generated, so it can test the required relational outcome without becoming a general semantic model.

## 8. Isolated candidate and in-situ Project are both necessary

H5 is right to reject `fresh chat = clean holdout` inside the same Project.

### Isolated candidate stratum

Purpose:

- test the exact frozen candidate without Project-history contamination;
- establish reproducible qualification against withheld cases.

The isolation claim must bind exact candidate/settings/files/runtime and explain what historical/project context is absent.

### In-situ stratum

Purpose:

- test whether real Project history, memory surfaces, and recovery context cause contamination or precedence regressions;
- not a clean holdout in the statistical sense.

These two strata answer different questions and should report separately.

A release can pass isolated semantics while fail in-situ contamination. That is a real failure, not a contradictory test result.

## 9. Annotation correctness must remain NOT_VERIFIED without a safe receipt

If the observable runtime exposes only final assistant output, the evaluator may qualify black-box behavior.

It may not infer that internal/structured fields were correct merely because the answer looked right.

For annotation-layer qualification, require an exposed privacy-safe receipt containing the necessary closed fields or digests, e.g.:

- proposition/evidence locator;
- origin;
- stance;
- referent subject/domain;
- branch relation/ID as opaque identity;
- correction/admissibility result;
- policy version;
- no intimate transcript copied merely for audit convenience.

If that surface is unavailable, report:

`BLACK_BOX_BEHAVIOR = QUALIFIED`

`ANNOTATION_LAYER = NOT_VERIFIED`

rather than hallucinating instrumentation from output quality.

## 10. Avoid evaluator feedback leakage

Qualification fixtures and expected outputs should not become training/prompt material for the same candidate before qualification completes.

If a candidate fails and is repaired using a revealed holdout, those exact cases become regression/training evidence and a new holdout tranche is required for the next external qualification.

Otherwise "unseen transform" becomes a decorative adjective after the first failure cycle.

## 11. Recommended qualification receipt summary

The separate receipt can remain compact while preserving auditability:

```text
qualification_receipt_id
policy_version
candidate/settings/project digests
isolation method
isolated_total/pass/fail
in_situ_total/pass/fail
black_box_status
annotation_status
metamorphic_invariants_count/pass/fail
trajectory_count/pass/fail
privacy_class
fixture_manifest_digest   # not fixture contents
result_manifest_digest
supersedes/revokes refs
record_time
```

Detailed fixture/result evidence can live in a separately protected artifact keyed by digest if privacy requires tighter access.

## Final disposition

- **Approve** separate behavioral qualification receipt + installation reference/digest/binding.
- **Reject** copying full qualification evidence into installation as the default architecture.
- **Require** dependency availability/digest/currentness verification so the reference cannot dangle silently.
- Treat H5's 32-case plan as a reasonable floor if it includes cross-family metamorphic relationships and multi-turn trajectories; count alone is not persuasive.
- Preserve separate black-box and annotation-layer verdicts.
- Preserve deterministic CI, behavioral qualification, annotation qualification, and installation as distinct evidence classes even if one release report summarizes them.

No candidate, evaluator, native Project file, database, installation state, deployment, credential, merge, paid-service configuration, or canonical memory was modified by this research.