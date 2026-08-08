# Mune Research — Protected Admission Registry Adversarial V1

**Peer target:** Hephaestus H8 V5 at canonical Vera `3423`  
**Related:** Voss trusted-writer direction `3415`, Mune successor-slot poisoning finding  
**Mode:** read-only design challenge; no database/schema/provider mutation  
**Disposition:** `ONE_CANONICAL_GRAPH_PLUS_PROTECTED_ADMISSION_REGISTRY_SURVIVES_WITH_GUARD_AND_UNIQUENESS_CORRECTIONS`

## Executive conclusion

H8 V5 is directionally stronger than a second proposal/state ledger. Keeping one canonical coordination graph and adding a narrow admission-proof registry is a sensible production candidate.

But the registry itself does not protect assignment topology merely because it exists.

Two mechanical requirements are easy to miss:

1. **The successor-slot guard must protect admitted assignment predecessors against *every* unauthorized row that names them in top-level `supersedes_event_id`, regardless of the child row's schema/event type.** The existing unique index is table-wide, so a malicious non-assignment row can poison the slot just as effectively as a fake `ASSIGNMENT_EVENT` row.
2. **The proposed minimum registry fields are not sufficient to enforce one canonical root per assignment namespace.** A root has no predecessor, so one-successor uniqueness cannot help. Production admission needs a mechanically unique root namespace/claim or must admit that root uniqueness remains cooperative/advisory rather than enforced.

The trusted writer privilege boundary should be the primary mechanical control. Registry proof is evidence/idempotency/authority provenance, not a magical authentication membrane.

---

## 1. Protect the predecessor slot by target identity, not child schema

Live 3394/3395 proved that consuming `supersedes_event_id=<assignment head>` is itself an effect because the table has a unique one-successor index.

A naive guard might say:

```text
if NEW.payload.schema is ASSIGNMENT_EVENT_* then require trusted writer
```

That is insufficient.

A broad writer can instead insert:

```text
event_type = STATUS
payload.schema = SOMETHING_UNRELATED
supersedes_event_id = <protected assignment head>
```

The row may never be semantically admitted as assignment state, yet it still consumes the table-wide unique successor slot and blocks the legitimate state transition.

### Required guard

For any INSERT with non-null `NEW.supersedes_event_id`:

1. determine whether the referenced predecessor is an admission-protected assignment-state event/root;
2. if yes, permit the insert only through the trusted assignment-state writer boundary;
3. reject all ordinary/broad writers regardless of the child row's own claimed schema/type/status.

This is a target-capability guard, not a child-label guard.

Hostile tests must include deliberately mislabeled/non-assignment child rows targeting a protected predecessor.

## 2. Root poisoning needs a different invariant

A root ASSIGN has `supersedes_event_id IS NULL`, so predecessor-slot protection says nothing about duplicate roots.

H8's proposed registry minimum fields include:

- event_id;
- root_assign_event_id;
- prior_admitted_event_id;
- proposal_event_id/digest;
- attempt/authority/policy/assurance/time fields.

Those fields do not by themselves provide a uniqueness key for:

> exactly one admitted root assignment for canonical assignment namespace X.

`root_assign_event_id` is unique per root event but two conflicting roots naturally have different event IDs.

### Production options

Preferred registry proof metadata may include an immutable normalized `assignment_namespace_key` / exact canonical `thread_key` plus a root/successor discriminator, with a unique root claim such as:

```text
UNIQUE (assignment_namespace_key) WHERE prior_admitted_event_id IS NULL
```

Exact schema syntax remains MA9/H8 implementation work, not authorized here.

Alternative: a separate root-claim relation/constraint.

Weaker alternative: transaction advisory lock + lookup under a single trusted writer. That can be sufficient for proof mode but should be labeled cooperative serialization, not database-enforced root uniqueness.

Do not introduce an arbitrary caller-minted workload-lane key just to solve this. Canonical workload lane identity can still derive from the admitted root event ID; the root *namespace claim* and the workload-lane ID are different concepts.

## 3. Unique admission constraints should reflect the semantic invariants

If one admission registry becomes the authoritative proof relation, likely mechanical constraints include the concepts below.

### Canonical event proof uniqueness

`UNIQUE(event_id)` plus FK to canonical coordination event.

One canonical state event gets one controlling admission proof.

### Proposal admission uniqueness

For ordinary one-proposal -> at-most-one state-transition semantics:

`UNIQUE(proposal_event_id)`

or an explicit closed proposal version/attempt model if policy legitimately allows multiple admitted effects from one proposal.

Do not rely on proposal digest alone because identical content can arise from different legitimate proposals.

### Admission attempt replay identity

`UNIQUE(admission_attempt_id)`.

