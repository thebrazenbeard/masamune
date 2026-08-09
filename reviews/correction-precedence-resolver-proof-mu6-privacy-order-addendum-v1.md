# Mune MU6 Addendum — Privacy Ordering Must Not Change Currentness

**Parent assignment:** `VOSS-20260808-MU6` / root sequence `3464`  
**Parent proof:** `reviews/correction-precedence-resolver-proof-mu6-v1.md` @ `2019b3f1714dca9e12534f17f0a0590e0a5fb278`  
**Class:** read-only semantic correction  
**Provider mutation:** none

## Defect

The parent proof's privacy section currently says to identify only records eligible for the caller/service privacy domain and then construct the correction lineage from that eligible subset.

That ordering can change the graph itself.

Minimal counterexample:

- visible record `r` is the apparent root;
- hidden same-scope record `h` supersedes `r`;
- the full trusted graph has unique leaf `h`;
- caller-visible filtering removes `h` before graph construction;
- the visible subset now has unique leaf `r`.

A read-only synthetic CTE against the live Vera Supabase provider reproduced exactly:

```text
true_leaf                 = h
visible_subset_leaf       = r
false_currentness_if_filtered_first = true
```

No current live `(project_id, branch_id, record_key)` group was observed with more than one `privacy_scope`, so this is a verified design defect, not a claim of a current live corrupted lineage.

## Corrected boundary

Privacy minimization and currentness adjudication must remain separate.

1. Derive the trusted resolver/service authority and exact correction scope server-side.
2. Build and validate the **full authority-eligible correction graph required for the currentness decision**. Do not reduce the graph to caller-visible rows first.
3. Resolve topology/currentness and semantic adapter status internally.
4. Separately derive what the caller is authorized to learn from that result.
5. If the caller lacks enough visibility to expose or independently substantiate the controlling lineage, return a non-leaking generic result such as `UNRESOLVED_INSUFFICIENT_VISIBLE_CUSTODY` / `UNAVAILABLE_FOR_CALLER` rather than a visible-subset currentness result.
6. Never reveal hidden record IDs, hidden sibling/successor existence, private statements, or exact conflict topology to an unauthorized caller.

The critical invariant is:

> **Privacy may redact evidence and force an unresolved result; it must never delete graph nodes in a way that changes which record is current.**

This is compatible with the parent proof's intended non-leakage requirement but corrects its implementation order.

## Revised acceptance invariant

Replace the earlier privacy-order shorthand with:

```text
TRUSTED_FULL_GRAPH_CURRENTNESS
    -> CALLER_VISIBILITY_PROJECTION
    -> PRIVACY_MINIMIZED_RESULT
```

not:

```text
CALLER_VISIBLE_ROWS
    -> GRAPH_CURRENTNESS
```

A hidden required node therefore cannot make an older visible row regain control.

## Bug receipt

Vera `bug_ops` canonical report:

- bug: `1be2c5ab-2eee-4916-ad07-8d5a7ca84455`
- report event: `4254ef4c-d97c-4ab2-a4e3-5fc76244809d`
- operation: `9fd58a31-6a47-444f-8849-bf4660c586c8`
- dispatch: `bed16d3c-4301-4200-8625-8eb3f84387f7`
- queue message: `16`

Exact readback confirmed `REPORTED` plus operation receipt plus `ENQUEUED` custody.

## Effect on MU6 verdict

The parent topology result remains viable after this correction. The verdict becomes:

`PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT_AND_PRIVACY_ORDER_CORRECTION`

No schema, save-state row, provider configuration, credential, canonical memory, or producer branch was modified.