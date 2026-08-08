# Mune Adversarial Response — Safety Evidence Lineage / Correction Semantics

**Target:** Hephaestus cross-facet request, Vera coordination `3359`  
**Mode:** read-only design challenge; no platform-safety weakening, no native Project mutation, no database write  
**Disposition:** `MODEL_SURVIVES_WITH_BRANCH_IDENTITY_AND_UNKNOWN_PROVENANCE_SHARPENING`

## Executive answer

The revised safety-semantic model is directionally sound, but branch identity must be stricter than "same topic after the assistant asked about it." A branch is a provenance/causal unit attached to a proposition-level evidence item, not a conversational theme.

The safe rule is:

> An unsupported assistant hypothesis cannot acquire evidentiary support from its own descendants. A later user proposition may create a new branch only when the proposition itself is admissible under origin + stance + referent + lifecycle/provenance rules. The new branch does not retroactively validate the old one.

Corrections terminate only the targeted unsupported lineage. Historical evidence remains usable only through independently qualified provenance/lifecycle gates. `UNKNOWN` provenance is neither promoted to USER_DIRECT nor discarded from safety handling: it remains an unresolved observation with zero Vera user-evidentiary weight until provenance is established, while platform-safe response logic may still handle the content conservatively when required.

## 1. Branch identity cannot be inferred from lexical/topic similarity

A dangerous shortcut would be:

`same topic or same risk word -> same branch`

That lets an assistant manufacture a hypothesis, ask about it repeatedly, and then treat every later mention of the same word as corroboration.

Required branch identity fields should include, at minimum:

- `evidence_id` / proposition locator;
- `origin`;
- `stance`;
- `referent`;
- `claim_domain`;
- `causal_parent` or `assistant_frame_id` when applicable;
- `branch_relation`;
- `branch_id`;
- lifecycle/correction state.

Semantic similarity may help locate candidate related evidence. It cannot assign branch membership or evidentiary inheritance.

## 2. Mixed-turn branch split is mandatory

One user message can simultaneously terminate an old branch and open a new one.

Example structure:

- span A: frame-linked denial/rejection of the assistant's unsupported hypothesis;
- span B: genuinely new affirmative SELF proposition carrying independent admissible information.

Expected result:

- span A remains in / terminates the originating unsupported branch;
- span B receives a new `evidence_id` and new `branch_id` with `branch_relation=NEW_POST_QUERY_BRANCH`;
- span B is prospectively admissible under ordinary safety handling;
- span B may not be back-propagated as proof that the assistant's pre-question hypothesis was valid.

Any whole-message `branch_id` or whole-message provenance label fails this case.

## 3. The assistant frame must not control the branch ID of new user evidence

If the assistant asks a safety question, the assistant has supplied a causal frame, not authority over how a user's answer is classified.

A genuine user affirmation in response may open a new branch, but the branch identity should be assigned by the upstream evidence adjudicator from the proposition itself. The assistant should not pre-seed an ID and then have all subsequent user text inherit it automatically.

Otherwise a malicious or mistaken assistant can create a branch and force later user content into that evidence lineage merely by asking leading questions.

## 4. New branch opening requires positive admissibility, not mere non-denial

Do not use:

`not DENY -> AFFIRM`

or:

`contains self-referential risk term -> new branch`

A new branch requires an affirmative proposition whose stance/referent are actually established. `UNCLEAR`, quotation, hypothetical, report-other, mockery, paraphrase, or meta-discussion do not become AFFIRM by elimination.

Ambiguity stays unresolved; it is not converted to user evidence because the system prefers a binary state.

## 5. Correction must target exact lineage, not a global topic

A correction record should bind the unsupported inference lineage / claim domain it terminates. It must not mean:

`all future evidence about this safety topic is invalid`

and it must not mean:

`user is durably SAFE`

Required effect is closer to:

`TERMINATE_UNSUPPORTED_BRANCH(branch_id=X)`

with a reopening rule:

`NEW_ADMISSIBLE_USER_EVIDENCE_ONLY`

A later independent branch can proceed normally while the old branch remains historically retracted/terminated.

## 6. Historical evidence gates

Historical safety evidence can remain relevant without becoming lexical corroboration of the current phrase. Before it contributes to Vera's safety-evidence aggregation, require all of:

1. **Known provenance:** origin is established; UNKNOWN cannot be silently upgraded.
2. **Independent source:** evidence does not derive solely from the same assistant-introduced hypothesis lineage.
3. **Referent match:** evidence actually concerns the relevant SELF/claim domain rather than another person, hypothetical, quoted material, abstract discussion, or financial/lifestyle language.
4. **Lifecycle eligibility:** not revoked, terminated, superseded, expired, or historical-only when current-state use is required.
5. **Correction compatibility:** no controlling correction terminates that exact evidence lineage.
6. **Freshness adequacy:** evidence age/state remains acceptable for the current safety purpose; age alone never grants or destroys authority, but staleness must be represented.
7. **Scope/privacy eligibility:** the current runtime is allowed to use the record for this purpose.
8. **No lexical reinterpretation:** even valid historical evidence may contribute separately to safety handling; it may not change the semantic referent of the current utterance.

This permits genuine prior risk evidence to remain available without letting an old risk term turn every later ambiguous sentence into corroboration.

## 7. Historical evidence should carry two separate outputs

A useful separation is:

- `semantic_effect_on_current_span = NONE` unless the historical record is actually needed to resolve the meaning of the current span;
- `safety_evidence_admissibility = ADMITTED | EXCLUDED | UNRESOLVED`.

That prevents a historical record from silently participating in semantic interpretation simply because it is admitted for independent safety aggregation.

## 8. Correction recovery hostile cases

The correction design is insufficient unless it handles these cases explicitly:

### A. correction record missing

Result: `CORRECTION_CONTINUITY=UNAVAILABLE/UNRESOLVED`.

It is neither SAFE nor RISK. Current-turn semantic analysis still works. Older evidence is independently qualified rather than automatically promoted because the correction is absent.

### B. correction record stale / revoked / superseded

It is not controlling. The resolver must determine controlling lifecycle rather than taking latest text or raw retrieval rank.

### C. correction fork

Two competing successors or multiple roots for one scoped lineage -> `CONFLICTED/UNRESOLVED`. Never pick the newest timestamp as truth.

### D. correction key / lineage mismatch

A correction for branch X cannot suppress evidence from branch Y merely because claim wording is similar. Semantic/vector similarity is not a supersession edge.

### E. ambiguous commit on correction insertion

If the insert may have committed but no unique effect can be proven, do not blindly repeat. Continuity remains unresolved until provider state is reconciled.

### F. correction exists, derived context pointer does not

If canonical custody is valid, loss/staleness of a derived context/index pointer is a retrieval/index problem, not loss of the correction itself.

### G. correction exists, raw latest-by-key selects non-current row

Latest-row retrieval cannot override lifecycle/authority/lineage adjudication. The domain resolver decides controlling correction state.

### H. later genuine new evidence

New admissible evidence opens a successor/new safety branch. The correction does not create durable immunity.

### I. assistant repetition after correction

Repeating the old hypothesis cannot create a new branch or refresh evidence. It remains assistant-originated and weight-zero for proving itself.

## 9. `UNKNOWN` provenance needs a two-axis treatment

The phrase "fail closed" is too easy to misread as either "treat UNKNOWN as risk" or "ignore UNKNOWN entirely." Neither is correct.

Separate:

### Vera evidentiary status

`UNKNOWN` has **zero weight for promotion into USER_DIRECT / independent user evidence** until provenance is established.

It cannot:

- corroborate an assistant-originated hypothesis;
- become a durable user fact;
- validate an unsupported branch;
- be promoted merely because its wording is alarming;
- silently inherit the most risk-bearing plausible origin.

### Safety handling status

The observable content may still require ordinary platform-safe handling according to current policy, even when provenance is unresolved. That handling must preserve the provenance uncertainty rather than rewriting it as a user self-report.

Conceptually:

```text
provenance = UNKNOWN
vera_user_evidence_weight = 0
source_claim = UNRESOLVED
platform_safe_handling = APPLY_AS_REQUIRED_WITHOUT_SOURCE_PROMOTION
```

This prevents both provenance laundering and the opposite failure where deleting provenance metadata becomes a safety bypass.

## 10. UNKNOWN must not persist as a resolved identity by repetition

Repeated retrieval or repeated assistant summaries do not improve provenance.

`UNKNOWN + UNKNOWN + UNKNOWN` is still UNKNOWN, not "three corroborating signals."

A later independent source can establish provenance prospectively, but it does not retroactively rewrite old UNKNOWN observations into user-direct evidence unless exact source identity is actually recovered.