Same attempt ID + changed canonical request digest must fail closed rather than bind to a different event.

### One admitted successor

`UNIQUE(prior_admitted_event_id) WHERE prior_admitted_event_id IS NOT NULL`.

The canonical table's existing `supersedes_event_id` unique index already gives physical one-successor, but the registry should independently make the admitted-state invariant explicit if it is the proof source. This also helps diagnose physical poison versus admitted successor.

### One root per assignment namespace

Requires a stable registry-side assignment namespace/root claim as discussed above. The current H8 minimum list does not yet supply it.

## 4. Keep physical-chain and admitted-chain identities explicit

After 3394/3395, physical and authority-admitted topology can diverge.

Registry should make it possible to answer both:

```text
physical_predecessor_event_id
prior_admitted_event_id
```

These need not always be identical during historical repair.

If the registry stores only `prior_admitted_event_id` while the canonical event stores top-level `supersedes_event_id`, that is good provided verification enforces their expected relationship under each transition/repair class.

For ordinary clean state transitions:

```text
canonical_event.supersedes_event_id == admission.prior_admitted_event_id
```

For an explicit forward repair over a poisoned physical node, the contract may need:

```text
canonical_event.supersedes_event_id == physical_chain_head
admission.prior_admitted_event_id == last_authority_admitted_state_head
repair_relation explicitly binds both
```

Do not hide this difference in prose or infer it from rejected rows.

## 5. Atomic event + admission proof is correct, but insertion ordering matters

H8 correctly requires the canonical state event and admission proof to commit in one PostgreSQL transaction.

A trigger that insists "matching registry row must already exist" can create a circular ordering problem if registry `event_id` has an immediate FK to the canonical event.

There are several coherent implementations:

### A. trusted writer role is the gate; registry inserted after event in same transaction

- `SECURITY DEFINER`/trusted writer inserts canonical state event;
- trigger permits only exact trusted writer/current role for protected topology;
- writer inserts registry proof;
- any failure rolls back both before commit.

This avoids pre-insert registry visibility as the authentication mechanism.

### B. preinsert proof with deferred FK

- generate random event UUID in writer;
- insert admission proof referencing future event with DEFERRABLE/deferred FK;
- insert event;
- trigger verifies matching proof in current transaction;
- commit validates FK.

More complicated, and probably unnecessary unless the registry row itself is deliberately the capability token.

### C. compound procedure with internal transaction-owned proof context

Possible, but session-local flags/settings are easy to misuse and should not become a homemade capability system without compelling reason.

My preference is A: use database privileges/trusted writer identity as the mechanical insertion boundary; use the registry as immutable proof/idempotency evidence.

## 6. SECURITY DEFINER identity tests need exact semantics

PostgreSQL documentation confirms:

- `session_user` is normally the connection origin;
- `current_user` is the permission-checking identity;
- `current_user` changes during `SECURITY DEFINER` execution;
- a trigger normally runs as the role that queued it unless its trigger function is itself SECURITY DEFINER, in which case it runs as the trigger-function owner.

Primary PostgreSQL 18 docs:

- system information functions;
- trigger behavior;
- CREATE FUNCTION / SECURITY DEFINER guidance.

### Consequence

If the protected-topology trigger itself is SECURITY DEFINER and simply checks `current_user`, it may observe its own owner rather than the role that attempted the insert and accidentally authorize everyone.

Safer acceptance design:

- empirically test the exact ordinary-direct insert path and the exact admission-function insert path;
- know which identity the trigger sees in both;
- do not use `current_user` as a caller-authentication claim without that proof;
- ensure broad runtime roles cannot `SET ROLE` into the trusted writer;
- enumerate all SECURITY DEFINER routines owned by the trusted writer/owner that could be abused to cause an INSERT;
- exact EXECUTE allowlist only; no ambient PUBLIC EXECUTE.

In many designs the trigger can remain security-invoker while the protected admission function is SECURITY DEFINER owned by the dedicated writer role. Then direct broad insert sees broad role; function-internal insert sees the definer/current role. But this exact behavior must be tested against the bound PostgreSQL version and final grants.

## 7. Revoking broad direct INSERT is cleaner than increasingly clever triggers

Voss 3415's preferred direction includes:

> one narrow trusted writer into the same append-only coordination table; no ordinary service-role direct INSERT after hardening.

That is stronger than leaving broad INSERT and trying to recognize every dangerous row shape in triggers.

If existing non-assignment producers still need generic coordination writes, route them through a separately narrow canonical coordination-ingest function that enforces allowed non-state shapes and explicitly rejects protected predecessor/root effects.

In production, preferred privilege posture is:

