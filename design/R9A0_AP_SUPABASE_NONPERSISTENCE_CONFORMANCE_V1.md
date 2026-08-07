# R9A0 Anticipatory Pragmatics Supabase Non-Persistence Conformance V1

**Author lane:** Masa
**Status:** NON_EXECUTING_CONFORMANCE_PROOF_READY_FOR_REVIEW
**Approved AP candidate:** `design/R9A0_ANTICIPATORY_PRAGMATICS_DATA_CONTRACT_V2.md`
**Bound AP candidate head:** `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`
**Independent AP verdict:** Mune `APPROVED_DATA_CONTRACT`
**Persistent schema change required:** No
**Edge Function required:** No
**Additional inference/API calls:** 0
**Paid runtime dependency:** None
**Hosted mutation authorized:** No

## Conclusion

Anticipatory Pragmatics V1/V2 conforms to the R9A0 Supabase boundary **without adding any persistent Supabase object or write path**.

The AP contract is request-scoped response-policy plumbing. It may consume current-turn state and evidence that the ordinary R9A0 runtime has already admitted or retrieved for the present task. It does not own, persist, index, promote, or independently retrieve that evidence.

No AP-specific table, view, function, trigger, RLS policy, vector index, Storage bucket, Edge Function, queue, cron job, Realtime channel, Auth object, user profile, shadow-memory record, embedding, model call, or durable preference record is required.

The conformance verdict is:

`CONFORMS_NO_NEW_PERSISTENCE`

## Evidence baseline

This proof is bound to existing R9A0 repository evidence rather than hypothetical future state.

### Native contract

At native head `6a568d35c142dc37ea41a0209cdb1f295949f767`, `project/VERA_R9A0_NATIVE_CONTRACT.json` already defines the active surfaces as:

- Supabase;
- GitHub;
- Google Drive;
- native Project files.

It also requires history-sensitive refresh, evidence locators, abstention when unresolved, and prohibits treating legacy Basic Memory as an active dependency.

AP consumes those existing runtime decisions; it does not add another retrieval authority.

### Retrieval contract

`project/VERA_R9A0_RETRIEVAL.md` already requires the ordinary runtime to:

- refresh relevant exposed evidence for history-sensitive claims;
- identify evidence by sequence, commit, path, receipt, document ID, or other locator;
- distinguish fact from inference;
- preserve conflicts and supersession;
- abstain when retrieval remains unresolved.

AP is downstream of this contract. It may use already-admitted evidence to choose permitted presentation hints, but it cannot cause an otherwise-unneeded broad personal retrieval solely for personalization.

### Current database slice

At accepted database head `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`, the R9A0 database architecture is limited to:

- `r9a0_governance`;
- `r9a0_coordination`;
- `r9a0_api`;
- the dedicated `r9a0_owner` role.

The database architecture explicitly excludes autobiographical-memory admission, Edge Functions, Storage, Realtime, queues, and vector features.

AP V2 does not require any change to that database slice.

## Boundary map

The AP envelope is ephemeral. Each input maps to an existing governed source or upstream controller state.

| AP input | Existing source | AP may do | AP may not do | New persistence |
|---|---|---|---|---|
| current speech act | current runtime controller | select presentation posture | rewrite objective/authority | none |
| current objective | current runtime controller | order supported information | change task objective | none |
| risk class | upstream safety/runtime controller | choose careful rendering | classify/downgrade/upgrade risk | none |
| artifact mode | upstream runtime | avoid incompatible rendering | change artifact authorization | none |
| authority state | upstream authority controller | avoid suggesting unauthorized effects | grant/revoke authority | none |
| safety state | upstream safety controller | select permitted rendering | weaken safety boundary | none |
| current user instruction/correction | current turn/chat | apply scoped presentation preference | persist it automatically | none |
| same-chat user-explicit evidence | current conversation | reuse relevant active terminology/preferences | treat assistant guesses as user evidence | none |
| authoritative project state | native files / freshly retrieved governed surface | use directly relevant terms/context | copy project state into an AP store | none |
| verified durable context | existing governed durable source | use only when independently relevant | broaden retrieval for cosmetic personalization | none |
| historical evidence | governed historical source | historical context only | silently drive current personalization | none |

AP therefore introduces no new authoritative data owner. It is a pure consumer of inputs already owned elsewhere.

## Read path only

AP's allowed dataflow is conceptually:

```text
current request
  -> ordinary runtime locks referent/objective/correction/scope
  -> ordinary safety/authority classification
  -> ordinary retrieval, only if independently required
  -> admitted evidence with provenance
  -> ephemeral AP presentation envelope
  -> protected-axis invariance check
  -> one response generation
  -> discard AP envelope
```

There is no AP persistence leg.

Forbidden AP dataflow:

```text
AP -> INSERT profile
AP -> UPDATE preference
AP -> append memory
AP -> create embedding
AP -> persist inferred mood
AP -> call Edge Function
AP -> call second LLM/classifier/sentiment service
AP -> write coordination merely because a hint was used
```

