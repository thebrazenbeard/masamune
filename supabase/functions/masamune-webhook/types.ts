export type SubjectKind = "PULL_REQUEST" | "ISSUE" | "SWEEP";

export type Severity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export type FindingKind =
  | "BUG"
  | "REGRESSION_RISK"
  | "SECURITY_CONCERN"
  | "DESIGN_WEAKNESS"
  | "TESTING_GAP"
  | "PERFORMANCE_OPPORTUNITY"
  | "MAINTAINABILITY_IMPROVEMENT"
  | "SPECULATIVE_NEEDS_VALIDATION";

export interface Finding {
  id: string;
  title: string;
  kind: FindingKind;
  severity: Severity;
  confidence: number;
  file?: string | null;
  line?: number | null;
  evidence: string[];
  mechanism: string;
  suggestion?: string | null;
}

export interface Challenge {
  finding_id: string;
  verdict: "CONFIRM" | "REJECT" | "NARROW" | "UNRESOLVED";
  rationale: string;
  evidence: string[];
  narrowed_title?: string | null;
}

export interface LaneReport {
  lane: "MASA" | "MUNE";
  provider_id: string;
  model_id: string;
  findings: Finding[];
  challenges: Challenge[];
  notes: string[];
}

export interface Subject {
  repository: string;
  kind: SubjectKind;
  number?: number | null;
  head_sha: string;
  base_sha?: string | null;
  title: string;
  url: string;
}

export interface ReviewReport {
  subject: Subject;
  masa: LaneReport;
  mune: LaneReport;
  confirmed: Finding[];
  narrowed: Finding[];
  unresolved: Finding[];
  rejected_ids: string[];
  evidence_receipts: EvidenceReceipt[];
  scope_note?: string | null;
}

export interface RepoPolicy {
  enabled: boolean;
  review_pull_requests: boolean;
  allow_external_pull_requests: boolean;
  allow_issue_commands: boolean;
  allow_sweep: boolean;
  post_unresolved: boolean;
  max_files: number;
  max_file_bytes: number;
  max_context_bytes: number;
}

export interface EvidenceReceipt {
  finding_id: string;
  lane: "MASA" | "MUNE";
  quality: "EXACT_FILE_LINE" | "EXACT_FILE" | "CONTEXT_ONLY" | "MODEL_ASSERTION";
  file: string | null;
  line: number | null;
  source_sha256: string | null;
  context_sha256: string;
  rationale: string;
}

export interface ReviewContext {
  subject: Subject;
  text: string;
  policy: RepoPolicy;
}

export const DEFAULT_POLICY: RepoPolicy = {
  enabled: true,
  review_pull_requests: true,
  allow_external_pull_requests: false,
  allow_issue_commands: true,
  allow_sweep: true,
  post_unresolved: false,
  max_files: 10,
  max_file_bytes: 8_000,
  max_context_bytes: 20_000,
};

export type Command =
  | { kind: "INVESTIGATE"; issueNumber: number | null }
  | { kind: "SWEEP"; issueNumber: null };

export function parseCommand(text: string): Command | null {
  const investigate = text.match(
    /^\s*\/masamune\s+investigate(?:\s+#?(\d+))?\s*$/im,
  );
  if (investigate) {
    return {
      kind: "INVESTIGATE",
      issueNumber: investigate[1] ? Number(investigate[1]) : null,
    };
  }
  if (/^\s*\/masamune\s+sweep\s*$/im.test(text)) {
    return { kind: "SWEEP", issueNumber: null };
  }
  return null;
}
