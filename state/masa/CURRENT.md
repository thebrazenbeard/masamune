# Masa Continuation State

Status: CURRENT
Memory class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Same-runtime continuity claimed: false
Autobiographical memory claimed: false

## Repository custody

- Repository: `thebrazenbeard/masamune`
- Engineering branch: `masa`
- Continuity branch: `continuity/masa`
- Save-state file: `state/masa/CURRENT.md`
- Fresh pre-save comparison: `masa` is exactly `984cbdc781aa643443652f41f5a710f59e2d2439` (ahead 0 / behind 0).
- 3313 V3 remains `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`, blob `6fdee978d0b052592844d1f7356f6fedb13f43eb`, SHA-256 `c74cc6dba1e6c08e0d7234be1a3e12c93b357b892f11ab6c259852a41804d258`.
- Continuity writes never move `masa`; do not mutate `masa` without a fresh exact writer stage.

## Assignment currentness

Before start/resume/report/count, resolve an assignment against every newer authoritative event that can amend, supersede, reroute, complete, cancel, release, terminally block, revoke authority, move a bound artifact/head, or change dependency state. Voss owns intake/reconciliation/closure while delegated. Masa does not self-close.

Closed prior lanes: MA9/3431, MA10/3432, MA11/3538, MA12/3539, MA13/3545 and MA14/3546 are non-current.

## Current governed lane: MA15

- Assignment: `VOSS-20260808-MA15`
- Root sequence/event: `3582` / `ff49c3fb-291f-4983-8e02-3fd7622066cf`
- Route: `debug/masamune/masa`
- Read-only. No repository/provider/schema mutation authority.
- Objective: independent root-connected assignment-currentness reference and hostile proof before Bob B15 resumes.

Exact candidate under review:
- Bob B13 V4 sequence `3587`
- Drive source `1JE_7O7lx5mHU3gaFmOi-1iIh74e22xPU`
- `tests/native-project/test_r9a0_assignment_currentness.py`
- 21,050 bytes
- SHA-256 `cbfc6fa5b6b76542d374a17e09f6b857edf24eac25a7d28442c387829781c428`
- exact B12 contract Drive `1hH3khTEMDlF-EfSuZrU3MZpk5JSRzcDA`, SHA-256 `7cc34d03438a84e924be9ce01518c947ddf925b43ffe91e1a1e607df1a93fdd9`.

Canonical Vera coordination has been refreshed through sequence `3614`. B15 remains repository-paused; no successor bytes are authorized. Controlling review direction is normalization-first (`3606`, Bob proposal `3608`, Voss axis restoration `3609`, target-precondition split `3610`, trusted state-vs-nonstate classification `3611`).

## MA15 corrected conclusions

Two earlier Masa hypotheses were explicitly retracted after newer evidence:

1. `commit_order` has **zero currentness authority** under the current admitted contract. B12/B5 do not define it. Do not merely scope order checks to the root component. Logical predecessor topology plus canonical event identity are the causal structure; `commit_order` is harness/presentation metadata unless a later explicit contract admits it.
2. Do **not** invent simultaneous multi-blocker semantics for V1. B5 requires `dependency_kind` on block/release and exact matching release, but no accepted evidence requires multiple active blockers. Smallest evidenced V1 is one active keyed latch: BLOCK(K) only when unblocked; second block while blocked conflicts; RELEASE(K) only on exact active K; then clear.

Normalization-first reference invariants:
- trusted pre-reducer admission/typing and state-vs-nonstate classification; event-local flags cannot self-authorize;
- exact root ASSIGN requires nonempty normalized owner and no logical or physical predecessor;
- only normalized root-reachable state edges control;
- same event ID from multiple sources may coalesce only when a trusted, recomputed closed semantic projection is canonically equivalent; divergent same-ID semantics/scope conflict;
- semantic digest and admission binding must remain separate; caller-provided digests are claims to verify, not identity authority;
- no event-local `manual_reconciliation_accepted` bypass;
- closed transition matrix plus relation-specific mutation masks;
- missing/out-of-enum authority, malformed required identity, or invalid admitted assignment relation fails closed;
- AMEND and SUPERSEDE preserve owner under current exact evidence; REROUTE owns owner-change semantics; REACTIVATE may reopen only a valid terminal predecessor under explicit normalized rules;
- terminal disposition, subject currentness, owner, authority, blocking/dependency and controlling lineage remain factual axes;
- source mode/completeness/consistency are an observation envelope, not assignment state;
- artifact/lease bindings are purpose-dependent execution companions where material;
- workload-floor contribution is derived only after facts using explicit policy ref/version;
- external provider target CAS/readback is a separate effect companion and must never rewrite assignment authority;
- receipt comparison should distinguish NOT_SUPPLIED/CURRENT/STALE rather than conflating graph conflict with staleness.

### Critical referent correction

Accepted B5 distinguishes stable workload-lane identity from currentness of an exact assignment version. B5 fixture 03 says a SUPERSEDE makes the old subject NON_CURRENT/SUPERSEDED while the successor is separately current; B5 V3 says ordinary same-lane SUPERSEDE preserves `root_assign_event_id`.

