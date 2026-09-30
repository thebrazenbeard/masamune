import { GitHubAppClient } from "./github.ts";
import type { RepoPolicy, ReviewContext, Subject } from "./types.ts";

const CODE_EXTENSIONS = [
  ".py",
  ".pyi",
  ".js",
  ".jsx",
  ".ts",
  ".tsx",
  ".go",
  ".rs",
  ".java",
  ".kt",
  ".kts",
  ".rb",
  ".php",
  ".cs",
  ".cpp",
  ".cc",
  ".c",
  ".h",
  ".hpp",
  ".sql",
  ".sh",
  ".ps1",
  ".yaml",
  ".yml",
  ".toml",
  ".json",
];

const RISK_WORDS = [
  "auth",
  "security",
  "permission",
  "payment",
  "billing",
  "retry",
  "queue",
  "cache",
  "state",
  "migration",
  "database",
  "db",
  "session",
  "token",
  "worker",
  "api",
  "webhook",
  "transaction",
  "lock",
  "concurrent",
  "config",
];

const SECRET_PATTERNS: RegExp[] = [
  /-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----/g,
  /\bgh[pousr]_[A-Za-z0-9]{20,}\b/g,
  /\bgithub_pat_[A-Za-z0-9_]{20,}\b/g,
  /\bAKIA[0-9A-Z]{16}\b/g,
  /\b(api[_-]?key|access[_-]?token|secret|password)\b(\s*[:=]\s*)["']?[A-Za-z0-9_./+=-]{12,}["']?/gi,
];

function redact(text: string): string {
  let result = text;
  for (const pattern of SECRET_PATTERNS) {
    result = result.replace(pattern, "[REDACTED_POTENTIAL_SECRET]");
  }
  return result;
}

function utf8Bytes(text: string): Uint8Array {
  return new TextEncoder().encode(text);
}

function bounded(text: string, maxBytes: number): string {
  const safe = redact(text);
  const bytes = utf8Bytes(safe);
  if (bytes.length <= maxBytes) return safe;
  return new TextDecoder().decode(bytes.slice(0, maxBytes)) +
    "\n[MASAMUNE FILE/PATCH TRUNCATED]";
}

function trimParts(parts: string[], maxBytes: number): string {
  const output: string[] = [];
  let used = 0;
  for (const part of parts) {
    const safe = redact(part);
    const bytes = utf8Bytes(safe);
    if (used + bytes.length > maxBytes) {
      const remaining = maxBytes - used;
      if (remaining > 0) {
        output.push(new TextDecoder().decode(bytes.slice(0, remaining)));
        output.push("\n[MASAMUNE CONTEXT TRUNCATED AT POLICY BYTE LIMIT]");
      }
      break;
    }
    output.push(safe);
    used += bytes.length;
  }
  return output.join("\n");
}

function isCodePath(path: string): boolean {
  const lower = path.toLowerCase().replaceAll("\\", "/");
  const segments = new Set(lower.split("/"));
  if (
    [...segments].some((segment) =>
      ["vendor", "node_modules", "dist", "build"].includes(segment)
    )
  ) return false;
  return CODE_EXTENSIONS.some((extension) => lower.endsWith(extension));
}

function diversify(paths: string[], limit: number): string[] {
  const buckets = new Map<string, string[]>();
  for (const path of paths) {
    const root = path.includes("/") ? path.slice(0, path.indexOf("/")) : path;
    const bucket = buckets.get(root) ?? [];
    bucket.push(path);
    buckets.set(root, bucket);
  }
  const chosen: string[] = [];
  while (chosen.length < limit && buckets.size > 0) {
    for (const root of [...buckets.keys()].sort()) {
      const bucket = buckets.get(root);
      if (!bucket?.length) {
        buckets.delete(root);
        continue;
      }
      chosen.push(bucket.shift()!);
      if (!bucket.length) buckets.delete(root);
      if (chosen.length >= limit) break;
    }
  }
  return chosen;
}

function selectIssuePaths(
  paths: string[],
  issueText: string,
  limit: number,
): string[] {
  const terms = new Set(
    (issueText.toLowerCase().match(/[a-z][a-z0-9_-]{2,}/g) ?? [])
      .filter((token) => token.length >= 4),
  );
  const scored = paths
    .filter(isCodePath)
    .map((path) => {
      const lower = path.toLowerCase();
      let score = 0;
      for (const term of terms) if (lower.includes(term)) score += 3;
      for (const risk of RISK_WORDS) if (lower.includes(risk)) score += 1;
      return { path, score };
    })
    .sort((a, b) => b.score - a.score || a.path.localeCompare(b.path))
    .map(({ path }) => path);
  return diversify(scored, limit);
}

function selectSweepPaths(paths: string[], limit: number): string[] {
  const scored = paths
    .filter(isCodePath)
    .map((path) => {
      const lower = path.toLowerCase();
      let score = RISK_WORDS.reduce(
        (sum, risk) => sum + (lower.includes(risk) ? 2 : 0),
        0,
      );
      if (!lower.includes("/test") && !lower.includes("spec")) score += 1;
      return { path, score };
    })
    .sort((a, b) => b.score - a.score || a.path.localeCompare(b.path))
    .map(({ path }) => path);
  return diversify(scored, limit);
}

export async function buildPrContext(
  gh: GitHubAppClient,
  repository: string,
  number: number,
  policy: RepoPolicy,
): Promise<ReviewContext> {
  const pr = await gh.pull(repository, number);
  const headSha = String(pr.head.sha);
  const baseSha = String(pr.base.sha);
  const subject: Subject = {
    repository,
    kind: "PULL_REQUEST",
    number,
    head_sha: headSha,
    base_sha: baseSha,
    title: String(pr.title ?? `PR #${number}`),
    url: String(pr.html_url),
  };

  const files = await gh.pullFiles(repository, number);
  const candidates = files
    .filter((item) => isCodePath(String(item.filename)))
    .sort((a, b) =>
      Number(b.changes ?? 0) - Number(a.changes ?? 0) ||
      String(a.filename).localeCompare(String(b.filename))
    )
    .slice(0, policy.max_files);

  const parts: string[] = [
    `SUBJECT: pull request #${number}`,
    `REPOSITORY: ${repository}`,
    `BASE_SHA: ${baseSha}`,
    `HEAD_SHA: ${headSha}`,
    `TITLE: ${String(pr.title ?? "")}`,
    `BODY:\n${String(pr.body ?? "")}`,
    "\nCHANGED FILES:",
  ];

  for (const item of candidates) {
    const path = String(item.filename);
    const patch = bounded(
      String(item.patch ?? "[patch unavailable]"),
      policy.max_file_bytes,
    );
    parts.push(
      `\n=== DIFF ${path} ===\nstatus=${String(item.status ?? "")} additions=${
        Number(item.additions ?? 0)
      } deletions=${Number(item.deletions ?? 0)}\n${patch}`,
    );
    const source = await gh.fileText(repository, path, headSha);
    if (source !== null) {
      parts.push(
        `\n=== HEAD SOURCE ${path} ===\n${
          bounded(source, policy.max_file_bytes)
        }`,
      );
    }
  }

  return {
    subject,
    text: trimParts(parts, policy.max_context_bytes),
    policy,
  };
}

export async function buildIssueContext(
  gh: GitHubAppClient,
  repository: string,
  number: number,
  policy: RepoPolicy,
): Promise<ReviewContext> {
  const issue = await gh.issue(repository, number);
  const { commitSha, treeSha } = await gh.defaultHead(repository);
  const body = String(issue.body ?? "");
  const subject: Subject = {
    repository,
    kind: "ISSUE",
    number,
    head_sha: commitSha,
    title: String(issue.title ?? `Issue #${number}`),
    url: String(issue.html_url),
  };

  const paths = await gh.treePaths(repository, treeSha);
  const chosen = selectIssuePaths(
    paths,
    `${String(issue.title ?? "")}\n${body}`,
    policy.max_files,
  );
  const parts: string[] = [
    `SUBJECT: issue #${number}`,
    `REPOSITORY: ${repository}`,
    `HEAD_SHA: ${commitSha}`,
    `TITLE: ${String(issue.title ?? "")}`,
    `ISSUE BODY:\n${body}`,
    "\nSELECTED REPOSITORY CONTEXT:",
  ];

  for (const path of chosen) {
    const source = await gh.fileText(repository, path, commitSha);
    if (source !== null) {
      parts.push(
        `\n=== SOURCE ${path} ===\n${bounded(source, policy.max_file_bytes)}`,
      );
    }
  }

  return {
    subject,
    text: trimParts(parts, policy.max_context_bytes),
    policy,
  };
}

export async function buildSweepContext(
  gh: GitHubAppClient,
  repository: string,
  policy: RepoPolicy,
): Promise<ReviewContext> {
  const { commitSha, treeSha } = await gh.defaultHead(repository);
  const subject: Subject = {
    repository,
    kind: "SWEEP",
    head_sha: commitSha,
    title: "Repository defect discovery sweep",
    url: `https://github.com/${repository}`,
  };
  const paths = await gh.treePaths(repository, treeSha);
  const chosen = selectSweepPaths(paths, policy.max_files);
  const parts: string[] = [
    "SUBJECT: repository-wide bounded defect discovery sweep",
    `REPOSITORY: ${repository}`,
    `HEAD_SHA: ${commitSha}`,
    "Only selected files below are in scope. Absence of a finding is not proof that the repository is defect-free.",
  ];

  for (const path of chosen) {
    const source = await gh.fileText(repository, path, commitSha);
    if (source !== null) {
      parts.push(
        `\n=== SOURCE ${path} ===\n${bounded(source, policy.max_file_bytes)}`,
      );
    }
  }

  return {
    subject,
    text: trimParts(parts, policy.max_context_bytes),
    policy,
  };
}