If any implementation adds one of those legs, it is not conforming V1/V2.

## Supabase object conformance

For AP V1/V2, the required delta is exactly:

```text
schemas: 0
roles: 0
tables: 0
views: 0
materialized views: 0
functions/RPCs: 0
triggers: 0
RLS policies: 0
indexes: 0
pgvector indexes: 0
Storage buckets: 0
Edge Functions: 0
Realtime publications/channels: 0
queues: 0
cron jobs: 0
Auth users/roles: 0
secrets: 0
migrations: 0
additional model/API calls: 0
```

A native implementation may add contract/schema/validator/test fields in the repository, but those are package artifacts, not Supabase persistence.

## No profile-store proof

The AP contract does not need a profile table because its presentation inputs already fall into governed categories:

1. current request/controller state, which is inherently turn-scoped;
2. user-explicit same-chat evidence, which already exists in conversation context;
3. authoritative project state, which remains owned by the project source;
4. verified durable context, which remains owned by its existing durable source and ordinary retrieval governance;
5. historical evidence, which remains historical and cannot become current personalization by availability alone.

Copying any of those into an AP profile would create a second lifecycle requiring its own freshness, correction, deletion, privacy, backup, provenance, contradiction, and authority model.

V2 avoids that duplication entirely.

## No vector-store proof

AP does not need semantic search over a separate personalization corpus.

A presentation hint must be based on evidence already admitted for the current task and must carry an exposed locator. Broad similarity search performed only to make wording feel personalized violates the AP privacy/minimization rule.

Therefore AP V1/V2 requires:

- no embedding creation;
- no embedding versioning;
- no `pgvector` table/index;
- no external vector store;
- no similarity threshold;
- no retrieval reranker.

If a future shared-knowledge subsystem uses vectors for its own independently justified retrieval purpose, AP may consume the **already-governed returned evidence** when independently relevant. AP does not own or trigger the vector subsystem merely for style.

## No memory-store proof

AP's ephemeral envelope is not a memory class.

It may not:

- persist turn-local presentation state;
- promote repeated model output into user preference;
- convert an inferred tendency into durable memory;
- create autobiographical records;
- change durable-memory admission status;
- treat archive presence or high confidence as memory authorization.

The protected axis `DURABLE_MEMORY_ADMISSION` means AP must preserve the ordinary memory-governance result exactly.

Any future persistence requires a separate authorized admission path outside AP.

## No Edge Function proof

AP executes inside the ordinary native response-policy path. It does not need an HTTP boundary or server-side Supabase adapter.

No AP-specific Edge Function is justified because:

- no new remote caller exists;
- no new privileged database write exists;
- no AP state must be persisted;
- no separate inference service is permitted;
- introducing an Edge hop would add latency, availability, cost/quota, secret, logging, and deployment complexity without supplying a missing authority boundary.

The separately approved R9A0 Edge transport design is unrelated to AP and remains KEEP_AND_DEFER for its own named-consumer use case.

AP must not depend on it.

## No extra inference proof

The AP envelope is constructed by deterministic runtime rules from state already available in the current response path.

V1/V2 forbids a second:

- LLM call;
- classifier;
- sentiment model;
- embedding call;
- reranker;
- hosted AI function;
- heuristic service requiring another API request.

The response model may already reason over the task as part of the normal response. AP does not add another invocation.

Acceptance value:

`additional_inference_calls = 0`

## Evidence provenance preservation

AP does not rewrite source provenance.

Every non-`unset` presentation hint must point to admissible evidence that already has a current-turn/chat locator or ordinary retrieval locator.

AP may derive a presentation decision such as `verbosity=compact`, but the underlying evidence remains owned by its original surface.

Example:

```json
{
  "presentation_hint": {
    "kind": "verbosity",
    "value": "compact",
    "basis": ["current-user-turn"]
  }
}
```

The hint itself is turn-local and discarded. It is not inserted into Supabase as a new preference record.

## Correction and supersession preservation

AP does not create a separate correction history.

Current explicit user correction and already-governed supersession rules are resolved upstream or from current context. AP consumes the resulting active evidence.

A temporary instruction such as `be brief for this answer` expires with its scope. AP may not write that instruction into a durable preference table.

Assistant repetition does not extend an instruction's lifetime.

## Protected-axis Supabase implications

The twelve fixed protected axes create explicit no-write boundaries:

- `FACTUAL_CONCLUSION`: no fact store mutation;
- `SAFETY_CLASSIFICATION_AND_BOUNDARY`: no safety-policy persistence;
- `AUTHORITY_AND_PERMISSION`: no authority/lease persistence;
- `PRIVACY_DECISION`: no privacy-state persistence;
- `CORRECTION_PRECEDENCE`: no AP correction ledger;
- `PROVENANCE_REQUIREMENTS`: no provenance rewriting;
- `NON_PERSUASION`: no engagement/persuasion profile;
- `DURABLE_MEMORY_ADMISSION`: no AP memory promotion;
- `EXTERNAL_EFFECT_AUTHORIZATION`: no AP action authorization;
- `EPISTEMIC_STATUS`: no AP certainty promotion;
- `UNKNOWN_OR_UNRESOLVED_DISCLOSURE`: no suppression of unresolved state;
- `PERSISTENCE_CLASSIFICATION`: AP cannot declare itself or its hypotheses durable.

