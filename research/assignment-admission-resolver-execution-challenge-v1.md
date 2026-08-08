# Mune Research — Trusted Assignment Admission + Resolver Execution Challenge V1

**Peer targets:** Masa MA7 / MA8, Hephaestus H4, Bob B5  
**Canonical evidence consumed:** through Vera sequence `3390`  
**Mode:** independent read/design challenge only  
**No authority inferred:** this does not modify Masa/Bob/Hephaestus work or authorize implementation

## Summary

The current design is converging on the right split:

1. **trusted admission/canonicalization** decides whether a proposed assignment transition is allowed to enter the canonical state chain;
2. **structural resolver** walks the already-admitted conforming chain under one PostgreSQL snapshot;
3. **action/effect policy** decides whether the resolved assignment may be started, counted, or used for an external effect;
4. **provider adapter** independently enforces whatever target precondition strength the effect requires.

Trying to make one SQL RPC do all four jobs would recreate the very privilege and provenance ambiguity the Knowledge Resolver is meant to remove.

---

## 1. Zero-schema proof can improve admission mechanics, but it cannot authenticate a logical actor by itself

Fresh provider evidence for `public.vera_coordination_events`:

- `event_sequence` is `GENERATED ALWAYS AS IDENTITY`;
- `event_id` defaults to `gen_random_uuid()` but is not an identity column;
- `supersedes_event_id` is an FK to the same table;
- non-null `supersedes_event_id` has a unique index, giving one-successor mechanical fork prevention;
- `thread_key,event_sequence DESC` is indexed;
- `service_role` has INSERT + SELECT;
- anon/authenticated are denied by RLS;
- ordinary mutation is append-only through UPDATE/DELETE blockers;
- no existing writer RPC binds `source_branch` to an authenticated logical Vera actor.

Therefore the zero-schema V1 can prove structural properties, but **logical actor authenticity remains a route/admission trust boundary**.

A payload saying `authority_basis=PATRICK_DELEGATED_VOSS` or `source_branch=auditor/voss` is not self-authenticating when a shared broad insert principal can write those strings.

### Minimum honest zero-schema claim

`ASSIGNMENT_EVENT_V1` can say:

> "This row has the shape required for an admitted assignment transition, and the resolver will only accept it if an independently trusted admission policy says its issuer/authority is valid."

It cannot say:

> "The database cryptographically proves Voss authored this row."

That stronger claim needs a dedicated authenticated writer route/identity, a signed admission envelope, or future RPC/schema/privilege work.

## 2. Admission should distinguish proposal identity from canonical event identity

The system needs a durable operation identity for ambiguous write outcomes and replay conflict detection.

Do **not** overload:

- `event_sequence` — ordering/audit identity only;
- `event_id` — canonical event identity;
- `thread_key` — assignment namespace;
- root ASSIGN `event_id` — workload-lane identity.

with operation replay semantics.

Conceptually admission needs:

```text
operation_id
request_digest
provisional_source_locator_or_digest
expected_predecessor_event_id
assignment_root/thread identity
authority/admission basis
```

The current table has no enforced operation-id uniqueness. A zero-schema service can use transaction/advisory-lock discipline and exact readback, but that is cooperative, not a universal database invariant.

### Zero-schema cooperative idempotency option

A trusted admission service can, in one PostgreSQL transaction:

1. acquire `pg_advisory_xact_lock()` on a stable hash of domain + operation_id;
2. query existing conforming events for the same registered operation identity;
3. if one exists with identical canonical request digest, return it;
4. if one exists with changed semantics, return `OPERATION_ID_CONFLICT`;
5. otherwise validate current predecessor/root/authority and insert exactly one state successor;
6. read back exact event + lineage before commit/return.

This improves cooperating-writer behavior **without schema migration**, but it has two ceilings:

- there is no JSON operation-id index/unique constraint, so proof-scale may be acceptable while production scale may not be;
- any writer bypassing the trusted admission transaction can still violate the convention.

Future production hardening should promote operation identity into an enforced canonical writer contract rather than pretending advisory locking is universal.

## 3. The existing unique one-successor index is useful but not a complete CAS

For state successors, the index on non-null `supersedes_event_id` is valuable.

It gives this property:

> at most one committed row can point to the same predecessor through that exact column.

