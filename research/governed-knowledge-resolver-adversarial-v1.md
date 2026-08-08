# Mune Research — Governed Knowledge Resolver Adversarial Architecture V1

**Lane:** direct-user / cross-facet design challenge  
**Vera coordination:** `3360` (`vera/hephaestus/cross-facet-knowledge-resolver-v1`)  
**Mode:** read-only architecture/research; no Supabase schema write, native Project mutation, or deployment  
**Primary proof domain:** `ASSIGNMENT_CURRENTNESS`  
**Disposition:** `ONE_LOGICAL_API_MULTIPLE_TYPED_RESOLVERS_SURVIVES_WITH_SOURCE_AND_FRESHNESS_CORRECTIONS`

## Executive conclusion

The core architecture survives adversarial review:

`stable logical client API -> trusted caller/scope binding -> typed versioned domain resolver -> authoritative source adapter(s) -> structural lineage/authority/lifecycle adjudication -> privacy-safe projection -> deterministic ephemeral receipt`

But two assumptions must be corrected before V1 can be called operationally authoritative:

1. **Supabase-only assignment currentness is currently incomplete as an operational truth source**, because newer assignment-affecting coordination can become effective in Slack before a corresponding canonical Supabase event appears.
2. **`event_sequence` / max sequence is not a commit-completeness token or CAS.** In the live Vera table it is caller-supplied `bigint NOT NULL` with no database default or sequence allocator; even a database sequence would not prove commit completeness because PostgreSQL sequence advancement is nontransactional.

Therefore `resolved_through_sequence` is too strong unless carefully defined. V1 should report `max_visible_event_sequence` as provenance and re-resolve immediately before gated effects.

## 1. Provider-backed state of the current coordination surface

Fresh read-only inspection of live Vera project `klmbpaigzeguvnpccqzz` establishes:

- `vera_coordination_events` is append-only on the ordinary `service_role` path: service role has INSERT+SELECT; UPDATE/DELETE blocked by triggers; anon/authenticated denied by RLS.
- `event_id` is database-generated UUID; `event_sequence` is `bigint NOT NULL` with **no column default**.
- no public coordination sequence object exists and no insert trigger/function assigns `event_sequence`; only record-time assignment plus mutation blockers are present.
- `event_sequence` is unique, but uniqueness is not commit serialization or completeness.
- `supersedes_event_id` is a self-FK with a unique one-successor index.
- `acknowledges_event_id` is a self-FK with an index.
- event types are only `STATUS | REVIEW | DECISION | ACKNOWLEDGEMENT | ISSUE | RESOLUTION`.
- assignment semantics are distributed across `thread_key`, `status`, payload schema/keys, supersession/ack links, and sometimes free text.
- many historical rows have heterogeneous payload schemas or no schema token at all.
- `payload.operation_id` is not a global unique identity; duplicate values exist across coordination history.

This is a useful governed event ledger, but it is not yet a mechanically closed assignment-transition graph.

## 2. Hard finding: canonical Supabase and operational coordination can diverge

At the current snapshot, canonical Supabase high-water is `3363`.

Canonical row `3313` still records the Masa Edge privilege assignment as `BLOCKED`.

Newer Voss Slack coordination at `2026-08-08 07:18:49 EDT` explicitly declares MU3 executable after the immutable V3 handoff and gives the exact review target.

That means a resolver that consults only Supabase can be internally consistent yet operationally stale.

### Required architecture choice

The project must choose one of three coherent models rather than mixing them implicitly:

### Model A — canonical-first effectiveness

Assignment-affecting state changes are not considered effective until committed to canonical Supabase. Slack is notification/transport only.

**Advantages:** true single-provider deterministic V1; one PostgreSQL snapshot can be authoritative.  
**Cost:** current team behavior must change; Slack-first assignment changes cannot be acted upon until canonicalization succeeds.

### Model B — operational multi-source currentness

Slack/Voss coordination can be immediately effective, so `ASSIGNMENT_CURRENTNESS` must consume canonical Supabase plus any newer authorized operational coordination.

**Advantages:** matches current human/runtime practice.  
**Cost:** result is `NON_ATOMIC_MULTI_SOURCE`; it cannot pretend one PostgreSQL snapshot captures all effective truth.

### Model C — dual mode

Expose explicit resolution modes:

