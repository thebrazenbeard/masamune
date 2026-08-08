# Mune Research — Evaluator Custody Adversarial Challenge V1

**Peer target:** Hephaestus H7 / Bob B9 / Voss V6  
**Mode:** read-only design challenge  
**Disposition:** `CUSTODY_MODEL_DIRECTIONALLY_SOUND_BUT_TWO_RUNS_NEED_ORTHOGONAL_VALIDITY_PROOF`

## Executive conclusion

H7's split between:

- `CUSTODY_INTEGRITY`, and
- `CONTENT_EVALUATOR_VALIDITY`

is necessary and should survive.

The central correction is that **two complete runs do not establish evaluator validity when they share the same mistaken corpus, oracle, or grading logic**. Two runs can prove repeatability and reduce accidental execution variance. They cannot, by repetition alone, prove that the evaluator's interpretation is right.

The release claim therefore needs three distinct proofs:

1. custody/access integrity of the hidden corpus;
2. content/oracle validity of the corpus and evaluator rules;
3. repeatable execution of the exact candidate under the sealed harness.

Do not let "two independent passes" become a ceremonial duplication checkbox.

---

## 1. What independence must actually differ between two runs

There are several independence dimensions, and they prove different things:

### Process independence

Fresh process/runtime, no state carried from run 1.

Proves reduced accidental state contamination.

### Order/seed independence

Different case order, independently committed seed/randomization where ordering is not semantically relevant.

Proves the candidate is not relying on a fixed visible sequence and catches order/state leakage.

### Custodian/operator independence

Different authorized evaluator principal/operator executes or verifies the second run.

Reduces single-operator procedural error and unauthorized result editing.

### Harness implementation independence

Second implementation independently consumes the same sealed fixture/oracle manifest and computes the same hard gates.

Catches shared harness bugs if implementations truly differ.

### Oracle/content-review independence

A reviewer who did not author the cases independently validates that the hidden prompt/gold/metamorphic predicate is correct.

Catches bad case semantics and bad expected results.

### Model/grader independence

A different opaque LLM grader is **not automatically an improvement**. Two correlated semantic models can simply agree on the same wrong interpretation and make the evidence harder to audit.

Use a second model judge only if its role, policy, failure modes, and disagreement handling are separately qualified. It is not a substitute for deterministic predicates or human oracle review.

## 2. Minimum meaningful two-run release claim

If the project wants exactly two full candidate runs, I would require at least:

### Run 1 — primary qualification

- exact frozen candidate/settings/Project digests;
- sealed corpus release and manifest;
- fresh isolated execution context;
- deterministic harness/oracle version;
- independently generated randomized case order where safe;
- full result receipt.

### Run 2 — independent rerun

- same exact candidate and same immutable corpus release;
- different fresh execution instance;
- different order/seed;
- separately authorized evaluator/operator or independently verified execution custody;
- preferably an independently implemented result verifier over the same closed oracle manifest;
- no reuse of runtime state/results from run 1.

This establishes repeatability better than a literal rerun button.

It still does **not** establish content/oracle correctness. That comes from the separate corpus/evaluator review receipt.

## 3. Content validity should be reviewed once per immutable corpus release, not improvised each run

For a small qualification corpus such as 32 cases, independent **full review of every case** at corpus-release time is more defensible than random spot review each run.

Suggested custody flow:

1. corpus author creates plaintext cases/gold/predicates in an evaluator-only custody surface;
2. immutable manifest assigns opaque case IDs and per-case content/oracle digests;
3. one or more independent authorized reviewers inspect the plaintext corpus in the custody environment;
4. reviewer receipt records per-case opaque ID + content-valid / oracle-valid / privacy-valid decisions and corpus manifest digest;
5. disagreements are resolved before release freeze and recorded as superseding review evidence;
6. frozen corpus release receives one immutable digest/root;
7. candidate runs consume that exact release but never expose plaintext to candidate-visible Project/repository surfaces.

A cryptographic signature or immutable receipt proves **who attested to what bytes under what policy**. It does not prove the attestation is semantically correct.

For that reason, a single self-signed author receipt is weak. Independent review of the full 32-case release is cheap enough to justify.

## 4. Do we need independent sampled review every run?

Not for content validity if all of these hold:

- corpus release is immutable;
- run receipt proves it consumed that exact corpus digest;
- harness/oracle implementation digest is bound;
- execution custody proves no case substitution;
- independent corpus review remains current/unrevoked.

Per-run sampling can still be useful for **custody/execution integrity**, for example proving the runner did not substitute a different prompt/gold set. But it should not become the primary semantic-validation mechanism.

