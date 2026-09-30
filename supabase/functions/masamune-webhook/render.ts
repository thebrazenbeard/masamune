import type { Finding, ReviewReport } from "./types.ts";

function safeMarkdown(text: string): string {
  return text.replaceAll("<!--", "&lt;!--").replaceAll("@", "@\u200b");
}

function findingBlock(finding: Finding): string {
  let where = "";
  if (finding.file) {
    const path = safeMarkdown(finding.file).replaceAll("`", "");
    where = ` — \`${path}${finding.line ? `:${finding.line}` : ""}\``;
  }
  const evidence = finding.evidence
    .slice(0, 5)
    .map((item) => `- ${safeMarkdown(item)}`)
    .join("\n");
  const suggestion = finding.suggestion
    ? `\n**Suggestion:** ${safeMarkdown(finding.suggestion)}\n`
    : "";
  return [
    `### ${finding.severity} · ${finding.kind}`,
    `**${safeMarkdown(finding.title)}**${where}`,
    "",
    safeMarkdown(finding.mechanism),
    "",
    "**Evidence:**",
    evidence || "- No specific evidence supplied.",
    suggestion,
  ].join("\n");
}

export function renderReport(
  report: ReviewReport,
  reviewId: string,
  includeUnresolved: boolean,
): string {
  const subject = report.subject;
  const marker = `<!-- masamune-review:${reviewId} -->`;
  const lines: string[] = [
    marker,
    "## ⚔️ Masamune adversarial review",
    "",
    `**Exact subject:** \`${subject.repository}@${subject.head_sha}\``,
    `**Mode:** ${subject.kind}`,
    `**Masa:** \`${report.masa.provider_id}/${report.masa.model_id}\``,
    `**Mune:** \`${report.mune.provider_id}/${report.mune.model_id}\``,
    "",
  ];

  const skepticFlags = report.skeptic_flags ?? [];
  if (skepticFlags.length) {
    lines.push("## Skeptic gate", "");
    for (const flag of skepticFlags) {
      lines.push("- `" + safeMarkdown(flag) + "`");
    }
    lines.push("");
  }

  if (report.confirmed.length) {
    lines.push("## Confirmed by Mune", "");
    for (const finding of report.confirmed) {
      lines.push(findingBlock(finding), "");
    }
  }

  if (report.narrowed.length) {
    lines.push("## Survives, narrowed", "");
    for (const finding of report.narrowed) {
      lines.push(findingBlock(finding), "");
    }
  }

  if (report.unresolved.length && includeUnresolved) {
    lines.push("## Unresolved / needs validation", "");
    for (const finding of report.unresolved.slice(0, 12)) {
      lines.push(findingBlock(finding), "");
    }
  } else if (report.unresolved.length) {
    lines.push(
      `_Policy withheld ${report.unresolved.length} unresolved hypothesis/hypotheses._`,
      "",
    );
  }

  if (
    report.confirmed.length === 0 &&
    report.narrowed.length === 0 &&
    report.unresolved.length === 0
  ) {
    lines.push(
      "No reportable finding survived this bounded review.",
      "",
      "That is **not** proof that the subject is defect-free.",
      "",
    );
  }

  if (report.rejected_ids.length) {
    lines.push(
      "<details>",
      "<summary>Rejected Masa hypotheses</summary>",
      "",
      report.rejected_ids.map((id) => `\`${id}\``).join(", "),
      "",
      "</details>",
      "",
    );
  }

  lines.push(
    "---",
    report.scope_note ??
      "Masamune reviewed only the evidence included in this exact run. Model agreement is not independent factual evidence.",
  );

  return lines.join("\n");
}
