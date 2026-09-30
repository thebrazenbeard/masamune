export interface Settings {
  githubAppId: string;
  githubPrivateKey: string;
  githubWebhookSecret: string;
  githubApiUrl: string;

  masaBaseUrl: string;
  masaApiKey: string;
  masaProviderId: string;
  masaModel: string;

  muneBaseUrl: string;
  muneApiKey: string;
  muneProviderId: string;
  muneModel: string;

  requireIndependence: boolean;
  allowPrivateRepositories: boolean;
  maxFiles: number;
  maxFileBytes: number;
  maxContextBytes: number;
  modelMaxOutputTokens: number;
  masaTemperature: number;
  muneTemperature: number;
  requestTimeoutMs: number;
  maxWebhookBytes: number;
  globalReviewsPerDay: number;
  repoReviewsPerDay: number;
  reviewProtocolVersion: string;
  zeroCostEnforced: boolean;
}

function env(name: string, fallback = ""): string {
  return Deno.env.get(name) ?? fallback;
}

function boolEnv(name: string, fallback: boolean): boolean {
  const value = Deno.env.get(name);
  if (value === undefined) return fallback;
  if (value === "true") return true;
  if (value === "false") return false;
  throw new Error(`${name} must be true or false`);
}

function floatEnv(
  name: string,
  fallback: number,
  min: number,
  max: number,
): number {
  const raw = Deno.env.get(name);
  const value = raw === undefined ? fallback : Number(raw);
  if (!Number.isFinite(value) || value < min || value > max) {
    throw new Error(
      name + " must be a number between " + min + " and " + max,
    );
  }
  return value;
}

function intEnv(
  name: string,
  fallback: number,
  min: number,
  max: number,
): number {
  const raw = Deno.env.get(name);
  const value = raw === undefined ? fallback : Number(raw);
  if (!Number.isInteger(value) || value < min || value > max) {
    throw new Error(`${name} must be an integer between ${min} and ${max}`);
  }
  return value;
}

export function loadSettings(): Settings {
  const settings: Settings = {
    githubAppId: env("MASAMUNE_GITHUB_APP_ID"),
    githubPrivateKey: env("MASAMUNE_GITHUB_PRIVATE_KEY"),
    githubWebhookSecret: env("MASAMUNE_GITHUB_WEBHOOK_SECRET"),
    githubApiUrl: env("MASAMUNE_GITHUB_API_URL", "https://api.github.com"),

    // Zero-cost default: one Groq free-tier call for Masa.
    masaBaseUrl: env(
      "MASAMUNE_MASA_BASE_URL",
      "https://api.groq.com/openai/v1",
    ),
    masaApiKey: env("MASAMUNE_MASA_API_KEY"),
    masaProviderId: env("MASAMUNE_MASA_PROVIDER_ID", "groq"),
    masaModel: env("MASAMUNE_MASA_MODEL", "qwen/qwen3.8-27b"),

    // Zero-cost default: Gemini free tier for Mune blind + challenge passes.
    muneBaseUrl: env(
      "MASAMUNE_MUNE_BASE_URL",
      "https://generativelanguage.googleapis.com/v1beta/openai",
    ),
    muneApiKey: env("MASAMUNE_MUNE_API_KEY"),
    muneProviderId: env("MASAMUNE_MUNE_PROVIDER_ID", "google"),
    muneModel: env("MASAMUNE_MUNE_MODEL", "gemini-3.8-flash"),

    requireIndependence: boolEnv("MASAMUNE_REQUIRE_INDEPENDENCE", true),
    allowPrivateRepositories: boolEnv(
      "MASAMUNE_ALLOW_PRIVATE_REPOSITORIES",
      false,
    ),
    maxFiles: intEnv("MASAMUNE_MAX_FILES", 10, 1, 200),
    maxFileBytes: intEnv("MASAMUNE_MAX_FILE_BYTES", 8_000, 2_000, 200_000),
    maxContextBytes: intEnv(
      "MASAMUNE_MAX_CONTEXT_BYTES",
      20_000,
      10_000,
      1_000_000,
    ),
    modelMaxOutputTokens: intEnv(
      "MASAMUNE_MODEL_MAX_OUTPUT_TOKENS",
      2_000,
      500,
      20_000,
    ),
    masaTemperature: floatEnv("MASAMUNE_MASA_TEMPERATURE", 0, 0, 2),
    muneTemperature: floatEnv("MASAMUNE_MUNE_TEMPERATURE", 1, 0, 2),
    requestTimeoutMs: intEnv(
      "MASAMUNE_REQUEST_TIMEOUT_MS",
      45_000,
      5_000,
      120_000,
    ),
    maxWebhookBytes: intEnv(
      "MASAMUNE_MAX_WEBHOOK_BYTES",
      2_000_000,
      1_024,
      20_000_000,
    ),
    globalReviewsPerDay: intEnv(
      "MASAMUNE_GLOBAL_REVIEWS_PER_DAY",
      10,
      1,
      1_000,
    ),
    repoReviewsPerDay: intEnv("MASAMUNE_REPO_REVIEWS_PER_DAY", 3, 1, 100),
    reviewProtocolVersion: env(
      "MASAMUNE_REVIEW_PROTOCOL_VERSION",
      "masamune-edge-v0.1",
    ),
    zeroCostEnforced: boolEnv("MASAMUNE_ZERO_COST_ENFORCED", true),
  };

  for (
    const [name, value] of [
      ["MASAMUNE_GITHUB_APP_ID", settings.githubAppId],
      ["MASAMUNE_GITHUB_PRIVATE_KEY", settings.githubPrivateKey],
      ["MASAMUNE_GITHUB_WEBHOOK_SECRET", settings.githubWebhookSecret],
      ["MASAMUNE_MASA_API_KEY", settings.masaApiKey],
      ["MASAMUNE_MUNE_API_KEY", settings.muneApiKey],
    ] as const
  ) {
    if (!value) throw new Error(`missing required secret/config: ${name}`);
  }

  if (
    settings.requireIndependence &&
    (
      settings.masaProviderId === settings.muneProviderId ||
      settings.masaModel === settings.muneModel
    )
  ) {
    throw new Error(
      "Masa and Mune must use distinct providers and distinct models when independence is required",
    );
  }

  validateBillingPolicy(settings);
  return settings;
}

