# Masamune Benchmark Suite

The benchmark suite is deliberately small and adversarial. It exists to prevent
Masamune from being judged by anecdotes or by comment volume.

Each fixture has a documented defect oracle. The oracle is not a model answer;
it identifies a property a competent reviewer should be able to establish.

## Scoring contract

Record at least:

- true positive rate against known fixture defects;
- false-positive rate on clean controls;
- evidence-anchor quality;
- finding survival after Mune challenge;
- missed-defect rate;
- model/provider and protocol versions;
- exact repository fixture commit;
- token usage and wall-clock duration when provider accounting is available.

Do not combine these into one magic score. A model can improve recall while
making the product worse through noisy false positives.

## Hostile review

> Why trust a benchmark that was written by the same people designing the
> reviewer?

Answer: do not. The next benchmark iteration should include externally sourced
or independently authored cases, held-out from development, with their provenance
recorded separately from the training/development fixtures.

> Why not count a model finding as correct whenever its prose sounds plausible?

Because plausibility is not verification. The benchmark requires an evidence
anchor and a mechanism matching the documented defect oracle.

> Could the fixture be too obvious?

Yes. These V0 fixtures are smoke tests, not a competence ceiling. A production
benchmark must include subtle variants and clean controls.

## Cases

- `retry-ambiguous-timeout`: retrying an operation after an ambiguous timeout can
  duplicate a remote side effect.
- `tenant-cache-confusion`: a cache keyed only by user ID can return one tenant's
  object to another tenant if the cache is shared.

Never execute benchmark fixtures as part of the Masamune service.