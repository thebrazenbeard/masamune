# Masamune Product Thesis

## Positioning

Masamune is not positioned as a generic AI code reviewer.

The product thesis is:

> Find defects the existing review process missed, then make a second
> deliberately different reviewer try to disprove the finding before spending
> developer attention on it.

The differentiator is adversarial qualification, exact-subject evidence, and
longitudinal repository failure knowledge.

## Commercial surface

Potential hosted tiers can be separated by capability rather than by hiding the
core evidence model:

- public/open-source evaluation tier;
- private-repository PR review;
- issue investigation;
- continuous/scheduled defect sweeps;
- repository failure memory;
- sandboxed test qualification;
- candidate repair PRs;
- organization policy/audit controls;
- dedicated or self-hosted enterprise execution.

Pricing is intentionally not encoded here. Inference, repository retrieval,
sandbox execution, and retention costs must be measured before plan limits are
treated as sustainable.

## Moat hypothesis

The long-term defensible asset is not a prompt.

For each authorized repository, Masamune can accumulate an evidence graph:

```text
incident
  -> root cause
  -> violated invariant
  -> affected subsystem
  -> repair
  -> regression test
  -> later changes touching the same invariant
```

That graph should remain customer-scoped and provenance-bound. It can make
future review more useful without claiming neural-weight learning or exposing
one customer's private history to another.

## Anti-goal

An inexpensive plan that emits unlimited speculative findings is not the
product. High-volume low-signal review destroys developer trust and can make
model cost structurally unprofitable.