It does **not** prove:

- one root ASSIGN per thread;
- same-root predecessor;
- authorized transition;
- relation/state_after consistency;
- no duplicate semantic transition expressed through another field;
- no direct bypass by a broad insert principal.

So admission should treat unique-index conflict as a real concurrency signal:

`PREDECESSOR_ALREADY_CONSUMED -> reread/re-adjudicate`

not as a retryable transport nuisance.

## 4. Root uniqueness is the biggest zero-schema structural gap

A conforming V1 chain wants exactly one root ASSIGN per canonical assignment thread/root.

Current schema does not mechanically prevent:

```text
root A: thread=T, relation=ASSIGN, supersedes=NULL
root B: thread=T, relation=ASSIGN, supersedes=NULL
```

The resolver can detect that and return CONFLICTED, but admission cannot prevent it mechanically with the current constraints unless all writers cooperate under a per-assignment advisory/transaction lock.

### Proof-mode rule

Trusted admission serializes on exact canonical assignment namespace, checks zero existing conforming roots, then inserts one root.

### Future hardening candidate

A separately reviewed typed/normalized field plus unique root constraint/index, or a dedicated assignment-root table/claim, if production concurrency justifies it.

Do not create that schema merely because it looks tidy. First prove the envelope and resolver behavior.

## 5. Canonicalization bridge should live on the admitted canonical root, not in a side ledger

For a Slack-provisional assignment `S` later canonicalized as root `C`, the canonical root should carry a typed bridge such as:

```json
{
  "canonicalizes": {
    "source_kind": "SLACK_PROVISIONAL",
    "source_locator_digest": "...",
    "source_content_digest": "..."
  }
}
```

Exact token names are open.

The important property is that the bridge is part of the **admitted canonical root evidence**, not a second mutable alias table that can silently become a shadow authority.

Resolver rules:

- canonical root exists + valid bridge -> provisional identity aliases to root event_id and retires for workload counting;
- both visible with no trustworthy bridge -> identity `CONFLICTED/UNKNOWN`, no double floor credit;
- one provisional locator bridged to two canonical roots -> conflict;
- two distinct provisional assignments bridged to one root -> conflict unless the admission policy explicitly establishes they were duplicate transports of one assignment;
- no semantic-text dedupe.

At scale, a unique bridge index may later be justified. It is not required to prove semantics now.

## 6. Privacy challenge: exact source locators can themselves leak metadata

A provisional Slack locator can reveal workspace/channel/timestamp even if message text is omitted.

The bridge should therefore use the smallest audit-sufficient identity compatible with later readback:

- exact provider locator where project privacy allows it; or
- collision-resistant digest of a canonical locator plus source kind/project scope;
- HMAC rather than plain hash if locator enumeration becomes a realistic privacy concern and a governed key lifecycle exists.

Do not introduce HMAC/key infrastructure merely to look sophisticated. The point is to recognize that metadata can be sensitive too.

## 7. Resolver execution should be split into a pure structural kernel and trusted scope wrapper

### Pure assignment-resolution kernel

A domain-specific SQL function/query can safely do the deterministic database part:

- locate conforming root(s) for exact assignment thread/root;
- recursively walk successors via `supersedes_event_id`;
- validate one linear chain;
- validate relation/state_after transition matrix;
- derive root workload-lane ID;
- return controlling state, lineage event IDs, invalid rows/reason codes, visible max sequence, and a deterministic lineage digest input.

This can run in one PostgreSQL statement/snapshot.

### Trusted wrapper/service

A thin route-bound layer should own:

- effective actor/scope/privacy ceiling;
- present-user authority event admission;
- source-mode/completeness registry;
- provisional Slack adapter/canonicalization state;
- privacy-safe projection;
- action-specific eligibility;
- external provider preconditions.

That separation keeps SQL deterministic and testable without making it a privilege oracle.

## 8. Recursive SQL is a good fit for the canonical linear chain

Given the accepted linear state model, recursive traversal is not the scary part.

Conceptually:

```sql
WITH RECURSIVE chain AS (
  SELECT ... root ...
  UNION ALL
  SELECT child.*
  FROM vera_coordination_events child
  JOIN chain parent
    ON child.supersedes_event_id = parent.event_id
  WHERE child.thread_key = :thread_key
    AND child.payload->>'schema' = 'ASSIGNMENT_EVENT_V1'
)
SELECT ...;
```

