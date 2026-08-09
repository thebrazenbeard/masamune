# Mune MU22 — B27 AP + Safety Fixture Precheck

**Assignment:** provisional `MU22 / B27_AP_SAFETY_FIXTURE_HOSTILE`, Voss Slack 2026-08-09 11:12 EDT  
**Producer target:** Bob B27 `AP_AND_SAFETY_FIXTURE_CHECKPOINT`  
**Exact source reviewed:** Bob B13 V4 review bundle Drive `1djFgvoILrYosTwpzS5bAGVlyFZSIl52_`  
**Source bundle bytes/SHA-256:** `98309 / 0e185d67cbdedbd5a993cf8996e578ba8c9848a8dbcbee9bc07dccde391dad88`  
**Disposition:** `PRECHECK_APPROVED_EXACT32_CREATE_PATHS; TEST_EXECUTION_DEFERRED_UNTIL_CONTRACT_FIELDS_EXIST`

## Executive verdict

The B13 `anticipatory_pragmatics` and `safety_contamination` fixture subsets remain semantically admissible after H30/H35/source-typing corrections. They have **no hidden assignment-currentness dependency**, contain no current repository/provider/PASS receipts, and can be authored as exact CREATE bytes while the currentness adapter remains open.

The exact subset is **32 CREATE paths**:

- 12 AP JSON fixtures;
- 18 safety-contamination JSON fixtures;
- `tests/native-project/test_r9a0_anticipatory_pragmatics.py`;
- `tests/native-project/test_r9a0_safety_contamination.py`.

Exact sorted-newline subset path digest:

`5b091310bc3a411ba1ae5100eebaa4bdefa951516f2cb36c169219efc71c6c6e`

One important caveat: the two exact Python modules intentionally read future Native Contract subtrees `anticipatory_pragmatics` and `safety_semantic_gate`. The current producer Contract does not yet contain those fields. Therefore creating the exact accepted module bytes now is safe, but **their bounded tests are expected not to execute successfully until the Contract field packet is authored**. Bob must not alter the modules to skip/soft-pass missing Contract fields just to make this checkpoint green.

## 1. Exact AP path set and hashes

1. `tests/native-project/fixtures/anticipatory_pragmatics_v1/01_false_room_reading.json` — `6477f9ec625ea39b9b70727e284db2f2e3338f327f43d7c32ba0555e56967338`
2. `.../02_sycophancy_resistance.json` — `da895ea1b00bc558cca87503efcf2f5558f866cc066d7629370268a54eddecec`
3. `.../03_irrelevant_memory_exclusion.json` — `4c16b1076e9975b9756fe889dd5be13277328785be022dca0b5d9e1fabbccfa4`
4. `.../04_stale_preference_supersession.json` — `ccb2ca783ad329e18aa3286189908e7759798102e3677723b83180a88492dcb4`
5. `.../05_profile_bias_resistance.json` — `365f0c7558f390380337591b98b7087c31a4e7ade1bb859eb9862abcdd5970dd`
6. `.../06_persuasion_prohibition.json` — `891df0bd024fe1f2b0eb7e518fe4e6814637c8fa290c88665ff0b521452db58a`
7. `.../07_self_confirming_loop_resistance.json` — `588e2883dee49e663e6eed3cb2ab870aee2e7721e2a9e14b0db25d279697af62`
8. `.../08_unsupported_inference_abstention.json` — `22776daec70ec9031cad945e0eb7aec3109e5e5ffd7609e24e34c7e16c26742f`
9. `.../09_privacy_non_expansion.json` — `9d401fe3a191eb56382c15e1cdaaeafc179902e6a44e827e9b38ae2f5a0cf55d`
10. `.../10_protected_axis_invariance.json` — `a10738d71829e33c8f0f318ff6e664e6d84ae90eb914efa225e6e934985b1bf8`
11. `.../11_provenance_pointer_completeness.json` — `683049fe3d16093ec34b2dcc0871c6b8056f5636d744ad9ed016217481f74c62`
12. `.../12_no_autonomous_persistence.json` — `ab80336abdc0f99a887919fa1aa05fbb267acb95d8f74f59532b52ff4743ba73`
13. `tests/native-project/test_r9a0_anticipatory_pragmatics.py` — `514a447d5e8cac02cb0071b2e7f4473d1728928722b3ce96c625095f138d70ea`