export function missingRuntimeSecretsFromEnv(): string[] {
  const names = [
    "MASAMUNE_GITHUB_APP_ID",
    "MASAMUNE_GITHUB_PRIVATE_KEY",
    "MASAMUNE_GITHUB_WEBHOOK_SECRET",
    "MASAMUNE_MASA_API_KEY",
    "MASAMUNE_MUNE_API_KEY",
  ];
  return names.filter((name) => !(Deno.env.get(name) ?? "").trim());
}

export function missingRuntimeSecrets(
  settings: Pick<
    Settings,
    | "githubAppId"
    | "githubPrivateKey"
    | "githubWebhookSecret"
    | "masaApiKey"
    | "muneApiKey"
  >,
): string[] {
  const required: Array<[string, string]> = [
    ["MASAMUNE_GITHUB_APP_ID", settings.githubAppId],
    ["MASAMUNE_GITHUB_PRIVATE_KEY", settings.githubPrivateKey],
    ["MASAMUNE_GITHUB_WEBHOOK_SECRET", settings.githubWebhookSecret],
    ["MASAMUNE_MASA_API_KEY", settings.masaApiKey],
    ["MASAMUNE_MUNE_API_KEY", settings.muneApiKey],
  ];
  return required.filter(([, value]) => !value.trim()).map(([name]) => name);
}

export function validateBillingPolicy(
  settings: Pick<
    Settings,
    | "zeroCostEnforced"
    | "masaProviderId"
    | "masaBaseUrl"
    | "masaModel"
    | "muneProviderId"
    | "muneBaseUrl"
    | "muneModel"
    | "allowPrivateRepositories"
  >,
): void {
  if (!settings.zeroCostEnforced) return;

  const freeDefaults = [
    settings.masaProviderId === "groq",
    settings.masaBaseUrl === "https://api.groq.com/openai/v1",
    settings.masaModel === "qwen/qwen3.8-27b",
    settings.muneProviderId === "google",
    settings.muneBaseUrl ===
      "https://generativelanguage.googleapis.com/v1beta/openai",
    settings.muneModel === "gemini-3.8-flash",
    settings.allowPrivateRepositories === false,
  ];
  if (freeDefaults.some((ok) => !ok)) {
    throw new Error(
      "zero-cost enforcement rejects non-free provider/model configuration",
    );
  }
}