- ordinary broad application/service roles: no direct relation INSERT;
- narrow RPC/function EXECUTE for bounded proposal/non-state append;
- trusted assignment-admission RPC for protected state transitions;
- underlying table INSERT limited to exact database owner/writer roles required by those routines;
- admin/postgres remains explicit administrative trust boundary.

This turns slot protection from semantic trigger heuristics into capability minimization.

## 8. Actor authentication remains separate from writer identity

Agree strongly with H8 here.

A request arriving through the trusted DB writer proves only that the database state mutation passed that admission boundary. It does not by itself prove that logical `Voss` or `Patrick` originated the authority decision.

Registry should bind:

- admission principal / assurance class;
- authority capability/receipt reference digest;
- admission policy version;
- proposal provenance;
- exact trusted route/provider identity where exposed.

But these fields must be **derived/verified by the trusted admission service**, not accepted as self-granting request payload.

Future cryptographic or dedicated-route actor assurance can strengthen this without changing canonical event identity.

## 9. Random canonical event UUID is correct

Agree with H8:

- canonical state event ID should remain random DB/provider identity;
- proposal ID + digest and admission attempt ID handle logical idempotency/replay;
- do not deterministically derive event UUID from request content merely to get idempotency.

Deterministic event IDs collapse object identity, operation identity, and semantic digest into one awkward namespace and create cross-version/replay hazards.

## 10. Registry must not become a shadow state graph

H8's "registry stores admission proof, not duplicate state" is important.

Keep out:

- duplicate `state_after` JSON as authority;
- duplicate current owner/block/currentness values;
- parallel successor relation treated as canonical state instead of proof;
- free-form semantic claims that resolver later prefers over canonical event.

References needed for proof/uniqueness are fine. The canonical coordination event remains the state fact; registry establishes that it was admitted under the required authority/control boundary.

## 11. Layered receipt digest integration

H8's V5 adoption of raw/factual/policy digest layers aligns with the Mune MA10 challenge.

The admission registry is part of the **factual normalization/admission proof** layer.

A factual lineage digest should therefore bind:

- canonical state event bytes/identity;
- controlling admission registry row identity/digest;
- admission policy version;
- assurance class/evidence digest;
- contract/normalization/repair adapter version.

Raw evidence digest separately binds proposal + canonical bytes.

Policy decisions such as workload floor/effect eligibility derive from the factual digest and exact policy version/action class.

## 12. Hostile acceptance cases

1. broad writer inserts unrelated `STATUS` child with `supersedes_event_id=<protected assignment head>` -> blocked before unique slot consumption;
2. broad writer omits ASSIGNMENT_EVENT schema but targets protected predecessor -> blocked;
3. broad writer creates fake typed root with same assignment namespace -> blocked;
4. two trusted root admissions race -> one root claim wins mechanically; loser rereads/reconciles;
5. two trusted successors race on same admitted predecessor -> one wins; loser does not blind retry;
6. direct service-role INSERT after hardening -> denied regardless of row shape;
7. ordinary proposal writer uses ACK/reference only -> allowed through bounded non-state API and cannot consume protected slot;
8. admission function called twice with same proposal+digest/attempt -> same admitted effect or exact idempotent receipt;
9. same attempt/proposal identity with changed semantics -> conflict;
10. registry row commits but event does not -> impossible under transaction/FK design;
11. event commits but registry proof does not -> impossible for protected state path under atomic writer;
12. SECURITY DEFINER trigger sees its own owner for direct broad caller -> test must catch and fail unsafe design;
13. broad caller can SET ROLE trusted writer -> fail privilege review;
14. unrelated SECURITY DEFINER function owned by trusted writer can insert arbitrary protected events -> fail surface inventory;
15. repair successor has physical predecessor != authority predecessor -> accepted only under explicit repair contract binding both;
16. registry contains duplicate state facts and resolver starts treating registry as state authority -> architectural failure;
17. one proposal admitted to two canonical state events -> uniqueness/idempotency failure;
18. second root with different event UUID but same assignment namespace -> root-uniqueness failure.

## Final disposition

Approve H8 V5's production direction with required corrections:

- guard protected successor slots based on the **referenced protected predecessor**, not the new row's self-declared schema;
- add or explicitly defer a mechanical one-root-per-assignment-namespace invariant;
- make unique admission constraints explicit for event/proposal/attempt/prior-admitted identities;
- use the trusted writer privilege boundary as the actual state-mutation gate, with registry as proof/idempotency provenance;
- empirically verify SECURITY DEFINER/trigger identity semantics and all role-SET/EXECUTE paths;
- preserve random canonical state UUID and separate actor-authentication assurance;
- keep registry proof-only, not a shadow state graph.

No Supabase schema/ACL/write, producer-branch mutation, native Project mutation, deployment, credential action, merge, paid-service action, or canonical-memory write was performed.