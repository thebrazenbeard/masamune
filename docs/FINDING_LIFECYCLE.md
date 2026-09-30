# Finding Lifecycle

Masamune findings move through an explicit state machine. The state describes
what Masamune has established about a claim, not how confident a model sounds.

```text
PROPOSED
   |
   v
CHALLENGED
   |-----> REJECTED
   |
   +-----> UNRESOLVED
   |
   +-----> NARROWED
   |
   +-----> CONFIRMED
```

PROPOSED means a model generated the finding.

CHALLENGED means the finding has been presented to the adversarial challenge
lane. Challenge evidence is recorded separately from Masa's original evidence.

CONFIRMED requires all of the following in V0:

- the finding survives the challenge;
- Masa confidence is at least the configured threshold;
- Mune supplies concrete challenge evidence;
- deterministic evidence auditing finds an exact file anchor;
- the exact subject and bounded-context digest are recorded.

NARROWED means the underlying concern survives but the original wording was too
broad. The narrowed claim is stored rather than silently replacing the original
hypothesis.

UNRESOLVED means the evidence does not justify either confirmation or rejection.
Unresolved findings may be withheld from the public GitHub comment under
repository policy but remain part of the durable review receipt.

REJECTED means the challenge supplied a concrete contradiction or other reason
the finding does not hold for the reviewed subject.

## Evidence quality

The deterministic evidence auditor classifies each finding:

- EXACT_FILE_LINE — the cited file is in the bounded context and the cited line
  is inside an untruncated source section.
- EXACT_FILE — the cited file is in context, but the line cannot be established
  exactly from the bounded source.
- CONTEXT_ONLY — the finding has no exact file anchor but its evidence text is
  directly present in the bounded context.
- MODEL_ASSERTION — the claim exists only in model output.

Evidence quality is a claim ceiling. It is not a probability that the finding
is true.

## Why this matters

> A finding with a 0.95 model confidence score but no source anchor is still a
> model assertion. A 0.65 finding with an exact source anchor is easier to audit.

The system therefore separates model confidence from evidence quality rather than
multiplying the two into a fake precision score.

## No-clean-bill rule

A review containing zero promoted findings must still identify its scope and
state:

> Absence of a finding is not evidence of absence.

That sentence is a product invariant, not marketing copy.