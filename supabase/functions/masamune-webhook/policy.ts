import { parse } from "@std/yaml";
import { DEFAULT_POLICY, type RepoPolicy } from "./types.ts";

const POLICY_KEYS = new Set<keyof RepoPolicy>([
  "enabled",
  "review_pull_requests",
  "allow_external_pull_requests",
  "allow_issue_commands",
  "allow_sweep",
  "post_unresolved",
  "max_files",
  "max_file_bytes",
  "max_context_bytes",
]);

function requireBoolean(value: unknown, name: string): boolean {
  if (typeof value !== "boolean") throw new Error(`${name} must be boolean`);
  return value;
}

function requireInt(
  value: unknown,
  name: string,
  min: number,
  max: number,
): number {
  if (!Number.isInteger(value) || Number(value) < min || Number(value) > max) {
    throw new Error(`${name} must be an integer between ${min} and ${max}`);
  }
  return Number(value);
}

export function loadPolicy(text: string | null): RepoPolicy {
  if (!text?.trim()) return { ...DEFAULT_POLICY };
  const raw = parse(text);
  if (raw === null || typeof raw !== "object" || Array.isArray(raw)) {
    throw new Error(".masamune.yml must contain a mapping");
  }
  const root = raw as Record<string, unknown>;
  const candidate = root.masamune ?? root;
  if (
    candidate === null || typeof candidate !== "object" ||
    Array.isArray(candidate)
  ) {
    throw new Error("masamune policy must contain a mapping");
  }
  const cfg = candidate as Record<string, unknown>;
  for (const key of Object.keys(cfg)) {
    if (!POLICY_KEYS.has(key as keyof RepoPolicy)) {
      throw new Error(`unknown Masamune policy key: ${key}`);
    }
  }

  const policy: RepoPolicy = { ...DEFAULT_POLICY };
  if ("enabled" in cfg) policy.enabled = requireBoolean(cfg.enabled, "enabled");
  if ("review_pull_requests" in cfg) {
    policy.review_pull_requests = requireBoolean(
      cfg.review_pull_requests,
      "review_pull_requests",
    );
  }
  if ("allow_external_pull_requests" in cfg) {
    policy.allow_external_pull_requests = requireBoolean(
      cfg.allow_external_pull_requests,
      "allow_external_pull_requests",
    );
  }
  if ("allow_issue_commands" in cfg) {
    policy.allow_issue_commands = requireBoolean(
      cfg.allow_issue_commands,
      "allow_issue_commands",
    );
  }
  if ("allow_sweep" in cfg) {
    policy.allow_sweep = requireBoolean(cfg.allow_sweep, "allow_sweep");
  }
  if ("post_unresolved" in cfg) {
    policy.post_unresolved = requireBoolean(
      cfg.post_unresolved,
      "post_unresolved",
    );
  }
  if ("max_files" in cfg) {
    policy.max_files = requireInt(cfg.max_files, "max_files", 1, 200);
  }
  if ("max_file_bytes" in cfg) {
    policy.max_file_bytes = requireInt(
      cfg.max_file_bytes,
      "max_file_bytes",
      2_000,
      200_000,
    );
  }
  if ("max_context_bytes" in cfg) {
    policy.max_context_bytes = requireInt(
      cfg.max_context_bytes,
      "max_context_bytes",
      10_000,
      1_000_000,
    );
  }
  return policy;
}

export function applyOperatorCaps(
  policy: RepoPolicy,
  caps: Pick<RepoPolicy, "max_files" | "max_file_bytes" | "max_context_bytes">,
): RepoPolicy {
  return {
    ...policy,
    max_files: Math.min(policy.max_files, caps.max_files),
    max_file_bytes: Math.min(policy.max_file_bytes, caps.max_file_bytes),
    max_context_bytes: Math.min(
      policy.max_context_bytes,
      caps.max_context_bytes,
    ),
  };
}
