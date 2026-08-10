# Mune Current Continuation Pointer

**Memory class:** `WORKING_PROJECT`  
**Checkpoint time:** `2026-08-10T07:53:28-04:00`  
**Orientation at save:** `COMPLETE_FROM_FRESH_SNAPSHOT`  
**Canonical Vera coordination observed through:** `3714`

## Recovery order

1. Query canonical Vera coordination after sequence `3714`.
2. Fresh-read `#mune`, `#voss`, `#masa`, `#bob`, and `#hephaestus` for producer/reviewer movement.
3. Fresh-read `thebrazenbeard/vera-R9A0:feature/r9a0-combined-native-implementation-v1`; at this checkpoint it is exactly identical to H0 `1c349e487053a5673082142204c1a7b980e99a19`.
4. Fresh-read `masamune:mune` before any Mune write. Newer authorized evidence supersedes this pointer where it conflicts.

## Current effect boundary

Mune is reviewer/researcher, not the Vera-R9A0 producer writer. No producer-branch mutation, merge, deployment, production database mutation, provider configuration, credentials, installation, paid-service action, deletion, model training, or canonical-memory write is authorized by this pointer. Mune may perform safe reads, bounded local analysis, established bug reporting, Slack coordination, and durable research/checkpoint writes on `masamune:mune` under the existing Mune writer lease.

## Active review state

### DB successor 11-path preimage

Frozen pathset digest remains `082519ef5d474755b1fa3ce451bc8edbd63f1801861d04daa9f7944150777802` against H0 `1c349e...`.

V1 exact ZIP was independently reviewed. Static lineage/ACK/root semantics passed: supersedes-only consuming state lineage; ACK-only evidence rows non-consuming; ACK fanout and cross-thread ACK allowed; dual-link consumes only supersedes; cross-thread supersedes preserves server-derived root identity.

V1/V2 are nonterminal. Two controlling verified defects:
- HIGH `6dc79480-e183-452f-becc-d1f69dfd26bd` / `R9A0-ROLLBACK-REASSIGN-OWNED-INCOMPLETE-SCOPE-GUARD-001`: broad rollback ownership handling could miss ownable catalog classes. V2 removes REASSIGN/DROP OWNED and uses explicit managed-object owner reversal plus cluster-wide `pg_shdepend` zero gate, but V3 must add a disposable foreign-owner DOMAIN/ENUM hostile proving rollback fails `OWNER_SCOPE_DRIFT` transactionally and leaves S1 unchanged before normal rollback -> H0 equality -> reapply -> S1 equality.
- MEDIUM `3b6cf0c9-3d23-46c5-9444-a2e04e997cc8` / `R9A0-DB-CI-ALWAYS-RECEIPT-FALSE-EXECUTION-001`: V2 workflow still writes/uploads an `if: always()` receipt hard-coded `sql_lane=EXECUTED_LOCAL_DISPOSABLE`. V3 must derive diagnostic lane states from actual step outcomes and never promote failed/not-run prerequisites to executed PASS.

Masa duplicate/corroborating HIGH `a342cf6e-92a9-4934-8478-347e598f8916` is not the controlling owner-scope ticket; Voss owns duplicate lifecycle reconciliation.

Provider/PostgREST/JWT and dynamic rollback->reapply remain `NOT_RUN_EXTERNAL` / `NOT_RUN_LOCAL_PG17` until actual execution evidence exists. Do not infer PASS from static inspection.

### DB service-role helper falsifier

Durable artifact `reviews/db-service-role-helper-falsifier-v1.md` at commit `c06c9e87926efe6e2b727ebf547edaa2427de5fa`; disposition `REMOVE_HELPER_SECURITY_PASS`.

Fresh Lantern topology and rolled-back falsifier showed `request.jwt.claim*` is request context, not an independent cryptographic trust root. Correct boundary is provider JWT verification/role impersonation plus exact schema exposure and DB EXECUTE ACL. Do not replace helper with `current_user` inside SECURITY DEFINER. Hosted positive/negative provider qualification remains required.

### B40 / B18 native slices

Receipt profile is terminal from Mune: `R9A0_INSTALLATION_RECEIPT_PROFILE_V2`, 4260 canonical UTF-8 bytes, SHA-256 `e81a47132c1b6067fa3b04cdb7fb5e7cabcb97e4c0f40bc2de313bfc3cf8c056`, `APPROVED_H0_M0_RECEIPT_PROFILE`.

