import type {
  Challenge,
  EvidenceReceipt,
  Finding,
  LaneReport,
  ReviewReport,
  Subject,
} from "./types.ts";

function copyFinding(finding: Finding): Finding {
  return {
    ...finding,
    evidence: [...finding.evidence],
  };
}

export function reconcile(
  subject: Subject,
  masa: LaneReport,
  mune: LaneReport,
  challenges: Challenge[],
  evidenceReceipts: EvidenceReceipt[] = [],
  scopeNote?: string,
): ReviewReport {
  const byId = new Map<string, Challenge>();
  for (const challenge of challenges) {
    if (!byId.has(challenge.finding_id)) {
      byId.set(challenge.finding_id, challenge);
    }
  }

  const confirmed: Finding[] = [];
  const narrowed: Finding[] = [];
  const unresolved: Finding[] = [];
  const rejectedIds: string[] = [];
  const receiptById = new Map(
    evidenceReceipts.map((receipt) => [receipt.finding_id, receipt]),
  );

  const masaIds = new Set(masa.findings.map((finding) => finding.id));

  for (const finding of masa.findings) {
    const challenge = byId.get(finding.id);
    if (!challenge) {
      unresolved.push(copyFinding(finding));
      continue;
    }

    if (challenge.verdict === "REJECT") {
      rejectedIds.push(finding.id);
      continue;
    }

    const receipt = receiptById.get(finding.id);
    if (!receipt) {
      unresolved.push(copyFinding(finding));
      continue;
    }

    if (challenge.verdict === "CONFIRM") {
      const exactAnchor = receipt.quality === "EXACT_FILE_LINE" ||
        receipt.quality === "EXACT_FILE";
      if (
        finding.confidence >= 0.65 && challenge.evidence.length > 0 &&
        exactAnchor
      ) {
        const promoted = copyFinding(finding);
        promoted.evidence.push(
          ...challenge.evidence.map((item) => `Mune verification: ${item}`),
        );
        confirmed.push(promoted);
      } else {
        unresolved.push(copyFinding(finding));
      }
      continue;
    }

    if (challenge.verdict === "NARROW") {
      if (
        receipt.quality === "MODEL_ASSERTION" || challenge.evidence.length === 0
      ) {
        unresolved.push(copyFinding(finding));
        continue;
      }
      const narrowedFinding = copyFinding(finding);
      if (challenge.narrowed_title) {
        narrowedFinding.title = challenge.narrowed_title;
      }
      narrowedFinding.confidence = Math.min(narrowedFinding.confidence, 0.85);
      narrowedFinding.evidence.push(
        ...challenge.evidence.map((item) => `Mune verification: ${item}`),
      );
      narrowed.push(narrowedFinding);
      continue;
    }

    unresolved.push(copyFinding(finding));
  }

  // Blind-only Mune findings have not survived an additional independent
  // challenge, so preserve them as unresolved rather than promoting them.
  for (const finding of mune.findings) {
    if (!masaIds.has(finding.id) && finding.confidence >= 0.60) {
      unresolved.push(copyFinding(finding));
    }
  }

  return {
    subject,
    masa,
    mune: { ...mune, challenges },
    confirmed,
    narrowed,
    unresolved,
    rejected_ids: rejectedIds,
    evidence_receipts: evidenceReceipts,
    scope_note: scopeNote ?? null,
  };
}