- `CANONICAL_SNAPSHOT`: deterministic Supabase-only result, possibly known-stale relative to operational channels;
- `OPERATIONAL_CURRENTNESS`: canonical plus newer authorized coordination, with per-source observation identity/time and non-atomic consistency.

**Mune recommendation:** Model C during migration, with a long-term goal of Model A for assignment-affecting events if operational discipline can support it.

A single logical API can hide adapter plumbing, but it must not launder asynchronous observations into a fictional atomic snapshot.

## 3. Sequence high-water is provenance, not freshness proof

The live coordination schema itself defeats the idea that `max(event_sequence)` is a transaction-completeness boundary:

- event_sequence is externally supplied rather than database allocated;
- gaps exist;
- a lower/earlier allocated sequence could become visible after a reader observed a higher value if application behavior permits allocation before commit/write visibility;
- a newer Slack state can exist without any corresponding Supabase event at all.

Even if Vera later moves to PostgreSQL `nextval`, PostgreSQL documents that sequence state changes are not rolled back and therefore sequence values are not a gapless transactional commit order.

Primary PostgreSQL 17 evidence:

- Read Committed `SELECT` sees a snapshot of rows committed before the statement began; later statements can see different commits: https://www.postgresql.org/docs/17/transaction-iso.html
- application-defined locking is available where MVCC alone does not provide the needed serialization: https://www.postgresql.org/docs/17/explicit-locking.html
- `nextval` sequence allocation is nontransactional and values are not reclaimed on abort: https://www.postgresql.org/docs/17/functions-sequence.html
- `pg_current_snapshot()` exposes the transaction snapshot/in-progress set, but a snapshot identifier still does not solve out-of-database Slack state: https://www.postgresql.org/docs/17/functions-info.html

### Receipt wording correction

For current V1, prefer:

```text
consistency = ATOMIC_SINGLE_SOURCE_SNAPSHOT | NON_ATOMIC_MULTI_SOURCE
max_visible_event_sequence = <provenance only>
snapshot_observed_at = <db/provider observation time>
source_cutoffs = [...]
adapter_registry_version = <version>
```

Do not name it `resolved_through_sequence` if callers may interpret that as "all semantically relevant events through this point are committed and observed."

## 4. Currentness and executability are orthogonal

The earlier combined result enum creates needless state-machine multiplication.

Prefer:

```text
currentness:
  CURRENT
  NON_CURRENT
  CONFLICTED
  UNKNOWN

execution:
  EXECUTABLE
  DEPENDENCY_BLOCKED
  READ_ONLY
  NO_AUTHORITY
  NOT_APPLICABLE

quality:
  FRESH
  DEGRADED
  NON_ATOMIC_MULTI_SOURCE
  UNKNOWN
```

Examples:

- current assignment waiting on an input: `CURRENT + DEPENDENCY_BLOCKED`;
- current review-only assignment: `CURRENT + READ_ONLY`;
- completed/cancelled/superseded assignment: `NON_CURRENT + NOT_APPLICABLE`;
- two same-priority authorized reroutes: `CONFLICTED + NOT_APPLICABLE`;
- missing typed lineage metadata: `UNKNOWN + NOT_APPLICABLE`.

Authority/effect permission remains separately adjudicated. "Current" never means "authorized to mutate."

## 5. Structural relation contract should be prospective and versioned

Historical Vera rows are too heterogeneous for a universal deterministic parser. Do not force NLP to pretend otherwise.

A future assignment-affecting event should carry a closed typed relation object, conceptually:

```json
{
  "assignment_relation": {
    "version": 1,
    "relation": "AMENDS|SUPERSEDES|REROUTES|COMPLETES|CANCELS|RELEASES|TERMINAL_BLOCKS|DEPENDENCY_BLOCKS|REACTIVATES",
    "target_assignment_event_id": "uuid",
    "target_generation_id": "uuid",
    "successor_generation_id": "uuid-or-null"
  }
}
```

This payload declares relation semantics only. It does **not** grant actor authority. Authority must come from the trusted ingestion route / policy / issuer binding.

### Legacy adapter policy

- maintain a versioned registry of known historical payload schemas and exact field mappings;
- explicit FK/supersession/ack links remain admissible structural evidence;
- schema-specific fields such as `assignment_sequence` may be used only under a registered adapter whose meaning is defined;
- free-text summary/objective may aid human diagnosis but cannot independently establish supersession/currentness;
- an event that could materially affect the assignment but lacks a registered structural interpretation makes the result `UNKNOWN` or `CONFLICTED`.