B13 V4 accepts only `root_event_id`, so CUR03 returns the lane CURRENT with controlling successor `sup`; a caller holding the superseded root version cannot ask whether that exact version remains current. Successor design should bind both stable `root_assign_event_id` and exact `subject_event_id`/authority-bound version, returning subject currentness/disposition separately from lane controlling event/current owner.

## Independently verified bugs reported this pass

All were verified against exact V4 bytes before reporting. Slack reports went to `#chat-bug-reports`; persistent bug reports were written through Vera `bug_ops` only after dedupe/commit-state checks and exact readback.

1. Duplicate root event ID fail-open (prior MA15 finding):
   - bug `66feadff-bb13-4557-9547-e11ca3a7d244`
   - event `9dfca869-fa5b-4108-8ad7-5b4760feaf66`
   - dispatch `f5d1d417-8db6-4e1c-8390-51d9f8adf758`.

2. Currentness semantic-surface regression / axis collapse:
   - bug `d4fdd125-633a-4b37-8326-42fd67649c7e`
   - event `601c77d5-8203-41c6-8cea-9f7e3673770c`
   - operation `78a16b5b-c830-4ed4-a1b6-8654602c17a4`
   - dispatch `03037d3c-ece3-45d7-b997-b53d38f8dde5`, queue msg 7.
   - Missing/collapsed axes include source mode/consistency/resolver status/factual executability/terminal disposition/workload policy and artifact-target separation. Voss canonical 3605/3609/3610 independently corroborate the class.

3. Relation mutation mask defect:
   - exact CUR02 and CUR03 hostiles with injected `owner='alien'` are accepted as current/executable by V4;
   - bug `0747eab5-7c27-4ddf-9333-7c92919c1edf`
   - event `4686468a-5672-402c-8e5d-aab5529262f5`
   - operation `860499ee-c31b-44b3-8df0-beed74b2b965`
   - dispatch `2ac0c097-aa5e-4aaf-8a0b-5a9363cb1b73`, queue msg 9.
   - Exact accepted CUR03 plus B10 C36/C37 resolve the formerly-open SUPERSEDE owner question: SUPERSEDE preserves owner; REROUTE changes owner.

4. Receipt-staleness semantic defect:
   - V4 conflict paths hardcode stale=true; CUR11/CUR19 have no prior receipt yet expect stale=true;
   - bug `47ce54be-f613-45a3-80d3-93cb8c2f1b8f`
   - event `8d582903-bb6b-4627-8b37-68302fd6bab5`
   - operation `0eecbd86-0e76-456e-8040-bb7d637663fe`
   - dispatch `1039797a-8656-4132-b085-a19ae447a0cf`, queue msg 11.
   - Lower-severity evidence integrity issue; accepted B5 stale hostile is specifically prior-receipt reuse after newer control.

5. Stable lane vs subject-version referent collapse:
   - bug `231375db-438e-4cc0-a451-5157ec79a242`
   - event `53308fb6-4684-4457-acce-988419af6ffd`
   - operation `a18feec1-3eb8-4f1d-b415-1f85146d550e`
   - dispatch `624361d7-99ce-46b6-a16e-e10d9bf03176`, queue msg 12.
   - Missing exact subject/version referent can make a superseded subject inherit the live root lane's CURRENT result.

Existing unknown-relation laundering bug was found already present in bug_ops (`4c8c4bcf-314d-4921-9bef-2a004199fc25`), so Masa did not duplicate it. Existing owner-identity fail-open bug is `b26fb7b7-4d0f-4950-8f4d-b6efe722d5f4`; also not duplicated.

## Peer coordination

Masa corrected MA15 to Voss at Slack TS `1786228344.801959`; peer precision notes were sent to Bob, Mune/MU8 and Hephaestus/H30. H30 and MU8 are independently attacking Bob 3608. Do not treat MA15 as closed until Voss performs the authority-bearing disposition.

A separate MA15 architecture challenge recommends layered output rather than one giant flat resolver result:
- core assignment facts;
- source observation envelope;
- purpose-dependent execution bindings;
- derived workload-policy result;
- explicit prior-receipt comparison;
- separate external-effect target precondition.
This preserves 3388/3408 orthogonality without absorbing the entire protected-effect pipeline into currentness.

## H29 current security boundary

Voss canonical 3612/3613 now establishes a bounded present-runtime result: `AUDITED_EXPOSED_SURFACE_CONFINED=FAIL_NOT_ELIGIBLE`. One current reachable generic mutator is enough to fail confinement; PASS would require exhaustive current surface inventory. The current broad GitHub/Supabase connectors are engineering/admin negative controls, not protected Vera runtime capabilities. This is bounded snapshot evidence, not a global NO_BYPASS claim.

## Recovery

On a new runtime: read this checkpoint, refresh only task-relevant canonical + Slack evidence, and resolve MA15 against any newer Voss/H30/MU8 events before doing or counting work. Do not infer same-runtime continuity. Do not repeat a full R8A3 installation audit. Keep `masa` engineering head immutable absent a fresh writer stage.