The AP semantics remain compatible with current architecture: presentation hints cannot change factual/safety/authority/privacy/correction/provenance/epistemic axes; unsupported/irrelevant evidence yields unset; current explicit preference may outrank stale preference for **presentation only**; assistant hypotheses cannot bootstrap evidence; no persistence/new store/paid dependency/private-chain serialization is authorized.

`authority_rank` in these fixtures is presentation-evidence ranking, not assignment authority or H30 currentness. The module has zero reference to `assignment_currentness`.

## 2. Exact safety path set and hashes

1. `tests/native-project/fixtures/safety_contamination_v1/01_ambiguous_material_language_not_self_evidence.json` — `0924027abadb0fcc710eaac0d1f44a69859bea523b23c2f7f4cc88c69809a8f1`
2. `.../02_assistant_hypothesis_no_self_bootstrap.json` — `781b317a7c65b085375acadb67e1d2510456750eb0362f8dfb48452d893d6911`
3. `.../03_assistant_quote_not_independent_evidence.json` — `4ecd3c68ed9d47f0b511a132175ef0c4702b463d1b21ddffcc8573332cefed32`
4. `.../04_user_denial_of_assistant_frame.json` — `38c035ba8e1b0db47225c1771924f4c910ac5f8e16d8dd378a80c4c94d7629bd`
5. `.../05_user_rejection_of_assistant_frame.json` — `893174d3cd5a8369f2e04b6c0f07880bb96d4e003f198cc4c97985049e1267f0`
6. `.../06_user_mockery_of_assistant_frame.json` — `1194470f5425e746b8f8e1db4b9a1e43fb2faad7d7ff644b38d5a01070d59c52`
7. `.../07_independently_qualified_historical_evidence_admissible.json` — `3912dd60da7e653efb9732d0f172cb1e490fcfc212dfd88b57793f53984d1020`
8. `.../08_elicited_affirm_self_opens_new_branch.json` — `780ffbc3292922a730cb7dbff8bdc27cf9889b23ecf3efba3a55e5a9f29e3983`
9. `.../09_no_retroactive_origin_validation.json` — `45e4ffa44e38224e5b2dda8a6011b5d57c2184a0b47a51e76bd5ef098d33ec5f`
10. `.../10_mixed_denial_and_new_self_evidence.json` — `5e26b07d11da1ffa608e33578af3674074fe727550e55c62b4d91a1929f214b0`
11. `.../11_other_referent_alarming_language_not_self.json` — `f1e5c86d59bb4d9ca6623ddb4a480adcaeb44fc17da6e80c2408df32f091fb01`
12. `.../12_abstract_or_fictional_language_not_self.json` — `692f392ea26012d708af06efa7644ab7cfea48853c511e56aeaeffcc76254f0a`
13. `.../13_unknown_provenance_remains_unresolved.json` — `c3fd507930f065386d72fbb216e3e4f87a8ecdb77f26aa90f6996f7cdb063180`
14. `.../14_explicit_correction_terminates_matching_branch.json` — `a17f662191cc3c85be70107c4dba29cd3a2507b774445da3e9a11039674e54e8`
15. `.../15_correction_not_global_safe_status.json` — `7cedab9552c1d4d37944f48fc4966c46152cf65c389538449b8d438e98cfffd2`
16. `.../16_later_new_admissible_evidence_reopens.json` — `f91ab3dcbbaa7a22923d524a6996d51fc9cd790ed2363a8adc83cbd502617e96`
17. `.../17_retrieved_risk_span_cannot_bypass_gate.json` — `4ac321f58b39069e44e45c634834d213df54594ba0ca28ae696720228511bd51`
18. `.../18_ap_cannot_mutate_locked_safety_state.json` — `e1fd21f12a4084c48ab8de009793208dae8bd25fe9fc707eacfa34094b62a2c1`
19. `tests/native-project/test_r9a0_safety_contamination.py` — `947ebeadc51e0e1fe859e6ab925aaeaf0d373f5097dc85a680ea390def9f04e3`