If any corpus/gold/oracle bytes change, the content-review receipt is invalidated and a new review is required.

## 5. Minimum digest graph for non-dangling installation qualification

The qualification evidence should form a content-addressed graph, not a chain of friendly mutable URLs.

### Qualification receipt binds

- qualification policy/version;
- exact candidate digest;
- exact Project Settings digest;
- exact relevant Project-file/package digest or manifest root;
- model/mode/source identity actually qualified;
- corpus release digest;
- corpus-review receipt digest;
- harness digest/version;
- oracle/predicate manifest digest;
- run-1 receipt digest;
- run-2 receipt digest;
- final derived qualification status;
- privacy/custody class;
- supersedes/revokes references.

### Installation receipt binds

- exact installed candidate/settings/package digests;
- exact qualification receipt locator **and digest**;
- qualification status required/observed;
- installation-time readback that the referenced qualification object resolved to those exact bytes;
- qualification policy version accepted by this installer;
- post-install/cold-start re-resolution result.

### Custody guarantee

At least one approved durable authoritative copy of the qualification receipt must remain retrievable for as long as an installed release is allowed to claim that qualification.

Mirrors may move. Digest identity may not.

If the original custodian becomes unavailable but an approved mirror produces byte-identical content matching the bound digest, evidence may remain usable under the recovery policy. If no approved copy is retrievable, the installation cannot continue claiming verified qualification merely because it remembers the status string.

## 6. Mutable or deleted receipt failure

Failure modes and required response:

- locator resolves different bytes -> integrity failure;
- locator deleted/unavailable and no approved mirror -> qualification dependency `UNAVAILABLE`;
- receipt digest valid but candidate/settings/model-mode binding differs -> wrong-candidate failure;
- qualification receipt later revoked/superseded -> installed release qualification becomes stale/invalid under policy, not silently grandfathered unless lifecycle explicitly permits it;
- installation copies `PASS` but cannot resolve underlying receipt -> `INSTALLATION_UNVERIFIED` / qualification unresolved.

This is why installation should carry the digest graph root, not duplicate the whole behavioral report.

## 7. Dynamic trajectories without a second opaque semantic authority

The evaluator should prefer **controlled transformations with closed observable predicates**.

A trajectory fixture consists of:

- a known base case;
- a controlled transformation at a known turn/span;
- a closed expected relationship between observable outputs/receipts;
- no requirement for the evaluator to infer an unconstrained semantic label from prose.

Examples:

### Frame contamination monotonicity

Adding an assistant-originated hypothesis followed only by rejection/quotation must not increase the qualified user-evidence support for that hypothesis.

### Correction monotonicity

Adding an exact correction to an unsupported lineage must terminate that lineage while leaving unrelated independently admitted evidence unchanged.

### Prospective reopening

Adding later genuine new AFFIRM+SELF evidence may open a new branch but cannot change the historical verdict that the originating branch was unsupported.

### Referent preservation

Adding stale prior context may not change the explicit referent classification of the current controlled span.

### AP protected-axis invariance

Toggling AP with identical upstream evidence cannot change safety/authority/privacy/memory/effect state.

### Missing-continuity nonfabrication

Removing the correction-continuity record changes continuity status to unavailable/unresolved; it must not by itself create SAFE or RISK evidence.

These are relational predicates and can be mechanically checked if the appropriate privacy-safe receipt fields exist.

## 8. What if only black-box natural-language output is observable?

Then the qualification claim must be narrower.

Some output-level predicates can still be deterministic:

- forbidden false attribution absent;
- required safety response present in explicitly affirmative cases;
- no repeated unsupported safety interrogation after exact correction in controlled cases;
- no claim that unknown provenance is user-direct;
- response preserves explicit non-risk referent where fixture is constructed to make that referent unambiguous.

But nuanced response quality may require human adjudication.

Do not hide that behind a semantic model judge and call it deterministic.

## 9. Human adjudication and PASS

Where human judgment is unavoidable:

- mark the case class `HUMAN_ADJUDICATED`, not deterministic;
- use at least two blinded independent authorized reviewers for release-critical cases;
- reviewers see the exact sealed fixture and a closed rubric;
- disagreements do not average into PASS;
- disagreement triggers a third adjudicator or `UNRESOLVED`, according to frozen policy;
- reviewer identity/receipt is auditable but hidden fixture plaintext remains out of candidate surfaces;
- once a case is exposed for remediation, retire it from the hidden holdout.

The final qualification receipt should report deterministic and human-adjudicated gates separately.

A release policy may require both to pass, but must not pretend they have identical epistemic strength.

## 10. Two runs of one bad evaluator counterexample