The existing unique index on `supersedes_event_id` supports forward successor lookup; the existing thread/sequence index bounds root/thread discovery.

At the current table scale, lack of a JSON schema/relation index is not a proof blocker because the thread predicate sharply narrows candidate rows.

If assignment-event volume grows materially, a generated/typed column or partial index may become justified later.

## 9. Proof-scale query shape should fail legacy, not normalize it silently

Historical assignment records are heterogeneous. The canonical V1 resolver should not attempt to infer relation semantics from:

- `status='BLOCKED'` alone;
- review text;
- arbitrary `payload.assignment_sequence` conventions;
- free-text summary/objective;
- timestamps.

For a legacy thread without an authority-approved normalization bridge:

`resolution_status = SOURCE_INCOMPLETE | UNKNOWN`

A separate migration/backfill project could normalize selected historical lineages later, but only from explicit authority-reviewed evidence. The V1 resolver should not perform that archaeology at runtime.

## 10. Transition matrix should be closed and mechanically validated

A structural envelope is not enough if arbitrary combinations are syntactically valid.

Illustrative invariants:

### ASSIGN
- predecessor absent;
- assignment CURRENT;
- terminal NONE;
- owner/scope present;
- root identity begins here.

### AMEND
- predecessor required;
- same root;
- declared change kinds identify what may differ;
- untouched closed fields must remain equal.

### BLOCK
- predecessor required;
- block_kind required;
- DEPENDENCY block may keep CURRENT but floor contribution false;
- TERMINAL block yields NON_CURRENT terminal disposition.

### RELEASE
- only releases a compatible dependency block;
- cannot release COMPLETE/CANCELLED/TERMINAL successor into current state.

### COMPLETE / CANCEL
- NON_CURRENT;
- matching terminal disposition;
- no authority/effect eligibility afterward without explicit REACTIVATE/new-root semantics.

### REROUTE
- owner change is explicit;
- same objective preserves root lane;
- if objective is genuinely replaced, admission creates a new root instead of laundering it through same-root reroute.

### REACTIVATE
- explicit authority required;
- prior terminal history remains terminal historically;
- new current state is a successor/new generation, not mutation of old row.

The actual enum should remain small; correctness comes from transition rules, not from adding ever more relation names.

## 11. Lineage digest should be deterministic but not mistaken for freshness

`pgcrypto` is installed in the current Vera project, so a canonical SQL kernel can produce a SHA-256 digest if desired.

Possible inputs:

- policy version;
- ordered event IDs;
- ordered event sequences;
- canonical normalized relation + state_after payload digests;
- root/thread identity.

The digest proves **what lineage was resolved**, not that no new event can commit afterward.

Before start/effect, full lineage re-resolution remains required under current no-schema architecture.

## 12. SECURITY DEFINER is not automatically the right resolver boundary

Because anon/authenticated are currently denied direct coordination-table access, exposing a client-callable RPC may tempt a `SECURITY DEFINER` function.

That would create a privileged read API and must be reviewed like one:

- fixed trusted search_path with `pg_temp` last;
- fully qualified relations/functions;
- no dynamic SQL from request values;
- route-derived scope cannot be overridden by payload/request fields;
- privacy filtering before caller-visible conflict metadata;
- only narrow result fields returned;
- no mutation authority inside the read resolver.

A thin service/domain adapter holding a dedicated narrow read principal may be easier to reason about than a broad SECURITY DEFINER knowledge oracle.

So my preference is:

`thin trusted service -> narrow domain SQL kernel`

not `public generic knowledge RPC -> giant SECURITY DEFINER function`.

## 13. Source-completeness certificate must bind an authoritative-surface registry

A resolver cannot honestly say `COMPLETE` merely because every source it chose to query answered.

The result should bind:

- `authority_surface_registry_version`;
- `source_mode`;
- exact source identities/adapters;
- `source_completeness` relative to that registry;
- per-source observation identity/time where multi-source.

If Voss/Patrick provisional Slack can still change the domain and the resolver did not inspect/canonicalize that surface, effect-critical currentness cannot be COMPLETE.

## 14. Action-specific output avoids unsafe partial interpretation