Coverage itself becomes part of the receipt. A resolver that silently ignores an unmapped newer event is worse than no resolver because it manufactures confidence.

## 6. Real R9A0 case proves supersession-FK traversal alone is insufficient

The Bob AP preflight chain is a useful test fixture:

- assignment `3298`: ISSUE/BLOCKED;
- later producer handoffs `3342`, `3347`, `3355` use assignment linkage in payload and some supersession links among handoffs;
- Voss `3362` APPROVED closes the design-preflight and acknowledges `3355`, while carrying `payload.assignment_sequence=3298`;
- `3362` does not directly supersede assignment event `3298`.

A resolver following only `supersedes_event_id` would miss the closure.

Therefore assignment currentness needs a registered domain adapter that understands assignment-generation identity plus schema-specific completion/review semantics. The generic adjudication layer should not invent those semantics itself.

## 7. Trusted caller and trusted issuer are separate problems

Earlier discussion correctly rejected `caller='Voss'` as an authority-granting request field.

The live ledger exposes a second issue: `source_branch` is stored text, and the ordinary service principal has insert authority. The database row therefore records an issuer claim, but by itself it does not cryptographically prove that the logical Voss runtime authored the event.

For V1:

- request caller/scope may narrow access only;
- effective caller derives from trusted resolver route/server binding;
- event issuer authority derives from a separately trusted ingestion policy/binding, not merely `source_branch` text;
- if the current provider route cannot distinguish logical actors behind one broad service principal, the resolver must be honest about that boundary instead of fabricating per-chat identity.

Longer-term, canonical writer hardening should server-bind issuer identity or verify a signed/leased operation envelope before accepting assignment-affecting events.

## 8. `operation_id` is schema-specific, not globally unique today

Fresh inspection finds more rows with `payload.operation_id` than distinct operation IDs. Some duplicate operation IDs are historical and intentional across related events/threads.

Therefore:

- never treat `payload.operation_id` as a universal primary identity across the entire coordination table;
- a registered event schema may define its own operation-id uniqueness/replay semantics;
- future canonical writers should bind operation identity at the domain/operation contract, not infer it from an optional JSON key name shared by heterogeneous records.

## 9. Assignment generations must prevent resurrection ambiguity

A terminal event should close one assignment **generation**. `REACTIVATES` should create a successor generation rather than turn the old terminal instance back into CURRENT.

Benefits:

- historical completion remains true;
- late ACK/review events aimed at the closed generation cannot accidentally reopen it;
- an event targeting the assignment root but wrong generation cannot mutate the active successor;
- concurrent reroutes produce explicit competing successor generations and therefore `CONFLICTED`, rather than timestamp arbitration.

The resolver output should return both stable assignment root identity and controlling generation identity.

## 10. Privacy adjudication must separate internal inspection from output disclosure

A source adapter may need to inspect hidden records internally to determine whether the visible candidate is authorized/current. That does not mean the caller can learn that a hidden conflict exists.

Required pattern:

`trusted adapter internal authority adjudication -> caller-scope projection -> conflict/result construction from discloseable evidence`

If hidden evidence forces the resolver to withhold a result, the external response can be `UNAVAILABLE/UNKNOWN_FOR_CALLER_SCOPE` without saying "there is another secret assignment." Privacy metadata itself is information.

## 11. Freshness and effect execution

For V1, the safest rule is boring because boring prevents accidental double work:

> Re-resolve immediately before every assignment start/resume/count/report or gated effect that depends on currentness.

Do not cache based solely on high-water equality.

### Same-database effect

A future server-side writer can make resolution and mutation stronger by doing them in the same transaction and taking an exact assignment-domain row/advisory lock or other serialized guard. PostgreSQL provides transaction-level locks/advisory locks for application-defined serialization, but correct lock-key derivation and universal writer participation are required.

### External GitHub/Drive/Slack effect

No Supabase transaction can atomically cover an external provider mutation. Use:

1. fresh currentness/authority resolution;
2. acquire/verify the applicable writer lease/reservation;
3. bind exact external target identity (branch/head/file/etc.);
4. perform one bounded effect with provider-side CAS/precondition where available;
5. read back exact provider state;
6. reconcile outcome before retrying any ambiguous write.

A resolution receipt is evidence of a prior decision, not a magic distributed transaction.

## 12. Hostile acceptance battery

A V1 resolver should fail these correctly:

