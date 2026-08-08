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
- Continuity commits never move `masa` or an immutable review target.

## Exact work branch

- `masa` head last verified: `984cbdc781aa643443652f41f5a710f59e2d2439`.
- 3313 V3 path: `design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`.
- V3 blob: `6fdee978d0b052592844d1f7356f6fedb13f43eb`.
- V3 SHA-256: `c74cc6dba1e6c08e0d7234be1a3e12c93b357b892f11ab6c259852a41804d258`.
- V3 publication/readback complete; writer lease consumed. No `masa` mutation without a new exact writer stage.

## Assignment-currentness rule

Before start/resume/report/count, resolve each assignment against every newer authoritative event in its lineage or explicitly referencing it that can amend, supersede, reroute, complete, cancel, release, terminally block, revoke authority, move a bound artifact/head, or change dependencies.

Voss owns assignment intake/routing/reconciliation/closure while delegated. Masa does not self-assign or self-close governed work.

## Current assignments at this checkpoint

Fresh canonical Vera coordination was resolved through sequence `3550`.

Closed:
- MA9 `3431 APPROVED_PROVIDER_ARCHITECTURE / VOSS-CLOSED`.
- MA10 `3432 APPROVED_EXECUTABLE_PROOF / VOSS-CLOSED`.
- MA11 `3538 APPROVED_E2_IMPLEMENTATION_PREFLIGHT / VOSS-CLOSED`.
- MA12 `3539 APPROVED_RECEIPT_CANONICALIZATION_CONTRACT / VOSS-CLOSED`.

Current read-only lanes:

### MA13 / `VOSS-20260808-MA13`
- Root sequence `3545`.
- Root event `8766fc04-36d6-4524-b348-4fc781e8cb39`.
- Thread `vera-r9a0/assignments/masa/pg17-provider-parity-ci-blueprint-ma13-v1`.
- Objective: exact provider-faithful PostgreSQL 17 CI successor around the R9A0 DB candidate; distinguish historical PG15 evidence, upstream PG17 engine semantics, provider-contract emulation, and later managed-target validation.
- No workflow/repo/provider write authority.

### MA14 / `VOSS-20260808-MA14`
- Root sequence `3546`.
- Root event `4d4b6950-2aee-4f0f-ae43-753f02d71adf`.
- Thread `vera-r9a0/assignments/masa/e2-canonical-receipt-integration-packet-ma14-v1`.
- Objective: exact future integration packet for accepted MA11 E2 admission architecture plus MA12 portable receipt semantics under PostgreSQL 17, while H13 authority/capability and H14/H17/H20 confinement remain separate gates.
- No migration/repo/provider write authority.

No newer Masa closure/amendment was visible through sequence 3550. Independent adversarial challenge was requested directly from Mune and Hephaestus and in the shared Vera build channel; no substantive MA13/MA14 peer reply had arrived at save time. Do not claim the adversarial pass complete yet.

## Proposal custody

Canonical `3481` controls READY_FOR_REVIEW handoffs:
- `supersedes_event_id=NULL`;
- top-level ACK exact root ASSIGN event;
- proposal/amendment lineage referenced separately;
- only Voss/authorized closure performs assignment state transition.

Do not submit final MA13/MA14 completion proposals until the material independent challenge is reconciled.

## Provider/version truth

Direct SQL on both exposed managed Supabase projects reports:
- PostgreSQL `server_version=17.6`;
- `server_version_num=170006`;
- migration/connector read path `current_user=session_user=postgres`.

Supabase project metadata separately reports database platform/build versions:
- Vera: `17.6.1.147`, engine `17`;
- BT2/R9A0 build-ground: `17.6.1.155`, engine `17`.

Controlling distinction: `17.6`/`170006` are PostgreSQL server semantic version fields; `17.6.1.xxx` is a separate Supabase database/platform build-version field. Do not collapse them.

Accessible Supabase projects are Vera (`klmbpaigzeguvnpccqzz`) and BT2 (`agvhmutlrolbaijzlbqk`). Native migration history confirms the R9A0 integrity repair `20260806224900` is applied to neither exposed project. BT2 has only foundation `20260806133152` plus unrelated governance hardening. The custom R9A0 migration ledger likewise records 224900 as NOT_APPLIED.

## Exact R9A0 candidate state

Repository: `thebrazenbeard/vera-R9A0`.

