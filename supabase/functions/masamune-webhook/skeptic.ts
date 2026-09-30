import type { Challenge, EvidenceReceipt, LaneReport } from "./types.ts";

export function skepticFlags(
  masa: LaneReport,
  mune: LaneReport,
  challenges: Challenge[],
  receipts: EvidenceReceipt[],
): string[] {
  const flags: string[] = [];
  const masaIds = new Set(masa.findings.map((finding) => finding.id));
  const muneIds = new Set(mune.findings.map((finding) => finding.id));
  for (const id of masaIds) {
    if (muneIds.has(id)) flags.push("CROSS_LANE_FINDING_ID_COLLISION");
  }

  const challengedIds = new Set(
    challenges.map((challenge) => challenge.finding_id),
  );
  const missing = [...masaIds].filter((id) => !challengedIds.has(id)).sort();
  if (missing.length) {
    flags.push(`CHALLENGE_COVERAGE_GAP:${missing.slice(0, 10).join(",")}`);
  }
  const extra = [...challengedIds].filter((id) => !masaIds.has(id)).sort();
  if (extra.length) {
    flags.push(
      `CHALLENGE_FOR_UNKNOWN_FINDING:${extra.slice(0, 10).join(",")}`,
    );
  }

  const receiptById = new Map(
    receipts.map((receipt) => [receipt.finding_id, receipt]),
  );
  for (const finding of masa.findings) {
    const receipt = receiptById.get(finding.id);
    if (!receipt) {
      flags.push(`MISSING_EVIDENCE_RECEIPT:${finding.id}`);
    } else if (receipt.quality === "MODEL_ASSERTION") {
      flags.push(`MODEL_ONLY_EVIDENCE:${finding.id}`);
    } else if (
      (finding.severity === "HIGH" || finding.severity === "CRITICAL") &&
      receipt.quality === "CONTEXT_ONLY"
    ) {
      flags.push(`HIGH_SEVERITY_WEAK_ANCHOR:${finding.id}`);
    }
  }

  if (masa.provider_id === mune.provider_id) flags.push("SHARED_PROVIDER");
  if (masa.model_id === mune.model_id) flags.push("SHARED_MODEL");
  return flags;
}