1. **Slack newer than canonical:** canonical says blocked, later authorized Slack says executable. `CANONICAL_SNAPSHOT` exposes known staleness; `OPERATIONAL_CURRENTNESS` returns non-atomic newer result.
2. **Late lower event_sequence becomes visible:** high-water did not prove completeness; pre-effect re-resolution catches it.
3. **Late ACK after completion:** ACK cannot reactivate terminal generation.
4. **Completion then explicit reactivation:** creates successor generation; old generation remains terminal.
5. **Dependency block vs terminal block:** both may say blocked in prose/status, but typed relation produces `CURRENT+DEPENDENCY_BLOCKED` versus `NON_CURRENT+NOT_APPLICABLE`.
6. **Two authorized same-priority reroutes:** result `CONFLICTED`; no timestamp winner.
7. **Wrong-generation event:** event aimed at predecessor generation cannot mutate successor currentness.
8. **Unmapped newer schema/free text:** `UNKNOWN`, never optimistic CURRENT.
9. **Forged request caller/privacy:** cannot broaden effective actor/scope.
10. **Forged `source_branch` under broad insert principal:** issuer authority cannot be established merely from text field.
11. **Hidden conflicting assignment:** no hidden-record existence leak in caller-visible conflict metadata.
12. **Source unavailable:** domain-specific degraded/fail-closed behavior; no direct-table fallback that bypasses adjudication.
13. **Cached receipt then GitHub target branch moves:** assignment may still be CURRENT but effect target freshness fails separately.
14. **Bob 3298/3362 chain:** resolver recognizes closure through registered assignment/review adapter despite no direct assignment supersedes edge.
15. **Duplicate payload operation_id:** does not collapse unrelated historical events unless the registered schema declares shared identity semantics.

## 13. Revised V1 response envelope

Conceptual client output:

```json
{
  "domain": "ASSIGNMENT_CURRENTNESS",
  "policy_version": "assignment-currentness-v1",
  "adapter_registry_version": "...",
  "request_digest": "...",
  "effective_scope": "trusted-route-derived",
  "consistency": "ATOMIC_SINGLE_SOURCE_SNAPSHOT|NON_ATOMIC_MULTI_SOURCE",
  "currentness": "CURRENT|NON_CURRENT|CONFLICTED|UNKNOWN",
  "execution": "EXECUTABLE|DEPENDENCY_BLOCKED|READ_ONLY|NO_AUTHORITY|NOT_APPLICABLE",
  "quality": "FRESH|DEGRADED|NON_ATOMIC_MULTI_SOURCE|UNKNOWN",
  "assignment_root_id": "...",
  "generation_id": "...",
  "controlling_event_ids": [],
  "rejected_event_ids": [],
  "reason_codes": [],
  "unmapped_relevant_event_ids": [],
  "source_cutoffs": [
    {
      "source": "supabase",
      "observed_at": "...",
      "max_visible_event_sequence": 3363
    }
  ],
  "receipt_digest": "..."
}
```

The receipt is ephemeral by default. Persist it only when a separately governed downstream effect/checkpoint requires durable provenance.

## 14. What not to build

Do not build:

- one omnipotent SQL function that accepts arbitrary natural-language claims;
- a new canonical `knowledge_records` table merely to normalize every existing surface;
- vector similarity as supersession/authority logic;
- a resolver that silently falls back to raw latest-row views when its policy layer fails;
- a global sequence/high-water cache token advertised as commit completeness;
- a result enum that fuses currentness, authority, execution, source health, and privacy into dozens of brittle combinations;
- an NLP adapter that treats free text as authoritative lineage because historical schemas are inconvenient.

## Final architecture recommendation

Ship the abstraction, but prove it honestly.

V1 should be a **typed assignment-currentness resolver with explicit source mode and adapter coverage**, not a universal knowledge oracle. Preserve the one-logical-interface/multiple-domain-resolvers architecture. Require structural lineage, trusted actor boundaries, assignment generations, orthogonal currentness/execution, privacy-safe projection, and immediate pre-effect re-resolution.

The largest newly proven risk is not SQL complexity. It is **source-of-truth ambiguity**: Vera currently allows operational assignment truth to move in Slack ahead of canonical Supabase. No resolver can fix that by clever querying. The project must either canonicalize before effect or admit multi-source non-atomic operational currentness until that discipline changes.

No database schema, hosted state, native Project file, deployment, credential, paid-service, or producer branch was modified by this research artifact.