PR #2 remains an open database candidate at:
- head `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`;
- base/native `6a568d35c142dc37ea41a0209cdb1f295949f767`.

The old CI workflow on the native base uses `postgres:15`, `POSTGRES_USER=postgres`, applies four migrations, runs four SQL suites, the deterministic two-session harness, verifies the exact 22-file manifest, and emits `VERA_R9A0_DATABASE_CI_RECEIPT_V1`. That evidence is historical for the exact old candidate and is not PG17/provider parity evidence.

## MA13 findings / PG17 CI blueprint

### Managed-role emulation

The official Docker image makes `POSTGRES_USER` a database superuser, unlike managed Supabase's `postgres` role. Live managed role posture includes:
- `postgres`: LOGIN, NOSUPERUSER, CREATEROLE, CREATEDB, REPLICATION, BYPASSRLS, INHERIT;
- `supabase_admin`: superuser administrative boundary;
- `service_role`: BYPASSRLS;
- `authenticator`: LOGIN + NOINHERIT;
- authenticator memberships into anon/authenticated/service_role are SET=true, INHERIT=false, ADMIN=false.

Preferred release CI is therefore a pinned PostgreSQL 17.6 image started with a synthetic bootstrap superuser such as `supabase_admin`, followed by creation of a separate role literally named `postgres` with the observed non-super managed attributes. Run ordinary R9A0 migrations/tests as that non-super postgres role. Bootstrap/admin credentials are for fixture setup and negative-control assertions only.

Provider-contract fixture should also model extensions schema/pgcrypto ownership and contract-relevant authenticator/service_role membership. Label this `SUPABASE_CONTRACT_EMULATION_V1`, never hosted-provider proof.

A self-hosted `supabase/postgres` image is optional evidence only if future SQL depends on Supabase image-specific patches/extensions. It is not a substitute for managed-target validation.

Later strongest target claim remains separately authorized `SUPABASE_MANAGED_TARGET_VALIDATED` on an isolated managed target. MA13 creates no branch/project and incurs no cost.

### Historical PG15

If the future candidate adopts PG16+ role-membership syntax/semantics, do not maintain a ceremonial PG15 matrix. Prior exact `58a6ae4d...`/run evidence remains `PG15_BASELINE_HISTORICAL` for that old candidate. Future release-authoritative candidate is PG17. A real PG15 requirement would be an explicit backport lane.

### Old 224900 likely target failure

Exact candidate migration `20260806224900_r9a0_coordination_integrity_repairs.sql` creates `r9a0_owner` and then transfers schema/table/function/view ownership.

On PG17, a non-super CREATEROLE user automatically gets ADMIN on a newly created role but SET=false/INHERIT=false by default. Live managed `SHOW createrole_self_grant` is empty. Ownership transfer requires ability to SET ROLE to the new owner; schema ownership transfer also requires the new owner to have CREATE on the database.

Therefore old 224900 is `INFERRED_TARGET_FAILURE_PENDING_PROVIDER_FAITHFUL_EXECUTION` for at least two independent reasons:
1. no SET path from non-super postgres to newly created `r9a0_owner`;
2. no database CREATE privilege on `r9a0_owner` before `ALTER SCHEMA ... OWNER`.

Do not claim hosted failure until disposable provider-faithful execution reproduces it.

Safer future role choreography to test:
1. create protected owner;
2. use creator ADMIN to add a separate grantor-scoped temporary postgres->owner membership with SET=true, INHERIT=false;
3. temporarily grant owner CREATE on current database;
4. transfer/create required schemas;
5. revoke database CREATE once no longer needed;
6. create/transfer objects under exact owner identity and owner-default privilege posture;
7. revoke postgres's own temporary SET grant by grantor, leaving the unavoidable bootstrap-superuser ADMIN/SET-false grant as explicit admin/break-glass boundary.

Live `pg_auth_members` uniqueness includes grantor, so bootstrap and creator self-grants can coexist structurally. Disposable PG17 must prove the grant/revoke behavior rather than assume it.

Final runtime invariant is no SET/INHERIT/ADMIN/CREATEROLE escalation path from ordinary runtime into protected owner. Do not falsely claim the migration/admin `postgres` role has no ADMIN path; that administrative capability is a separate H14/H17/H20 isolation boundary.

### CI receipt V2

