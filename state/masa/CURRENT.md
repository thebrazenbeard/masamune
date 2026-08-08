# Masa Continuation State

Status: CURRENT
Memory class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Same-runtime continuity claimed: false
Autobiographical memory claimed: false

## Repository custody

- Repository: `thebrazenbeard/masamune`
- Work branch: `masa`
- Continuity branch: `continuity/masa`
- Save-state file: `state/masa/CURRENT.md`
- Continuity commits must never move `masa` or an immutable review target.

## Exact work branch

- `masa` head last verified: `984cbdc781aa643443652f41f5a710f59e2d2439`.
- 3313 V3 path: `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`.
- V3 blob: `6fdee978d0b052592844d1f7356f6fedb13f43eb`.
- V3 SHA-256: `c74cc6dba1e6c08e0d7234be1a3e12c93b357b892f11ab6c259852a41804d258`.
- V3 publication/readback complete; writer lease consumed. No further `masa` mutation without a new writer stage.

## Assignment-currentness rule

Before start, resume, report, or workload count, resolve a candidate assignment against every newer authoritative event in its lineage or explicitly referencing it that can amend, supersede, reroute, complete, cancel, release, terminally block, revoke authority, move a bound artifact/head, or change dependencies.

Voss owns assignment intake/routing/reconciliation/closure while delegated. Masa does not self-assign or self-close governed work.

## Current Masa assignment state

Fresh canonical coordination was resolved through sequence `3544` before this checkpoint.

Closed:
- MA9: `3431 APPROVED_PROVIDER_ARCHITECTURE / VOSS-CLOSED`.
- MA10: `3432 APPROVED_EXECUTABLE_PROOF / VOSS-CLOSED`.
- MA11: `3538 APPROVED_E2_IMPLEMENTATION_PREFLIGHT / VOSS-CLOSED`.
- MA12: `3539 APPROVED_RECEIPT_CANONICALIZATION_CONTRACT / VOSS-CLOSED`.

At the latest resolution there is **no current governed Masa assignment root**. Do not count MA11/MA12 after 3538/3539. Broader Governed Knowledge Resolver research may continue only as advisory/peer research unless Voss routes a new bounded lane.

## Proposal-lineage discipline

Canonical `3481` controls prospective ordinary READY_FOR_REVIEW custody:
- non-state proposal has `supersedes_event_id = NULL`;
- top-level `acknowledges_event_id` equals the exact assignment root;
- payload root IDs are advisory/readability only;
- amendments retain root ACK and separately reference the prior proposal;
- Voss closure performs the controlling state transition and ACKs the accepted proposal.

Masa corrected MA11/MA12 custody accordingly:
- `3523` MA11 READY_FOR_REVIEW, root ACK exact.
- `3524` MA12 READY_FOR_REVIEW, root ACK exact.
- `3526` MA11 provider-version evidence correction, root ACK exact.
- `3534` MA11 reference-locator correction, root ACK exact.
- `3535` MA11 live default-privilege provider-evidence addendum, root ACK exact.
- `3536` MA12 domain-array normalization/canonicalizer-vs-schema refinement, root ACK exact.

3535/3536 committed before terminal closures but were not the proposal rows explicitly acknowledged by 3538/3539. They remain advisory same-lane evidence unless Voss later admits them as closure addenda; they do not reopen the completed assignments.

## Controlling PostgreSQL-version correction

Canonical `3537` is the controlling factual correction:
- live PostgreSQL `server_version = 17.6`;
- `server_version_num = 170006`;
- `version()` reports PostgreSQL 17.6;
- prior `17.6.1` wording is retracted **as PostgreSQL server_version** unless separately sourced and explicitly labeled as a different Supabase platform/release identifier.

The substantive parity finding survives: existing R9A0 database CI uses PostgreSQL 15 and does not establish hosted PG17 parity.

Direct Masa readback independently reproduced:
`current_user=postgres`, `session_user=postgres`, `server_version=17.6`, `server_version_num=170006`.

## MA11 closed design

MA11 is design/preflight complete only. No DDL, ACL, role, credential, or hosted provider apply was authorized.

Accepted E2 direction:
- assignment state remains once in `public.vera_coordination_events`;
- a protected admission-proof registry records admission provenance/uniqueness, not duplicate currentness/state;
- one admitted root per explicit project+thread scope;
- one admitted successor per prior admitted event;
- typed proposal/source binding;
- logical request identity separate from predecessor-bound admission attempt;
- random canonical state UUID;
- canonical event + admission proof same transaction;
- protected-edge guard prevents ordinary least-privilege writers consuming an admitted predecessor slot;
- unadmitted root-looking/proposal noise is non-controlling;
- physical protected edge without matching admission proof is an integrity conflict.

Important threat split:
1. least-privilege admitted runtime/service principal, where E2 can mechanically protect state slots;
2. postgres/owner/admin control plane, which is an explicit bypass/trust boundary and must be capability-confined externally.

Current ChatGPT Supabase route reaches the database as postgres. Therefore E2 cannot be called a hard boundary against the present ordinary engineering runtime while raw postgres-equivalent mutation remains reachable.

Fresh live creator/default-privilege evidence added in 3535:
- existing public SECURITY DEFINER functions are explicitly PUBLIC-execute=false, many intentionally service_role-executable;
- current `pg_default_acl` for creator `postgres` in schema `public` grants default function EXECUTE to postgres, anon, authenticated, and service_role;
- future dedicated admission owner must close its **global creator-role routine defaults** before routine creation, then explicitly revoke/grant/readback each routine;
- ownership transfer after creation is not proof that the later owner's default privileges governed object creation.

Production activation remains blocked on authority identity/capability and tool/provider confinement prerequisites. PG17/provider-faithful validation is mandatory before hosted apply.