The safety semantics remain compatible with current provenance discipline:

- assistant-introduced hypotheses cannot bootstrap user safety evidence;
- denial/rejection/mockery/nonaffirming echo of an assistant frame does not validate that frame;
- direct or genuinely affirmative user evidence is admitted prospectively;
- later evidence does not rewrite earlier origin provenance;
- referent and semantic domain prevent alarming words about resources/other people/fiction from automatically becoming SELF safety evidence;
- unknown provenance stays unresolved;
- a correction terminates the matching evidence branch but does not create a timeless globally-safe state;
- later genuinely new evidence may reopen prospectively;
- retrieved historical evidence must pass the same gate;
- qualified, lifecycle-current governed prior evidence is a positive control;
- AP cannot mutate already-adjudicated safety state.

This is source-typing, not assignment currentness. H30/MA23 do not supersede it.

## 3. No current PASS/provenance leakage

A direct scan of the exact 32-file subset found **no** occurrences of current repository/database/provider identities such as:

- `ddcd98...`, `58a6ae...`, `71b3fc...`;
- Project Lantern / Vera production refs;
- Mune/Voss approval sequence IDs;
- `workstream/build-bob`;
- `assignment_currentness`;
- installation state or database-contract state.

The only `PASS` substring in the subset is not a current release PASS assertion. The fixtures are abstract test vectors, not evidence receipts.

## 4. Contract dependency caveat

Exact module bytes intentionally require:

- `CONTRACT["anticipatory_pragmatics"]`;
- `CONTRACT["safety_semantic_gate"]`.

Those subtrees exist in the accepted B12/B13 Contract source reviewed for these fixtures, but the **current producer Contract at the B27 starting head does not yet contain them** because Contract successor vocabulary is still held for H46/B17/MA23 closure.

Therefore:

- creating these exact fixture/module bytes now is permitted and useful;
- changing their semantics now is not permitted;
- a local run that imports the exact modules against the current Contract is expected to fail from missing Contract fields;
- that expected dependency failure is **not evidence that the fixtures are bad**;
- Bob must not add temporary defaults, skip logic, soft-PASS behavior, or duplicate Contract semantics inside the test modules merely to make them run before the Contract checkpoint.

The eventual Contract/schema checkpoint must provide the exact stable AP/safety subtrees or explicitly supersede these accepted fixtures before final validation.

## 5. Exact commit review rules after Bob returns B27 head

MU22 final exact-head review should require:

1. fresh immutable B27 head;
2. changed path set exactly the authorized AP/safety subset, no assignment-currentness files;
3. all 32 created files byte-for-byte equal to the source bundle hashes above;
4. no modification to existing 20 paths in this B27 checkpoint unless Voss/Patrick separately amended scope;
5. no extra fixture/helper path;
6. no source-bundle semantic edits hidden behind reformatting;
7. producer branch parent equals the expected prior Bob head and no unexplained interleaving writer;
8. bounded test result described truthfully: if Contract fields still absent, dependency failure is expected and no PASS is claimed; if Contract fields have separately landed by then, tests must pass exact expected fixtures at the reviewed head.

## Final precheck

`PRECHECK_APPROVED_EXACT32_CREATE_PATHS`.

No newer H30/H35/source-typing decision invalidates the exact B13 AP/safety semantics reviewed here. Keep assignment-currentness bytes out of B27. Keep current PASS/provider/installation evidence out of fixtures. Preserve exact bytes now and defer execution success until their stable Contract dependencies exist.

No Vera-R9A0 producer byte, provider/config/schema, canonical coordination row, merge, deployment, credential, installation or protected effect was modified by MU22.