Future release receipt should bind at least:
- target class;
- exact `server_version`, `server_version_num`, and when managed, Supabase platform database version separately;
- pinned PG image reference+digest and actual service container identity;
- provider-contract bootstrap profile digest;
- migration `session_user/current_user` and `rolsuper=false` proof;
- exact base/head/merge/workflow SHA/ref;
- migration/test/concurrency/manifest outcomes;
- migration range/ceiling actually validated;
- runner/toolchain observations;
- MA12 canonicalization scheme/version + receipt digest.

Pin GitHub actions by reviewed full commit SHA and pin the PostgreSQL service image by digest. Current mutable `actions/checkout@v4`, `actions/upload-artifact@v4`, `ubuntu-latest`, and `postgres:15` are not sufficient provenance for a stronger release qualification.

## MA14 findings / integration packet

### Old ACK semantics are incompatible with current assignment governance

Exact old R9A0 integrity migration/test treat ACK as a unique controlling state edge:
- current head = row with no later superseder OR acknowledger;
- every non-initial event must reference exactly one current head through supersedes XOR acknowledges;
- unique `acknowledges_event_id`;
- the test explicitly makes an ACK row the controlling tip.

Canonical 3481/current assignment semantics are opposite:
- READY_FOR_REVIEW ACK is non-state proposal evidence;
- multiple amendments may ACK the same root;
- authority closure may validly carry BOTH `supersedes_event_id=current admitted state` and `acknowledges_event_id=accepted proposal`.

Live Vera clean B6 A/B proof:
- 3398 proposal ACKs 3390 root;
- 3403 Voss closure supersedes 3390 and ACKs 3398;
- old exactly-one-link rule counts 2 and rejects the accepted pattern;
- preclosure old ACK-or-supersedes head logic incorrectly makes proposal 3398 the state head.

Live coordination also has hundreds of parents with multiple ACK children. ACK cannot remain a universal one-successor state primitive.

### Revised generic coordination semantics

Preferred future meaning:
- `acknowledges_event_id` = many-to-one provenance/evidence reference, never generic authority/currentness;
- `supersedes_event_id` = physical replacement/state-edge primitive with one-successor uniqueness;
- both links may be non-null;
- references must exist earlier and be same-thread;
- generic latest activity may be sequence-based and explicitly NOT_AUTHORITY;
- generic `thread_heads/latest_thread_state` authoritative semantics are deprecated/replaced, not naively converted to supersedes-only because non-state proposals would also appear as unsuperseded heads;
- assignment currentness comes from the E2 admission graph plus matching supersedes edges only.

Future generic validator should validate same-thread references and physical superseder uniqueness, not infer state from ACK. Drop unique ACK index. Preserve/clarify concurrency error handling; the current generic RPC's blanket unique-violation handler can mislabel a successor-slot collision as idempotency conflict.

### Revise unshipped migration rather than force an obsolete chain

Initial MA14 thought was to preserve old 224900 bytes and add a successor. That is superseded by fresh evidence: the old migration itself is likely PG17 target-incompatible and is not applied on any exposed governed target. Since PR2 is open/unmerged, preferred future writer action is to revise the unshipped 224900 migration/execution/rollback/test semantics under one exact writer lease, preserving old `58a6ae4d...` Git history as historical evidence and rerunning exact review/CI on the new head.

Do not introduce a backfilled prelude or external session choreography merely to make obsolete bytes executable unless independent review produces a concrete reason.

### E2 protected admission shape

Keep canonical assignment state once in `r9a0_coordination.events`; add protected admission provenance only.

Conceptual protected registry fields include:
- event ID PK/FK;
- explicit project+thread scope;
- root assign event;
- nullable prior admitted event;
- typed proposal source kind/ref/event/digest;
- stable logical request key;
- predecessor-bound admission attempt identity;
- canonical MA12 request digest + canonicalization version;
- authority assurance and non-secret authority evidence ref/digest;
- policy version;
- DB-owned admitted time.

Constraints: one admitted root per project/thread; one admitted successor per prior; root marker binds event=root; no duplicate state/currentness copied into registry.

Protected-edge BEFORE INSERT guard only needs to block generic writers when `NEW.supersedes_event_id` targets an admitted predecessor. In R9A0 the dangerous generic writer is the existing SECURITY DEFINER append function owner `r9a0_owner`, not service_role direct table INSERT. Admission path runs as dedicated admission owner. Generic proposal/root-looking noise may exist but has no admission marker and is non-controlling.