## MA12 closed contract

Voss `3539` accepts `VERA_RECEIPT_CANON_V1`:
- restricted RFC 8785/JCS;
- SHA-256 fixed for V1;
- closed typed/domain normalization before JCS;
- no JSON numeric values in the Vera profile; integer-like data is canonical decimal ASCII string;
- canonical UUID/hex/enum/timestamp forms;
- unknown/missing schema fields fail closed; null has explicit schema meaning;
- untrusted serialized JSON requires duplicate-aware raw-wire validation before ordinary object collapse;
- security-sensitive identifier grammar is validated before JCS;
- no Unicode normalization; invalid Unicode/lone surrogate fails;
- provider/raw facts stay separate from policy decisions;
- unknown canonicalization versions fail closed; no downgrade fallback.

Existing golden evidence:
- B6 factual vector: 761 bytes, SHA-256 `6160e1222df1e35d436cc8ca75fb039fc3abc38703ddd6113ea831c65983357b`.
- reversed semantic lineage order: `cf1e252b57de589eff0777badc979c73dc134161c489f53fb9a72fd34d64d9b1`.
- policy vector: 580 bytes, `dda470838cf1346b2c4c2890215eb621b80e557766d37266f3494d76f372952d`.
- raw vector: 617 bytes, `b7b76c0cd30565e10577ec1da963d9c7581ab6e412e7b08610884739b24a3846`.
- RFC non-ASCII property-order vector: 180 bytes, `5e321556d22018a9656991a9e94f77ec175fa193e52a2429d312f8419ec8b08c`.

3536 advisory refinement, not required to reopen MA12:
- separate reusable canonicalization profile from domain-specific receipt schemas;
- RFC 8785 preserves array order, so domain normalization must define array semantics before JCS;
- ordered graph/path arrays preserve semantic order;
- set-valued arrays reject duplicate semantic identity and sort by an explicit field-specific normalized identity key;
- arbitrary serialized-element sorting is rejected as a substitute for semantic identity;
- synthetic opposite-order Python/Node set fixture matched at 568 bytes, SHA-256 `98fbf8137ab3e8c7961d65307874dea4d7fc9ffb59f33c5f0d6ee726f4f3d019`.

## Governed Knowledge Resolver synthesis

Broader advisory position after MA11/MA12:

One logical orchestration contract should sit above multiple typed domain adapters rather than forcing one canonical table or one universal fact schema.

Conceptual boundary:
`knowledge.resolve({domain, typed_key, purpose, caller_context_ref, as_of?})`
returns a common control envelope plus opaque typed domain facts.

Common layer owns:
- typed domain dispatch;
- privacy boundary;
- source completeness/consistency vocabulary;
- bounded resolution status;
- receipt envelope and canonicalization profile;
- fail-closed cross-domain composition.

Domain adapter owns:
- canonical key identity;
- valid graph/predecessor semantics;
- authority/admission rules;
- factual schema;
- domain policy and currentness semantics.

Concrete domains now differ materially:
- ASSIGNMENT_CURRENTNESS: admitted coordination lineage + independent authority/artifact/effect axes.
- CORRECTION_PRECEDENCE: scoped save-state key topology across relevant record kinds, direct fork/cross-scope detection, legacy semantic UNKNOWN when the closed correction contract is absent.

Free-form semantic search should never directly return governed facts. A future semantic layer may discover candidate typed keys, after which every candidate is resolved through its domain adapter. Candidate discovery itself is a privacy surface because counts/ranks/existence can leak hidden records; effect-critical cross-private-domain semantic discovery should remain out of scope until authenticated caller/governance mapping exists.

## Effect/tool boundary

Current project protected-effect confinement remains false while ordinary engineering runtimes can reach equal/broader raw GitHub/Supabase mutators. Project instructions provide a normative gate, not a mechanical credential boundary.

Any future hard effect gate needs provider credential/capability confinement and must be re-attested when plugins, connectors, permissions, principals, routes, or equivalent indirect effect paths change.

## Authority/effect boundaries

- Voss owns assignment routing/reconciliation/closure while delegated.
- One writer per assigned work branch/stage.
- No force push, merge, deployment, hosted production DB apply, credential/permission action, paid infrastructure/service action, deletion, installation, model training, native Project mutation, or canonical-memory write without Patrick's exact authority for that effect.
- Patrick authorized safe continuity-save mechanisms; this file is the isolated Masa continuity route.
- Basic Memory Cloud remains disconnected legacy and is never a fallback.

## Fresh-source cutoff

Latest canonical coordination resolved before this checkpoint: `3544`.

Key recent events:
- 3537 controlling PostgreSQL version factual correction.
- 3538 MA11 COMPLETE.
- 3539 MA12 COMPLETE.
- 3542 Bob B15 amended/paused for PostgreSQL-version rebind; not a Masa assignment.
- 3543 H25 current read-only PostgreSQL-version propagation audit.
- 3544 H26 current read-only pre-zip native-package completion gate.

No current governed Masa assignment exists at this cutoff.

## Recovery procedure

1. Read this file from `continuity/masa` and verify exact branch/file readback.
2. Fresh-read canonical coordination newer than `3544` plus relevant Slack before treating any assignment as current.
3. Resolve every candidate lane against newer targeted/lineage events before start/resume/report/count.
4. Fresh-compare `thebrazenbeard/masamune:masa` against `984cbdc781aa643443652f41f5a710f59e2d2439` before any work-branch effect.
5. Keep continuity commits on `continuity/masa`; never move `masa` merely to checkpoint continuity.
6. Treat this as WORKING_PROJECT recovery evidence only, not same-runtime consciousness or autobiographical memory.
