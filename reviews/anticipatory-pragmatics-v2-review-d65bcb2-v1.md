# Mune Independent Review: R9A0 Anticipatory Pragmatics V2

**Reviewer:** Mune
**Candidate repository:** `thebrazenbeard/masamune`
**Exact candidate head:** `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`
**Controlling artifact:** `design/R9A0_ANTICIPATORY_PRAGMATICS_DATA_CONTRACT_V2.md`
**Normative companion:** `design/R9A0_ANTICIPATORY_PRAGMATICS_DATA_CONTRACT_V1.md` V1.1 at the same head
**Verdict:** `APPROVED_DATA_CONTRACT`
**Persistent schema approved/required:** No
**Additional inference calls approved/required:** 0
**Native implementation authorized by this review:** No

## Scope

This rereview evaluates the exact immutable V2 candidate against Mune findings `MUNE-AP-001` through `MUNE-AP-005` and the prior twelve-family adversarial framework. It is a data-contract approval, not approval to mutate native R9A0 Project files or release artifacts.

The `masa` branch was verified identical to the bound candidate head during review. The transition from V1.1 head `a79b1dea515569254fd49a885564c554481027e4` to `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14` adds only the explicit V2 Edge and AP controlling artifacts.

The claimed native enforcement surfaces were independently verified to exist at current native head `6a568d35c142dc37ea41a0209cdb1f295949f767`: `project/VERA_R9A0_NATIVE_CONTRACT.json`, `schemas/native-project/vera-r9a0-native-contract.schema.json`, and `scripts/validate_r9a0_project.py`. The current schema uses `additionalProperties: false`, so a future AP block necessarily requires an explicit schema/validator change rather than silently entering the contract.

## Finding closure

### MUNE-AP-001: overly broad current-chat precedence

**CLOSED.** V2 limits same-chat precedence to user-explicit or authoritative evidence governing the same presentation dimension. Assistant guesses, inferred emotion, model personality claims, repeated assistant wording, and unsourced interpretations do not gain authority from recency.

### MUNE-AP-002: free-text turn-local hypotheses

**CLOSED.** The free-text `turn_local_hypotheses` channel is removed. V2 permits only closed-enum presentation hints with evidence locators. Any future hypothesis mechanism requires a separately reviewed closed enum and hostile tests.

### MUNE-AP-003: mutable or incomplete protected axes

**CLOSED.** V2 fixes a non-editable twelve-axis set including factual conclusion, safety, authority, privacy, correction precedence, provenance, non-persuasion, durable-memory admission, external-effect authorization, epistemic status, unknown/unresolved disclosure, and persistence classification. Any AP-induced divergence discards the full hint set.

### MUNE-AP-004: conceptual controller not bound to native enforcement surfaces

**CLOSED AT DATA-CONTRACT LEVEL.** V2 binds a later authorized implementation to the existing R9A0 runtime, native contract, schema, validator, and native tests. Those surfaces exist and are suitable enforcement points. The current native contract does not yet contain AP, and the schema's closed property set means implementation cannot be faked by an undeclared field.

The later native implementation must actually add the AP contract/schema/validator/test assertions and pass exact-head CI before this design can become release behavior. That work remains with the native architecture/design-freeze lane and is not performed by this review.

### MUNE-AP-005: risk/artifact fields not explicitly upstream read-only

**CLOSED.** V2 makes speech act, objective, risk, artifact mode, authority state, and safety state runtime-owned read-only inputs. AP may consume them for permitted presentation behavior but may not classify, downgrade, upgrade, or mutate them.

## Adversarial result

The V2 contract preserves the approved no-new-store direction and now closes the main side channels that could have converted presentation policy into hidden profiling or substantive decision authority. Evidence admission is provenance-bound; personalization hints are closed; protected outcomes are fixed; upstream control state is read-only; AP expires at end of turn; and additional model/classifier/vector/Edge dependencies remain prohibited.

The twelve-family hostile evaluation framework remains required for implementation. In particular, implementation must demonstrate zero protected-axis divergence, zero assistant-generated evidence promotion, zero free-text hypothesis acceptance, zero upstream risk/authority/safety mutation, zero autonomous persistence, and zero added inference/API calls.

## Approval boundary

`APPROVED_DATA_CONTRACT` means:

- approve the V2 AP architecture and its no-new-persistent-store / zero-extra-inference decision;
- approve the named native contract/schema/validator/test surfaces as the intended enforcement route;
- do not treat this review as native implementation, release integration, installation, deployment, or Project-file mutation approval;
- future native implementation remains subject to Hephaestus/Bob/Vera/Voss design-freeze and exact-head validation requirements.

Mune's independent AP V2 rereview is complete for exact head `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`.