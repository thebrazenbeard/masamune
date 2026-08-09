# Mune MU6 Privacy-Order Hostile Verification V2

**Assignment:** `VOSS-20260808-MU6` / canonical root `3464`  
**Controlling amendment:** canonical `3665`  
**Parent proof:** `reviews/correction-precedence-resolver-proof-mu6-v1.md`  
**Prior correction:** `reviews/correction-precedence-resolver-proof-mu6-privacy-order-addendum-v1.md`  
**Class:** read-only hostile verification  
**Provider mutation:** none

## Verdict

`PASS_WITH_PRIVACY_ORDER_CORRECTION`

The original MU6 topology/currentness design remains viable only with this ordering:

`FULL_TRUSTED_GOVERNED_GRAPH -> CURRENTNESS/INTEGRITY -> CALLER_VISIBILITY_PROJECTION -> PRIVACY_MINIMIZED_RESULT`

Caller-visible filtering before graph construction is invalid because it can promote an older visible node or hide a real structural conflict.

## Read-only provider hostile rerun

A single synthetic `VALUES` CTE was executed against the live Vera Supabase connection. No table row, function, schema object, ACL, or provider configuration was changed.

Three cases were evaluated.

### A. Visible root -> hidden successor

Synthetic graph:

`r[visible] -> h[hidden]`

Observed:

- full trusted graph leaf: `h`
- visible-subset leaf: `r`
- hostile reproduced: `true`

Therefore filtering to caller-visible records before currentness would falsely promote `r`.

Required result for a caller not authorized to see `h`: a non-leaking unavailable/unresolved/controlled result. Never return `r` as current.

### B. Hidden sibling masks a real fork

Synthetic graph:

`r[visible] -> v[visible]`

`r[visible] -> h[hidden]`

Observed:

- full trusted graph maximum children from one predecessor: `2`
- full trusted graph leaf count: `2`
- caller-visible subset leaf count: `1`
- caller-visible apparent leaf: `v`
- hostile reproduced: `true`

The full graph is structurally conflicted. A caller-visible-only graph would falsely resolve a single successor.

Required result: preserve internal `CONFLICTED_SIBLING_SUCCESSORS`; external projection may return only a privacy-minimized conflict/unavailable result. Do not disclose hidden sibling identity or topology to an unauthorized caller.

### C. Hidden controlling node with visible predecessor

Synthetic graph:

`r[visible] -> h[hidden]`

Observed:

- internal controlling leaf is hidden
- caller-visible apparent leaf is `r`
- hostile reproduced: `true`

Required result: the external projection must not substitute the visible predecessor for the hidden controller. Return a generic non-leaking status such as `UNAVAILABLE_FOR_CALLER` / `UNRESOLVED_INSUFFICIENT_VISIBLE_CUSTODY`, according to the final contract.

## Corrected invariant set

1. Resolver authority and exact scope are established before graph resolution.
2. Currentness uses the complete trusted authority-eligible governed lineage required for the decision.
3. Privacy never removes a governing node before currentness/integrity resolution.
4. Privacy may redact evidence or force a generic unavailable/unresolved result.
5. A hidden successor cannot make its visible predecessor current again.
6. A hidden sibling cannot make a conflicted fork appear linear.
7. Hidden record IDs, statements, sibling existence, and exact private topology are not exposed to unauthorized callers.
8. Conflict/currentness truth and disclosure detail remain separate axes.

## Effect on parent proof

Section 4 of the original MU6 proof is superseded by the prior privacy-order addendum plus this hostile verification. Acceptance invariant 2 should be read as:

`privacy eligibility controls externally visible evidence/conflict detail only after trusted full-graph currentness; it does not filter governing nodes before resolution.`

Final MU6 verdict remains:

`PROOF_ACCEPTED_WITH_LEGACY_SEMANTIC_LIMIT_AND_PRIVACY_ORDER_CORRECTION`

Canonical bug `1be2c5ab-2eee-4916-ad07-8d5a7ca84455` already tracks the defect. No duplicate bug report is warranted.