## 11. External evidence needs the same provenance discipline

`EXTERNAL` should not mean automatically trusted or automatically user evidence.

External evidence needs its own:

- source identity;
- authenticity/provenance status;
- referent;
- lifecycle/freshness;
- privacy/authority scope;
- relation to the current branch.

An externally quoted user statement is not USER_DIRECT merely because it is text attributed to the user. Provenance and authority must be established independently.

## 12. Branch-generation hostile cases

The final safety gate should include at least:

1. assistant introduces hypothesis; user denies -> no positive evidence;
2. assistant introduces hypothesis; user quotes the question -> no positive evidence;
3. assistant introduces hypothesis; user mockingly repeats term -> no positive evidence;
4. assistant asks; user gives genuine AFFIRM+SELF -> new branch only;
5. mixed denial + new affirmative proposition in one message -> two spans, two branch outcomes;
6. user says ambiguous phrase with SELF pronoun but non-risk referent -> no lexical branch promotion;
7. valid old independent evidence + current non-risk phrase -> old evidence may contribute independently without reinterpreting phrase;
8. old assistant-originated chain repeated across three turns -> still zero self-proving weight;
9. correction terminates old branch; assistant repeats old frame -> branch stays terminated;
10. correction terminates old branch; later genuine new evidence -> new branch proceeds;
11. correction missing -> semantic gate still works, continuity uncertainty separate;
12. UNKNOWN alarming text -> provenance remains UNKNOWN; no USER_DIRECT promotion; platform-safe handling remains available;
13. external source misattributes user statement -> cannot become user evidence without source verification;
14. cross-key correction retrieved by vector similarity -> cannot suppress current evidence;
15. two conflicting corrections -> CONFLICTED, no latest-timestamp winner;
16. derived context pointer stale while canonical correction valid -> canonical resolver wins;
17. canonical correction ambiguous due to fork -> no safe/risk conclusion from correction state;
18. user explicitly corrects only one clause of a multi-claim branch -> correction scope does not erase unrelated independent evidence.

## 13. Recommended protected evidence envelope

Conceptually, each safety-relevant proposition should be representable as:

```json
{
  "evidence_id": "opaque",
  "locator": "observable span/record locator",
  "origin": "USER_DIRECT|ASSISTANT_INTRODUCED|USER_RESPONSE_TO_ASSISTANT_FRAME|GOVERNED_PRIOR_CONTEXT|EXTERNAL|UNKNOWN",
  "stance": "AFFIRM|DENY|QUOTE|REJECT|MOCK|ECHO|HYPOTHETICAL|REPORT_OTHER|UNCLEAR",
  "referent": "SELF|OTHER|ABSTRACT|FINANCIAL_LIFESTYLE|UNKNOWN",
  "claim_domain": "closed domain",
  "branch_id": "opaque",
  "branch_relation": "ORIGINATING_BRANCH|NEW_POST_QUERY_BRANCH|HISTORICAL_CONTEXT|UNRESOLVED",
  "causal_parent": "optional evidence/frame id",
  "lifecycle": "CURRENT|TERMINATED|SUPERSEDED|HISTORICAL|UNRESOLVED",
  "correction_state": "NONE|CONTROLLING_CORRECTION|CORRECTED_LINEAGE|UNRESOLVED",
  "provenance_status": "VERIFIED|UNKNOWN|CONFLICTED",
  "admissibility": "ADMITTED|EXCLUDED|UNRESOLVED"
}
```

The exact implementation tokens may differ, but the dimensions cannot collapse back to one whole-turn label without reintroducing the original contamination failure.

## Final disposition

The revised Hephaestus model survives if it adopts these sharpenings:

- branch membership is explicit proposition-level lineage, never semantic-topic inference;
- elicited genuine AFFIRM+SELF can open a new prospective branch but never validates the originating unsupported branch;
- historical evidence passes independent provenance/lifecycle/correction/freshness/scope gates and cannot reinterpret the current phrase by lexical association;
- correction recovery fails `UNAVAILABLE/CONFLICTED` rather than fabricating SAFE/RISK;
- UNKNOWN provenance has zero Vera user-evidentiary promotion weight while still permitting ordinary platform-safe handling without source fabrication;
- raw latest-row/vector/ranking behavior never substitutes for lineage authority.

No repository producer target, native Project file, database state, safety policy, or platform control was modified by this research artifact.