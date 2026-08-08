# Masamune Branch Status / Convergence Map

**Observed:** 2026-08-08 EDT  
**Evidence class:** repository-topology aid, not canonical Vera assignment authority  
**Repository:** `thebrazenbeard/masamune`  
**Default branch:** `collab`

This file exists because branch names are not a governance system, no matter how much GitHub would like us to pretend otherwise.

Before any write/review/convergence effect, fresh-read the exact target branch/head and current Vera writer lease. This map is descriptive and may become stale.

## Branch roles

### `collab`

**Purpose:** shared/default convergence base.  
**Exact head observed:** `9136b6a68859ceccea7fb4c4d03d3ff924f7d991`.

Current observations:

- repository default branch;
- common merge base for current `masa` and `mune` work;
- does not currently contain the later Masa design packet series or Mune review/research series.

Do not infer that content existing on `masa`/`mune` is accepted into shared convergence merely because it exists in this repository.

### `masa`

**Purpose:** Masa producer/design work branch.  
**Exact head observed:** `984cbdc781aa643443652f41f5a710f59e2d2439`.  
**Relative to `collab`:** 12 commits ahead / 0 behind at observation.

Current head is the immutable 3313 Edge privilege V3 publication:

`design/R9A0_EDGE_REPOSITORY_FIRST_PRIVILEGE_PACKET_V3.md`

Masa's current continuation state says the V3 writer lease is consumed and `masa` must not move without a fresh writer stage.

### `mune`

**Purpose:** Mune independent review, adversarial research, and Mune continuation state.  
**Exact head before creation of this map:** `97047b08afbcd94ecc53cce830605a8f3c7d1189`.  
**Relative to `collab`:** 30 commits ahead / 0 behind before this map commit.

Primary Mune surfaces:

- `reviews/**`
- `research/**`
- `state/CURRENT.md`
- `state/checkpoints/**`

Mune review artifacts do not patch Masa's immutable reviewed targets. Mune's repo write authority does not imply authority to merge/converge the branch.

### `continuity/masa`

**Purpose:** isolated Masa continuation/save-state route.  
**Observed topology:** 3 commits ahead / 0 behind `masa` at observation.  
**Continuity file:** `state/masa/CURRENT.md`.

Masa's own continuity contract says continuity commits must never move `masa` or an immutable review target. Treat this branch as WORKING_PROJECT recovery evidence, not producer publication/convergence.

The current connector observation used for this map did not expose the branch-tip SHA directly, so this map intentionally does not invent one. Fresh branch/ref verification remains required before relying on the mutable branch.

## Convergence status

Current branches are intentionally separated:

```text
collab @ 9136b6a...
  ├─ masa  -> design artifacts, current exact head 984cbdc...
  │    └─ continuity/masa -> save-state commits only
  └─ mune  -> reviews/research/continuation, current work lane
```

No merge/rebase/convergence of the current Masa or Mune branches into `collab` is claimed by this file.

A future convergence stage should require:

1. Voss/Patrick exact scope and writer lease for the convergence target;
2. fresh exact branch heads for `collab`, producer branch, and review branch;
3. identification of which artifacts are accepted/current versus historical/superseded;
4. no blind merge of Mune review history into producer design merely because both are useful evidence;
5. conflict review and exact-tree/readback after convergence;
6. preservation of immutable review targets and provenance;
7. fresh CI/validation where convergence changes any code/executable contract;
8. explicit disposition for continuation-only state paths before they enter a shared product branch.

## Artifact status convention

Use these meanings when reading the repository:

- **producer design artifact:** proposal/specification on `masa`; not automatically reviewed or implemented;
- **Mune review artifact:** independent verdict bound to an exact target; not itself producer code;
- **research artifact:** adversarial/design analysis; evidence/input, not automatic project policy;
- **continuation checkpoint:** WORKING_PROJECT resumption aid; always refresh current authority/state before acting;
- **shared convergence artifact:** only content explicitly admitted to `collab` or another designated shared branch under an authorized convergence stage.

## Current caveat

This map fixes discoverability, not governance. Branch purpose is documented here, but actual writer authority/currentness continues to come from Vera coordination and Patrick's present authority. If newer coordination contradicts this map, the map is stale and must not win merely because Markdown looks official.