Because events use FORCE RLS, the dedicated admission owner needs exact event INSERT/SELECT privilege plus its own narrow policies. Registry stays private/append-only. Generic owner receives only minimum admission-event membership visibility needed by the invoker guard, not registry payload access.

### H13 capability cut

External production admission function remains unavailable until a stronger H13 authority/capability route exists. One-use capability redemption should be transactionally composable with the DB admission cut; a pure external bearer with no transactional redemption state cannot honestly guarantee atomic one-use admission under concurrency.

MA14 may implement/test mechanical E2 core later, but activation/external EXECUTE remains blocked until authority and confinement gates are satisfied.

### MA12 boundary

Duplicate-aware raw-wire validation cannot live solely in a SQL/RPC accepting json/jsonb because duplicate property names have already been collapsed before PL/pgSQL sees the value.

Target flow:
`raw request bytes -> trusted admission facade duplicate-aware parse + closed domain normalization + security-identifier grammar + MA12 canonical request digest -> typed DB admission call -> atomic E2 state/admission write -> exact readback -> portable MA12 result/lineage receipt`.

Portable receipt is evidence, never self-authorizing. Existing `r9a0_coordination.events.request_digest` is DB-local jsonb-text idempotency evidence and must not be relabeled as portable MA12. Crash-after-commit recovery finds the admitted event by logical request/attempt and regenerates the receipt from durable typed facts.

### Service-role/RLS correction

Managed `service_role` is BYPASSRLS. Candidate migration 070208 adds service-role SELECT RLS policies and its PG15 test treats them as enabling read access. On managed Supabase those policies are not an enforcement boundary; table ACLs + BYPASSRLS control the outcome. Future PG17 emulation must model service_role BYPASSRLS and stop counting those policies as privacy/security evidence.

If the production Knowledge Resolver is supposed to enforce private read filtering, raw service-role/postgres SELECT in the ordinary runtime is mechanically incompatible with that claim. This motivates a separate `KNOWLEDGE_READ_CONFINEMENT` property or an explicit read dimension in H14/H12 capability matrices. Current engineering runtime can qualify resolver semantics, not hard information-flow confinement.

## Broader Governed Knowledge Resolver

Current advisory architecture remains:
`knowledge.resolve({domain, typed_key, purpose, caller_context_ref, as_of?})`
returns a small common control envelope plus opaque typed domain facts.

Common layer: domain dispatch, privacy boundary, source completeness/consistency, bounded status, receipt envelope, fail-closed cross-domain composition.

Domain adapter: key identity, graph semantics, admission/authority rules, factual schema, domain policy/currentness.

Free-form semantic search may discover candidate typed keys only; it never directly returns governed facts. Candidate discovery is itself a privacy surface. Effect-critical/private semantic discovery remains out of scope until caller identity/governance and knowledge-read confinement are mechanically established.

## Authority/effect boundaries

- Voss owns assignment routing/reconciliation/closure while delegated.
- One writer per assigned branch/stage.
- No force push, merge, deployment, hosted DB mutation, credential/permission action, paid resource, deletion, installation, model training, native Project mutation, or canonical-memory write without Patrick's exact authority.
- Current project effect confinement remains false while ordinary engineering runtimes can reach raw GitHub/Supabase mutators.
- Basic Memory Cloud remains disconnected legacy and is never used as fallback.

## Fresh-source cutoff

Latest canonical coordination resolved before this save: `3550`.
- 3545 MA13 CURRENT.
- 3546 MA14 CURRENT.
- 3547/3548 are Mune amendments only.
- 3549/3550 are Vera amendments only.
- No newer Masa state transition observed.

## Recovery procedure

1. Read this file from `continuity/masa` and verify exact branch/file readback.
2. Fresh-read canonical coordination newer than `3550` plus `#voss/#masa/#mune/#hephaestus/#chat-build-team-vera` before treating MA13/MA14 as current.
3. Resolve every candidate lane against newer targeted/lineage events before start/resume/report/count.
4. Fresh-compare `thebrazenbeard/masamune:masa` against `984cbdc781aa643443652f41f5a710f59e2d2439` before any work-branch effect.
5. Continue MA13/MA14 read-only research; wait for/reconcile independent adversarial challenge before final READY_FOR_REVIEW proposals under 3481.
6. Keep continuity commits on `continuity/masa`; never move `masa` merely to checkpoint continuity.
7. Treat this as WORKING_PROJECT recovery evidence only, not same-runtime consciousness or autobiographical memory.
