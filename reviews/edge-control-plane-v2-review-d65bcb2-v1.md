# Mune Independent Review: R9A0 Edge Control-Plane V2

**Reviewer:** Mune
**Candidate repository:** `thebrazenbeard/masamune`
**Exact candidate head:** `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`
**Controlling artifact:** `design/R9A0_EDGE_CONTROL_PLANE_PROPOSAL_V2.md`
**Normative companion:** `design/R9A0_EDGE_CONTROL_PLANE_PROPOSAL_V1.md` V1.1 at the same head
**Verdict:** `APPROVED_DESIGN_KEEP_AND_DEFER`
**Deployment authorized by this review:** No
**Credential/database apply authorized by this review:** No

## Scope

This rereview evaluates the exact immutable V2 candidate against Mune findings `MUNE-EDGE-001` through `MUNE-EDGE-004`. It does not approve deployment, hosted mutation, credential creation, database migration, paid service use, or a generic privileged Edge gateway.

The `masa` branch was verified identical to the bound candidate head during review. The transition from V1.1 head `a79b1dea515569254fd49a885564c554481027e4` to `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14` adds only the explicit V2 Edge and AP controlling artifacts.

## Finding closure

### MUNE-EDGE-001: semantic actor impersonation

**CLOSED.** V2 separates authentication from semantic authorization and requires a default-deny actor record binding actor/key identity to permitted `source_branch`, thread prefixes, event types, and target prefixes. A valid signature is insufficient to claim another actor's semantic identity. Wildcards require explicit governing authority and hostile tests.

### MUNE-EDGE-002: broad Edge admin/service credential

**CLOSED AT DESIGN LEVEL.** V2 rejects the project-wide `service_role` credential for deployment and requires a dedicated non-owner execution principal with only the fixed governed append capability. If a narrow principal cannot be implemented without duplicating transition semantics, the design requires Edge deployment to be rejected rather than falling back to broad privilege.

This is the correct least-privilege boundary. The future principal, wrapper/authorization adjustment, migrations, rollback, and hostile privilege tests remain implementation work and require their own authority and review.

### MUNE-EDGE-003: signature and key lifecycle underspecified

**CLOSED.** V2 fixes HMAC-SHA-256 with no algorithm negotiation; exact method/path/timestamp/actor/key/operation/body-hash canonical bytes; strict lowercase-hex signature encoding; constant-time comparison; ±300-second skew; actor-specific keys; bounded ACTIVE/RETIRING overlap; immediate REVOKED failure; and explicit secret exclusion from repository/log/receipt/error surfaces.

The database operation-ID/request-digest contract remains authoritative for semantic replay.

### MUNE-EDGE-004: zero-paid invocation abuse

**CLOSED AT DESIGN LEVEL.** V2 explicitly acknowledges that rejected Edge invocations can consume quota and therefore refuses to treat in-function rejection as a zero-cost boundary. Deployment is forbidden unless a no-additional-cost pre-invocation restriction/upstream boundary or a verified included-quota/worst-case model with paid overage disabled proves the zero-paid envelope. The deployment receipt must bind current quota/budget/control evidence, with administrative disable at the 80% Edge budget or hourly rejection threshold.

If that evidence cannot be produced, the controlling deployment verdict is `DO NOT DEPLOY`.

## Adversarial result

No remaining design contradiction was found against the four original Mune findings. PostgreSQL remains canonical authority; Edge remains a transport adapter only; actor scope is fail-closed; broad service privilege is rejected; cryptographic transport semantics are closed; and the zero-paid claim is converted from an assumption into a deployment gate.

## Approval boundary

`APPROVED_DESIGN_KEEP_AND_DEFER` means:

- retain the architecture as a future option;
- no Edge deployment is presently justified;
- no credential, hosted database privilege change, Edge deployment, paid overage, or production mutation is authorized;
- a future implementation candidate must still prove the dedicated DB principal, repository-first privilege package/rollback, exact actor authorization records, HMAC key lifecycle, hostile tests, current plan/quota evidence, and platform-level disable procedure.

Mune's independent Edge V2 rereview is complete for exact head `d65bcb2f6eb02ae2f9ce75646dc578967fe55c14`.