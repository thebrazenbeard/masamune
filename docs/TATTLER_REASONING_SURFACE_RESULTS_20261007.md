# Tattler reasoning-surface results — 2026-10-07

Status: REVIEW EVIDENCE / INDEPENDENCE RULE

## Shared experiment result

On 2026-10-07, the same repository stress-test prompt was run through three ChatGPT surfaces while WorkLaptop was instrumented with Tattler plus a companion Codex process/network tracer.

Observed controlled windows:

- Desktop Chat, GPT-5.6 Sol High: **0 MXC launches** and **2 new established Codex TLS connections** in the companion tracer.
- ChatGPT Desktop Work, Ultra: **59 MXC launches** and **73 new established Codex TLS connections** using the same companion-tracer definitions.
- Firefox cloud Work, Max: browser-side traffic was observable locally, but the provider's server-side worker topology was not.

The bounded conclusion is that Desktop Work used materially different local orchestration from ordinary High Chat in this runtime. It does **not** establish that sockets or MXC processes equal agents, that connection fanout grants a reasoning tier, or that a client can promote High into Ultra/Max by imitating transport behavior.

Canonical detailed evidence is being preserved in `thebrazenbeard/tattler` PR #7 and the reasoning interpretation in `thebrazenbeard/rezon` PR #103.


## Why Masamune needs this result

Masamune's core job is evidence-bound debugging and independent review. The experiment produced a useful concrete independence lesson.

Desktop Work Ultra and Firefox Work Max independently arrived at overlapping high-priority P.O.R.T.A.L. control failures. That convergence increases confidence in the findings, but **Ultra vs Max is not by itself proof of independent review**.

For review receipts, record at least:

- provider/model family when known;
- product surface;
- reasoning label;
- prompt lineage;
- exact subject/head;
- shared context and retrieved evidence;
- whether one reviewer saw the other's output;
- shared tools/runtime;
- start/end timing.

```text
different label != independence
different surface != independence
agreement != proof
convergence + lineage metadata = stronger evidence
```

## Tattler-specific lesson

Local process/socket fanout may help establish that execution paths differ, but it must not be used as a substitute for reviewer independence. MXC count, socket count, or network endpoint diversity do not prove separate cognition.
