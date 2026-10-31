> **License:** Masamune's original material is source-visible proprietary material, **not open source**. Private noncommercial review and evaluation are permitted under [LICENSE](LICENSE); commercial use, redistribution, hosted services, and publication of derivatives require separate written permission. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Third-party assets retain their own rights.

# Masamune — evidence-bound two-reviewer protocol

Masamune is a reusable **review method and early orchestration research workspace** for investigating software defects and proposed changes. It separates root-cause analysis, adversarial challenge, evidence reconciliation, and regression qualification so that agreement between reviewers is never mistaken for independent proof.

The two reviewer roles are named **Masa** (initial technical analysis) and **Mune** (blind scan and hostile challenge). They describe responsibilities, not the identity or authority of a particular AI model, computer, or person. A host may apply the method with appropriately isolated reviewers, but this repository does **not** ship a complete, runnable review service.

## What exists in this repository

| Component | Current evidence | Limit |
| --- | --- | --- |
| [Current execution protocol](PROTOCOL_V2_CURRENT.md) | Defines bounded reversible work, shared-writer coordination, independent verification, and protected-effect boundaries | A documented process, not a technical authorization service |
| [Orchestrator research module](supabase/functions/masamune-webhook/orchestrator.ts) | Sketches separate Masa/Mune model requests, challenge, evidence receipts, and reconciliation, with bounded selected-file context | **Not independently runnable:** sibling imports for configuration, model calls, evidence, hashing, reconciliation, and types are absent from the current tree |
| [Workspace startup-safety tests](tests/test_workspace_startup_safety.py) | Reject known concealed VS Code folder-open execution and pseudo-font executable paths in the checked-out source | Source-tree checks only; not a workstation, installed-extension, or deployment audit |
| [Historical continuation notes](state/continuation/) | Project-specific prior coordination records | Historical context, not current API documentation or proof of present authority |

### Apply the review method

For a repository change, the intended review sequence is:

1. **Pin the subject.** Record the repository, exact source commit or pull-request head, changed paths, declared behavior, and the bounded material each reviewer can inspect.
2. **Analyze independently.** Have an initial reviewer identify likely defects, while a second reviewer performs a blind assessment before seeing that first report.
3. **Challenge assertions.** Require both reviewers to connect material claims to reproducible source, test, or system evidence. Seek counterexamples and distinguish inferred risk from observed failure.
4. **Reconcile discrepancies.** Preserve disagreements and evidence gaps. A missing finding is **not** evidence of absence, and two models agreeing is not independent physical verification.
5. **Qualify the exact change.** Run relevant regression checks against the same pinned subject; record skipped tests, environmental restrictions, and test-versus-deployment boundaries.
6. **Gate effects at the host.** The host resolves writer conflicts and authenticates the actor, provider, scope, and consent before merges, deployments, credential use, destructive operations, or other protected effects. A model-produced recommendation grants no permission.

These are **instructions for using the method**; steps 1–6 are not claimed as automated operations of the current checkout.

## Reproduce available source validation

Python 3 with the standard library is sufficient for the tracked source checks:

```bash
python3 -B -m unittest discover -s tests -v
```

The three tracked tests inspect `.vscode` startup configuration and reject the known pseudo-font executable mechanism. They do not invoke review models, launch a Supabase service, or contact a live provider. The public orchestration fragment cannot currently be compiled as a standalone webhook from this repository because its local dependencies are missing. No ready-to-run installation or deployment command is advertised.

## Governance and evidence boundaries

- **Assignments:** A specific authorized task permits its necessary bounded and reversible inspection or isolated setup. Shared mutable writes still require single-writer coordination; consequential effects require the applicable host authority.
- **Review:** Source inspection, unit tests, model review, real-system probes, and formal verification are different evidence classes. Cite which one supports each conclusion.
- **Identity:** Names such as Masa and Mune are reviewer roles. Their messages and model-provider labels do not establish immutable provider identity, real-human consent, or authenticated execution authority.
- **Scope:** An inspection limited to selected files, bytes, or samples may miss important defects. A resolved review is not a guarantee of safety outside the inspected scope.
- **Security:** The present `.vscode` safety tests cover a previously removed workspace-startup vector in the current tree. Older checkouts, host settings, extensions, and credentials require separate examination.

For the normative local execution boundaries and regression conditions, read [PROTOCOL_V2_CURRENT.md](PROTOCOL_V2_CURRENT.md). For contribution and licensing terms, read [CONTRIBUTING.md](CONTRIBUTING.md), [CLA.md](CLA.md), [LICENSE](LICENSE), and [NOTICE](NOTICE).

**Status:** Protocol and incomplete orchestration prototype. No packaged service, deployable webhook, host-owned authorization server, provider attestation, independent reviewer runtime, or end-to-end integration qualification is established by this repository's current source and tests.