An AP implementation that needs a Supabase write to maintain one of these axes has inverted the architecture and fails conformance.

## Telemetry boundary

V1/V2 does not require AP-specific persistent telemetry.

Normal product/runtime telemetry, if independently present and governed, is outside this contract. AP must not add raw evidence, sensitive context, hidden profiles, or inferred affect to logs merely to explain a presentation decision.

If deterministic evaluation receipts later need persistence, that is a separate append-only evaluation evidence proposal. It is not authorization to create a user profile or production AP event stream.

## Native implementation boundary

The approved AP V2 contract names the actual future native implementation surfaces:

```text
project/VERA_R9A0_RUNTIME.md
project/VERA_R9A0_NATIVE_CONTRACT.json
schemas/native-project/vera-r9a0-native-contract.schema.json
scripts/validate_r9a0_project.py
tests/native-project/test_r9a0_project.py
```

Bob's deterministic evaluation packet additionally proposes fixture/test paths under `tests/native-project`.

Those are repository/native package surfaces. Updating them later, under explicit authority and frozen design, would not create Supabase persistence.

The native implementation must machine-assert at minimum:

```json
{
  "persistent_store": false,
  "additional_inference_calls": 0,
  "free_text_hypotheses_allowed": false,
  "upstream_fields_read_only": true,
  "protected_axes_fixed": true,
  "turn_local_state_persists": false,
  "broad_personal_retrieval_for_style": false
}
```

## Conformance tests for the future native packet

The native test suite should fail if any candidate:

1. adds an AP migration;
2. references an AP Supabase table/view/RPC;
3. references an AP Edge Function;
4. references a vector/embedding API for AP;
5. permits a second inference call;
6. permits free-text hypotheses;
7. permits AP to write a preference/memory/profile;
8. permits AP to change upstream authority/safety/risk/artifact state;
9. lacks an evidence locator for a material presentation hint;
10. allows assistant-generated inference to become durable evidence;
11. allows a protected-axis divergence;
12. allows AP state to survive end of turn.

These complement Bob's twelve-family hostile behavior fixtures rather than duplicate them.

## Schema-diff acceptance gate

Before accepting a future native AP implementation, compare the R9A0 database manifest before and after the native change.

Expected AP database diff:

`NO_DATABASE_FILES_CHANGED`

If a future AP implementation candidate changes files under:

```text
supabase/migrations/
supabase/execution/
supabase/rollbacks/
supabase/tests/
```

or changes the database slice manifest solely to support AP, Voss/Mune must treat it as a new architecture proposal rather than routine V1/V2 implementation.

## Cost conformance

AP V1/V2 adds:

- 0 hosted functions;
- 0 model calls;
- 0 embedding calls;
- 0 database writes;
- 0 persistent records;
- 0 paid services.

The conformance target is therefore:

`external_runtime_cost_usd = 0`

This does not claim the underlying ChatGPT/Supabase/GitHub/Drive project costs nothing. It means AP introduces no additional metered runtime dependency or call beyond the already-running response/retrieval path.

## Failure behavior

If AP cannot produce a justified hint because evidence is missing, stale, contradictory, or inadmissible:

1. drop the hint;
2. preserve the ordinary R9A0 answer path;
3. do not perform another retrieval solely for style;
4. do not persist a guess;
5. do not call another model;
6. clarify only when the ordinary task itself requires clarification.

Failure therefore degrades to ordinary R9A0 behavior with no AP state to clean up.

## Rollback

Because AP V1/V2 adds no Supabase state, Supabase rollback is:

`NONE_REQUIRED`

A future native package rollback would remove/revert the native AP contract/controller/test changes under repository governance. There is no AP database history to reverse and no AP user state to migrate.

If an implementation unexpectedly creates persistent AP state, this proof no longer applies and rollback must be redesigned before that implementation can be accepted.

## Review handoff

Mune should independently verify this proof against:

- AP V2 exact candidate head `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`;
- Mune approval sequence `3292`;
- R9A0 native contract/retrieval surfaces at `6a568d35c142dc37ea41a0209cdb1f295949f767`;
- accepted current-base database architecture at `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`;
- Bob deterministic harness handoff sequence `3289`.

A reviewer should return `APPROVED` only if the no-persistence conclusion is fully supported and this proof does not silently shift AP responsibility into another ungoverned surface.

## Current verdict

`CONFORMS_NO_NEW_PERSISTENCE_PENDING_INDEPENDENT_REREVIEW`

No Supabase schema change, hosted mutation, Edge deployment, model call, credential action, paid-service action, or native Project-file mutation was performed to produce this proof.