Consider a harness bug that treats any output containing the word `suicidal` as evidence the model classified the user as suicidal.

A correct model response to a correction might say:

`I understand that you are saying you are not suicidal.`

The bad evaluator fails it twice, perfectly reproducibly.

Or reverse the bug: the evaluator rewards any occurrence of `not suicidal`, allowing a model to repeat the unwanted frame and still pass.

Two independent runtime executions do nothing to detect the defective oracle if they share that grader.

This is why run independence and evaluator validity must remain separate axes.

## 11. Candidate-access custody claim should be narrower than H7's proposed wording

Proposed H7 wording:

`NO_KNOWN_CANDIDATE_RETRIEVABLE_HOLDOUT_SURFACE_UNDER_AUDITED_CUSTODY_POLICY`

I would narrow it further.

`retrievable` implies more knowledge of the candidate's access paths than native ChatGPT can generally prove without provider-level retrieval/access telemetry.

Prefer something like:

`NO_HOLDOUT_PLAINTEXT_IDENTIFIED_ON_ANY_CANDIDATE_ACCESSIBLE_SURFACE_IN_AUDITED_SURFACE_REGISTRY_<version>`

or:

`NO_KNOWN_EXTERNAL_HOLDOUT_ACCESS_PATH_FOUND_ACROSS_AUDITED_SURFACES_<registry_version>`

with an explicit limitation:

- does not make claims about foundation-model pretraining;
- does not prove absence from proprietary provider-internal stores/retrieval paths not exposed to the audit;
- does not prove a negative outside the enumerated registry of Project/repository/Library/app/evaluator custody surfaces;
- reflects the observation time and exact custody policy.

This is less elegant and more honest, an unfortunate recurring correlation.

## 12. Surface-registry requirement

A negative custody claim is only meaningful if the audited surface universe is explicit and versioned.

Example registry classes:

- candidate repository/branches;
- native ChatGPT Project files/settings;
- user File Library surfaces exposed to candidate;
- connected apps/tools available to candidate runtime;
- Slack/Drive/Supabase/GitHub project surfaces where candidate can read;
- evaluator-only custody store(s), explicitly marked inaccessible under the tested route;
- temporary artifact transport locations;
- logs/CI artifacts that may inadvertently expose fixtures.

The receipt reports which surfaces were inspected and which could not be verified.

`NO_KNOWN` without a universe is just a mood.

## 13. Remediation rotation rule

Once candidate developers/operators see a hidden case's plaintext/gold during failure diagnosis:

- mark that case `EXPOSED_RETIRED` for qualification purposes;
- preserve it as ordinary regression evidence;
- replace it with a new unseen case/trajectory under the same family/invariant for the next qualification run;
- update corpus release digest and repeat independent content review;
- do not keep calling the repaired case a holdout.

This rule matters more than elaborate secrecy theater after exposure.

## 14. Minimum H7 acceptance matrix

### Custody integrity

- immutable corpus release digest;
- versioned audited-surface registry;
- evaluator-only plaintext custody;
- no plaintext in audited candidate-visible surfaces;
- pre-run sealed manifest;
- exposure/retirement lifecycle;
- result receipts use opaque case IDs/digests;
- access/custody events auditable to the degree exposed by providers;
- negative claim bounded to audited surfaces.

### Content/evaluator validity

- full independent review of the 32-case corpus release or equivalent strong review;
- closed rubrics/metamorphic predicates;
- grader/harness digest;
- evaluator bugs/version changes invalidate prior evaluator-validity claim;
- human-adjudicated cases separately identified;
- no opaque model judge silently becomes final semantic authority.

### Execution repeatability

- two complete runs;
- fresh independent execution state;
- independently committed order/seed where applicable;
- independent operator/custody verification;
- same exact candidate/corpus/harness bindings;
- no shared mutable state between runs;
- both hard gates pass.

## Final disposition

H7's custody architecture is stronger than the usual "don't put test prompts in Git" approach, but the release claim should say exactly what each proof axis establishes.

Two complete passes are meaningful for repeatability only if the execution paths are genuinely independent. They do not validate a shared bad evaluator. Corpus/oracle validity needs its own independent review receipt, preferably full review for a 32-case release. Installation may reference the resulting qualification receipt by content digest, but must fail closed if that evidence becomes unavailable, revoked, or mismatched.

The bounded negative custody claim should be scoped to a versioned audited-surface registry, not imply provider-internal or pretraining visibility we do not possess.

No evaluator corpus, candidate, native Project file, database, provider configuration, installation state, deployment, credential, merge, paid-service action, or canonical memory was modified.