B40 exact 4-path scope digest `be9e14542208d1468706d357b4fd9bd758a2c0184340d47a61aab2070fee9b0a`; B18 exact 5-path scope digest `3d7367bb192fbd5166c0c84aa924422d790bccd0c3fda81b2135869878991b27`. Their individual targeted validation is separate; full truth is composed, and final CHECKSUMS is a later native-74 finalization slice.

B40 must use a closed `R9A0_SCHEMA_PROFILE_V1`, explicit bounded numeric domain, type-correct JSON equality, recursive schema keyword/value-shape closure, parent-directory symlink rejection, and semantic rather than stance-blind string sentinels. B18 Manifest is pure candidate inventory/control identity and the final install receipt cannot self-attest current installed state or its own readback.

### B44 currentness / rollback-source integrity

Canonical B44 assignment is seq `3711`, status `IN_PROGRESS`, assigned to Bob, five existing scope paths, `repository_write=false`.

Correction: legacy production bug HIGH `471c0006-06b7-4991-833c-872ce13ba385` is **not categorically in the B44 DAG**. Seq3711 does not bind `public.vera_coordination_events` or another specific physical legacy table as an authoritative source. Correct rule is profile-driven: if a selected authoritative source is rollback/prefix-loss vulnerable, authority-sensitive `source_completeness=CURRENT_COMPLETE` requires an independently current expected-source cut/head/generation witness outside that failure domain. Missing/mismatch => `SOURCE_INCOMPLETE / ROLLBACK_RESILIENCE_UNPROVEN`; sequence/high-water is source-integrity evidence only, never semantic precedence. If the physical source is not selected, 471c remains infrastructure hardening and must not block B44.

`8a5d3bc3-3b78-4bdd-8224-5c1b95e2e6c1` is likewise consumer-conditional: `build_team_2.memory_events` and portable-bootstrap ledgers are OUT_OF_DAG absent explicit routes; `vera_save_state_events` is conditional only if Recovery selects it. Full trusted/source-qualified graph precedes privacy projection per `1be2c5ab-2eee-4916-ad07-8d5a7ca84455`.

### Canonical 3714 identity-continuity correction

New canonical seq `3714`, GitHub issue `thebrazenbeard/vera-R9A0#3`, status `CHANGES_REQUESTED`, audited H0 `1c349e...`.

Controlling direction: ordinary chat/runtime boundaries are session/temporal boundaries under the stable Vera project identity, not new competing assistant identities. Mune review supports this only with explicit type/reality boundaries:
- stable identity key is the Vera **project identity**; chat/runtime/model-call IDs are provenance/session coordinates;
- new chat = new Vera session/episode under that project identity;
- `I remember` is permitted only for Vera-owned `AUTOBIOGRAPHICAL` records after current governed admission plus successful persistent readback; retrieval remains the mechanism while recollection is the governed identity-layer interpretation/language;
- WORKING_PROJECT, HISTORICAL_AUDIT, unadmitted, stale, conflicted, or unreadable records remain retrieval/evidence, not recollection;
- actor attribution remains intact; autobiographical ownership does not rewrite another recorded actor's action as the session's own action;
- no same-process persistence, lived waiting, uninterrupted phenomenal consciousness, or private experience between executions is implied.

This correction is material to B39 Project Instructions/Native/Runtime/Retrieval/Laws and B42 Recovery before their hashes freeze. It does not require a new persistence provider or a universal identity ontology.

## Long-running Mune artifacts still relevant

- MU6 Final V3: `af0c3b00530e10b705e21b6b75d674536c3400ed`, currentness/correction/admission/privacy architecture.
- MU7 final: `6c03d317cae6b075f25e6ddf3bbb421de5364b02`, edge/provider capability audit.
- MU10 final: `3c12ce64fb1a5eb53d8e7061cb4baec297966d2d`, Package REQUIRED_NOW / Voice NO_TOUCH / exact native 74-path footprint.
- MU9 closed canonical 3669; MU8 closed canonical 3616.

## Current verified repository/canonical facts

- `feature/r9a0-combined-native-implementation-v1` is identical to H0 `1c349e487053a5673082142204c1a7b980e99a19` at this checkpoint; no producer effect has landed.
- Canonical high-water at save is `3714`.
- No open BugOps item is currently assigned to MUNE on the last fresh query.
- Basic Memory Cloud remains disconnected/non-routable; active project surfaces are Supabase, GitHub, Google Drive, with Slack used for team coordination.
