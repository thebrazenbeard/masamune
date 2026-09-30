import type { Finding, LaneReport } from "./types.ts";

export type EvidenceQuality =
  | "EXACT_FILE_LINE"
  | "EXACT_FILE"
  | "CONTEXT_ONLY"
  | "MODEL_ASSERTION";

export interface EvidenceReceipt {
  finding_id: string;
  lane: "MASA" | "MUNE";
  quality: EvidenceQuality;
  file: string | null;
  line: number | null;
  source_sha256: string | null;
  context_sha256: string;
  rationale: string;
}

function normal(path: string): string {
  return path.replaceAll("\\", "/").trim();
}

interface Section {
  path: string;
  content: string;
}

function sections(context: string): Section[] {
  const header = /^=== (?:HEAD SOURCE|SOURCE|DIFF) (.+?) ===$/gm;
  const matches = [...context.matchAll(header)];
  return matches.map((match, index) => {
    const start = (match.index ?? 0) + match[0].length;
    const end = index + 1 < matches.length
      ? (matches[index + 1].index ?? context.length)
      : context.length;
    return {
      path: normal(match[1]),
      content: context.slice(start, end).trim(),
    };
  });
}

export async function auditFinding(
  finding: Finding,
  lane: "MASA" | "MUNE",
  context: string,
): Promise<EvidenceReceipt> {
  const contextBytes = new TextEncoder().encode(context);
  const contextDigest = new Uint8Array(
    await crypto.subtle.digest("SHA-256", contextBytes),
  );
  const contextSha256 = Array.from(
    contextDigest,
    (byte) => byte.toString(16).padStart(2, "0"),
  ).join("");
  const path = finding.file ? normal(finding.file) : null;
  const section = path
    ? sections(context).find((item) => item.path === path)
    : null;

  if (path && section) {
    const sourceBytes = new TextEncoder().encode(section.content);
    const sourceDigest = new Uint8Array(
      await crypto.subtle.digest("SHA-256", sourceBytes),
    );
    const sourceSha256 = Array.from(
      sourceDigest,
      (byte) => byte.toString(16).padStart(2, "0"),
    ).join("");
    const truncated =
      section.content.includes("[MASAMUNE FILE/PATCH TRUNCATED]") ||
      section.content.includes("[MASAMUNE CONTEXT TRUNCATED");
    if (finding.line && !truncated) {
      const lineCount = section.content.split(/\r?\n/).length;
      if (finding.line <= lineCount) {
        return {
          finding_id: finding.id,
          lane,
          quality: "EXACT_FILE_LINE",
          file: path,
          line: finding.line,
          source_sha256: sourceSha256,
          context_sha256: contextSha256,
          rationale:
            "Cited file and line are present in an untruncated bounded context section.",
        };
      }
    }
    return {
      finding_id: finding.id,
      lane,
      quality: "EXACT_FILE",
      file: path,
      line: finding.line ?? null,
      source_sha256: sourceSha256,
      context_sha256: contextSha256,
      rationale:
        "Cited file is present in bounded context, but the exact line cannot be established from the supplied section.",
    };
  }

  if (
    finding.evidence.some((item) => item.length > 0 && context.includes(item))
  ) {
    return {
      finding_id: finding.id,
      lane,
      quality: "CONTEXT_ONLY",
      file: path,
      line: finding.line ?? null,
      source_sha256: null,
      context_sha256: contextSha256,
      rationale:
        "Evidence text occurs directly in bounded context without an exact file anchor.",
    };
  }

  return {
    finding_id: finding.id,
    lane,
    quality: "MODEL_ASSERTION",
    file: path,
    line: finding.line ?? null,
    source_sha256: null,
    context_sha256: contextSha256,
    rationale:
      "No deterministic source anchor or exact context evidence was established.",
  };
}

export async function auditReports(
  masa: LaneReport,
  mune: LaneReport,
  context: string,
): Promise<EvidenceReceipt[]> {
  const receipts: EvidenceReceipt[] = [];
  for (const finding of masa.findings) {
    receipts.push(await auditFinding(finding, "MASA", context));
  }
  for (const finding of mune.findings) {
    receipts.push(await auditFinding(finding, "MUNE", context));
  }
  return receipts;
}