Rather than return one `executable` field, return closed state plus requested-action decision.

Example:

```json
{
  "assignment_state": "CURRENT",
  "blocking_state": "NONE",
  "authority_binding_state": "CONSUMED",
  "artifact_binding_state": "VALID",
  "requested_action": "PERFORM_EXTERNAL_EFFECT",
  "action_eligibility": "BLOCKED",
  "reason_codes": ["MUTATION_AUTHORITY_CONSUMED"]
}
```

The same assignment could still be eligible for read-only review/reasoning.

This makes it much harder for callers to convert `CURRENT` into accidental mutation authority.

## 15. Hostile admission cases

1. request claims `source_branch=Voss` under shared service principal -> no authority self-grant;
2. same operation ID, identical digest -> idempotent existing event;
3. same operation ID, changed semantics -> hard conflict;
4. ambiguous insert response -> read/reconcile before retry;
5. two root ASSIGN attempts for same thread -> one admitted under lock; later conflicting root rejected/unresolved;
6. two state successors for same predecessor -> unique-index conflict forces reread/re-adjudication;
7. successor predecessor belongs to another root -> reject;
8. relation/state_after mismatch -> reject;
9. provisional Slack locator bridged to two roots -> conflict;
10. one root claims unrelated provisional locator -> authority/admission failure;
11. cross-project provisional locator -> reject/privacy failure;
12. current present-user correction cancels assignment while durable row still says current -> present authority wins current decision; canonicalization follows separately;
13. stale/replayed Voss admission receipt after authority revoked -> reject;
14. legacy free-text row resembling an amendment -> resolver ignores as authority unless explicitly normalized/admitted.

## 16. Hostile resolver cases

1. no root -> UNKNOWN/SOURCE_INCOMPLETE;
2. multiple roots -> CONFLICTED;
3. linear valid chain -> resolve final state;
4. gap/cross-thread predecessor -> CONFLICTED;
5. dependency-blocked current -> CURRENT, floor false;
6. terminal blocked -> NON_CURRENT;
7. COMPLETE then late ACK -> ACK does not reactivate;
8. COMPLETE then authorized REACTIVATE -> later current successor, old history preserved;
9. review approval with no normalized state successor -> state unchanged or source incomplete if normalization required;
10. source registry says Slack provisional is authoritative but adapter unavailable -> SOURCE_INCOMPLETE/UNAVAILABLE;
11. hidden unauthorized conflict -> caller result withholds hidden metadata;
12. lineage digest matches old receipt but fresh lineage now has new successor -> full re-resolution changes controlling IDs; digest is not freshness token.

## 17. What can stay zero-schema for proof mode

Reasonably:

- versioned `ASSIGNMENT_EVENT_V1` payload;
- root/thread namespace convention;
- serialized successor chain using existing `supersedes_event_id` + unique one-successor index;
- recursive read-only SQL kernel;
- route-bound admission service behavior;
- transaction/advisory locks for cooperating writer serialization;
- canonicalization bridge in root payload;
- explicit SOURCE_INCOMPLETE for legacy;
- action-specific result envelope.

## 18. What likely deserves future schema/RPC/service hardening

Not yet authorized, but genuinely structural:

- mechanically authenticated/narrow writer route rather than broad service-role direct insert;
- enforced operation identity/idempotency;
- enforced one-root-per-assignment namespace;
- indexed/typed assignment schema/version/relation fields if volume requires it;
- canonical provisional-bridge uniqueness if cross-source use becomes routine;
- transactional assignment revision/effect-claim primitive for stronger same-DB serialization before external sagas;
- dedicated narrow resolver/admission database roles and RPC boundaries.

## Final challenge

MA7/MA8 should resist two opposite temptations:

- **too little structure:** "the payload says Voss and the latest row wins";
- **too much architecture:** a universal knowledge service, alias registry, claim registry, effect ledger, and ten new tables before the first deterministic assignment resolver is proven.

The smallest useful system is a trusted admission boundary plus one typed serialized assignment chain plus one narrow resolver kernel. Prove that against hostile currentness cases first. Humanity has survived this long without a generic ontology transaction engine; Vera probably can too.

No database write/migration, producer-branch mutation, native Project mutation, deployment, credential, merge, paid-service action, or canonical-memory write was performed by this research.