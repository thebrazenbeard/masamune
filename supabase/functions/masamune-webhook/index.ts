import {
  loadSettings,
  missingRuntimeSecrets,
  missingRuntimeSecretsFromEnv,
  type Settings,
} from "./config.ts";
import {
  buildIssueContext,
  buildPrContext,
  buildSweepContext,
} from "./context.ts";
import { sha256Hex, verifyGithubSignature } from "./crypto.ts";
import { GitHubAppClient } from "./github.ts";
import { MasamuneOrchestrator, reviewIdFor } from "./orchestrator.ts";
import { applyOperatorCaps, loadPolicy } from "./policy.ts";
import { renderReport } from "./render.ts";
import { DeliveryStore } from "./store.ts";
import {
  parseCommand,
  type ReviewContext,
  type ReviewReport,
} from "./types.ts";

declare const EdgeRuntime: {
  waitUntil(promise: Promise<unknown>): void;
};

type JsonObject = Record<string, unknown>;

function asObject(value: unknown): JsonObject {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return value as JsonObject;
  }
  return {};
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function supabaseServerKey(): string {
  const modern = Deno.env.get("SUPABASE_SECRET_KEYS");
  if (modern) {
    try {
      const parsed = JSON.parse(modern);
      if (typeof parsed?.default === "string" && parsed.default) {
        return parsed.default;
      }
    } catch {
      // Fall through to legacy key.
    }
  }
  const legacy = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!legacy) throw new Error("missing Supabase server key");
  return legacy;
}

async function publishReview(
  gh: GitHubAppClient,
  store: DeliveryStore,
  deliveryId: string,
  context: ReviewContext,
  anchorIssue: number,
  orchestrator: MasamuneOrchestrator,
  settings: Settings,
): Promise<void> {
  const reviewId = await reviewIdFor(context, settings);
  const marker = "<!-- masamune-review:" + reviewId + " -->";

  if (
    await gh.hasCommentMarker(
      context.subject.repository,
      anchorIssue,
      marker,
    )
  ) {
    await store.mark(deliveryId, "COMPLETED");
    return;
  }

  const cachedReport = await store.getReview(reviewId);
  if (cachedReport) {
    const cachedBody = renderReport(
      cachedReport,
      reviewId,
      context.policy.post_unresolved,
    );
    await gh.comment(context.subject.repository, anchorIssue, cachedBody);
    if (
      !(await gh.hasCommentMarker(
        context.subject.repository,
        anchorIssue,
        marker,
      ))
    ) {
      throw new Error(
        "cached Masamune comment write did not verify by readback",
      );
    }
    await store.mark(deliveryId, "COMPLETED");
    return;
  }

  const leaseClaimed = await store.claimExecutionLease(reviewId);
  if (!leaseClaimed) {
    await store.mark(
      deliveryId,
      "FAILED",
      "zero-cost model execution lane is busy; retry after the active lease expires",
    );
    return;
  }

  let report: ReviewReport;
  try {
    const admitted = await store.claimReviewBudget(
      reviewId,
      context.subject.repository,
      settings.globalReviewsPerDay,
      settings.repoReviewsPerDay,
    );

    if (!admitted) {
      const day = new Date().toISOString().slice(0, 10);
      const budgetMarker = "<!-- masamune-zero-cost-budget:" + day + " -->";
      if (
        !(await gh.hasCommentMarker(
          context.subject.repository,
          anchorIssue,
          budgetMarker,
        ))
      ) {
        await gh.comment(
          context.subject.repository,
          anchorIssue,
          budgetMarker +
            "\nMasamune's zero-cost review allowance is exhausted for today. " +
            "No paid inference fallback is enabled; try again after the UTC daily reset.",
        );
      }
      await store.mark(deliveryId, "COMPLETED");
      return;
    }

    report = await orchestrator.review(context);
  } finally {
    try {
      await store.releaseExecutionLease(reviewId);
    } catch (error) {
      console.error("Masamune execution lease release failed", reviewId, error);
    }
  }

  const body = renderReport(
    report,
    reviewId,
    context.policy.post_unresolved,
  );

  await store.saveReview(reviewId, deliveryId, report);
  await store.mark(deliveryId, "READY_TO_PUBLISH");

  if (
    !(await gh.hasCommentMarker(
      context.subject.repository,
      anchorIssue,
      marker,
    ))
  ) {
    await gh.comment(context.subject.repository, anchorIssue, body);
  }

  if (
    !(await gh.hasCommentMarker(
      context.subject.repository,
      anchorIssue,
      marker,
    ))
  ) {
    throw new Error("Masamune comment write did not verify by readback");
  }

  await store.mark(deliveryId, "COMPLETED");
}

async function processDelivery(
  deliveryId: string,
  eventName: string,
  payload: JsonObject,
  settings: Settings,
  store: DeliveryStore,
): Promise<void> {
  try {
    const installation = asObject(payload.installation);
    const repositoryPayload = asObject(payload.repository);
    const sender = asObject(payload.sender);
    const installationId = Number(installation.id ?? 0);
    const repository = String(repositoryPayload.full_name ?? "");
    if (!installationId || !repository) {
      await store.mark(deliveryId, "IGNORED");
      return;
    }

    if (sender.type === "Bot") {
      await store.mark(deliveryId, "IGNORED");
      return;
    }

    const gh = new GitHubAppClient(
      {
        appId: settings.githubAppId,
        privateKey: settings.githubPrivateKey,
        apiUrl: settings.githubApiUrl,
        timeoutMs: settings.requestTimeoutMs,
      },
      installationId,
    );

    const repoMeta = await gh.repo(repository);
    if (Boolean(repoMeta.private) && !settings.allowPrivateRepositories) {
      await store.mark(deliveryId, "IGNORED");
      return;
    }

    const defaultRef = String(
      repositoryPayload.default_branch ??
        repoMeta.default_branch ??
        "main",
    );
    const policyText = await gh.fileText(
      repository,
      ".masamune.yml",
      defaultRef,
    );
    const policy = applyOperatorCaps(
      loadPolicy(policyText),
      {
        max_files: settings.maxFiles,
        max_file_bytes: settings.maxFileBytes,
        max_context_bytes: settings.maxContextBytes,
      },
    );

    if (!policy.enabled) {
      await store.mark(deliveryId, "IGNORED");
      return;
    }

    const orchestrator = new MasamuneOrchestrator(settings);

    if (eventName === "pull_request") {
      const action = String(payload.action ?? "");
      const allowedActions = new Set([
        "opened",
        "reopened",
        "synchronize",
        "ready_for_review",
      ]);
      if (!allowedActions.has(action) || !policy.review_pull_requests) {
        await store.mark(deliveryId, "IGNORED");
        return;
      }

      const pr = asObject(payload.pull_request);
      if (Boolean(pr.draft) && action !== "ready_for_review") {
        await store.mark(deliveryId, "IGNORED");
        return;
      }

      const trustedAssociations = new Set([
        "OWNER",
        "MEMBER",
        "COLLABORATOR",
      ]);
      if (
        !policy.allow_external_pull_requests &&
        !trustedAssociations.has(String(pr.author_association ?? ""))
      ) {
        await store.mark(deliveryId, "IGNORED");
        return;
      }

      const number = Number(payload.number);
      if (!Number.isInteger(number) || number < 1) {
        throw new Error("pull_request event missing valid number");
      }
      const context = await buildPrContext(
        gh,
        repository,
        number,
        policy,
      );
      await publishReview(
        gh,
        store,
        deliveryId,
        context,
        number,
        orchestrator,
        settings,
      );
      return;
    }

    if (
      eventName === "issue_comment" &&
      payload.action === "created" &&
      policy.allow_issue_commands
    ) {
      const comment = asObject(payload.comment);
      const command = parseCommand(String(comment.body ?? ""));
      if (!command) {
        await store.mark(deliveryId, "IGNORED");
        return;
      }

      const username = String(sender.login ?? "");
      if (!username) {
        await store.mark(deliveryId, "IGNORED");
        return;
      }
      const permission = await gh.collaboratorPermission(
        repository,
        username,
      );
      if (!new Set(["write", "maintain", "admin"]).has(permission)) {
        await store.mark(deliveryId, "IGNORED");
        return;
      }

      const issue = asObject(payload.issue);
      const anchorIssue = Number(issue.number);
      if (!Number.isInteger(anchorIssue) || anchorIssue < 1) {
        throw new Error("issue_comment event missing issue number");
      }

      let context: ReviewContext;
      if (command.kind === "INVESTIGATE") {
        const target = command.issueNumber ?? anchorIssue;
        context = await buildIssueContext(
          gh,
          repository,
          target,
          policy,
        );
      } else {
        if (!policy.allow_sweep) {
          await store.mark(deliveryId, "IGNORED");
          return;
        }
        context = await buildSweepContext(gh, repository, policy);
      }

      await publishReview(
        gh,
        store,
        deliveryId,
        context,
        anchorIssue,
        orchestrator,
        settings,
      );
      return;
    }

    if (
      eventName === "issues" &&
      payload.action === "labeled" &&
      policy.allow_issue_commands
    ) {
      const labelObject = asObject(payload.label);
      const label = String(labelObject.name ?? "").toLowerCase();
      if (label !== "masamune") {
        await store.mark(deliveryId, "IGNORED");
        return;
      }

      const username = String(sender.login ?? "");
      if (!username) {
        await store.mark(deliveryId, "IGNORED");
        return;
      }
      const permission = await gh.collaboratorPermission(
        repository,
        username,
      );
      if (!new Set(["write", "maintain", "admin"]).has(permission)) {
        await store.mark(deliveryId, "IGNORED");
        return;
      }

      const issue = asObject(payload.issue);
      const number = Number(issue.number);
      if (!Number.isInteger(number) || number < 1) {
        throw new Error("issues event missing issue number");
      }
      const context = await buildIssueContext(
        gh,
        repository,
        number,
        policy,
      );
      await publishReview(
        gh,
        store,
        deliveryId,
        context,
        number,
        orchestrator,
        settings,
      );
      return;
    }

    await store.mark(deliveryId, "IGNORED");
  } catch (error) {
    const message = error instanceof Error
      ? error.name + ": " + error.message
      : String(error);
    console.error("Masamune delivery failed", deliveryId, message);
    try {
      await store.mark(deliveryId, "FAILED", message);
    } catch (markError) {
      console.error("Masamune failed to persist failure state", markError);
    }
  }
}

Deno.serve(async (request: Request) => {
  if (request.method === "GET") {
    try {
      const missing = missingRuntimeSecretsFromEnv();
      if (configuredMissing.length) {
        const zeroCost = Deno.env.get("MASAMUNE_ZERO_COST_ENFORCED") !== "false";
        return jsonResponse(
          {
            status: "not_ready",
            service: "masamune",
            runtime: "supabase-edge",
            billing_mode: zeroCost ? "zero-cost-enforced" : "operator-configured",
            missing: configuredMissing,
          },
          503,
        );
      }
      const healthSettings = loadSettings();
      const configuredMissing = missingRuntimeSecrets(healthSettings);
      const billingMode = healthSettings.zeroCostEnforced
        ? "zero-cost-enforced"
        : "operator-configured";
      if (missing.length) {
        return jsonResponse(
          {
            status: "not_ready",
            service: "masamune",
            runtime: "supabase-edge",
            billing_mode: billingMode,
            missing,
          },
          503,
        );
      }
      return jsonResponse({
        status: "ok",
        service: "masamune",
        runtime: "supabase-edge",
        billing_mode: billingMode,
      });
    } catch {
      return jsonResponse(
        { status: "misconfigured", service: "masamune" },
        503,
      );
    }
  }

  if (request.method !== "POST") {
    return jsonResponse({ error: "method not allowed" }, 405);
  }

  let settings: Settings;
  try {
    settings = loadSettings();
  } catch (error) {
    console.error("Masamune configuration error", error);
    return jsonResponse({ error: "service not configured" }, 503);
  }

  const contentLength = Number(
    request.headers.get("content-length") ?? "0",
  );
  if (
    Number.isFinite(contentLength) &&
    contentLength > settings.maxWebhookBytes
  ) {
    return jsonResponse({ error: "webhook payload too large" }, 413);
  }

  const body = new Uint8Array(await request.arrayBuffer());
  if (body.byteLength > settings.maxWebhookBytes) {
    return jsonResponse({ error: "webhook payload too large" }, 413);
  }

  const validSignature = await verifyGithubSignature(
    settings.githubWebhookSecret,
    body,
    request.headers.get("x-hub-signature-256"),
  );
  if (!validSignature) {
    return jsonResponse({ error: "invalid webhook signature" }, 401);
  }

  const eventName = request.headers.get("x-github-event");
  const deliveryId = request.headers.get("x-github-delivery");
  if (!eventName || !deliveryId) {
    return jsonResponse({ error: "missing GitHub webhook headers" }, 400);
  }

  let payload: JsonObject;
  try {
    const parsed: unknown = JSON.parse(new TextDecoder().decode(body));
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return jsonResponse({ error: "invalid JSON payload" }, 400);
    }
    payload = parsed as JsonObject;
  } catch {
    return jsonResponse({ error: "invalid JSON payload" }, 400);
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  if (!supabaseUrl) {
    return jsonResponse({ error: "missing Supabase URL" }, 503);
  }
  const store = new DeliveryStore(
    supabaseUrl,
    supabaseServerKey(),
  );
  const digest = await sha256Hex(body);
  const claim = await store.claim(
    deliveryId,
    eventName,
    digest,
  );
  if (!claim.accepted) {
    return jsonResponse({
      status: "duplicate",
      state: claim.state,
    });
  }

  await store.mark(deliveryId, "PROCESSING");
  EdgeRuntime.waitUntil(
    processDelivery(
      deliveryId,
      eventName,
      payload,
      settings,
      store,
    ),
  );

  return jsonResponse(
    {
      status: "accepted",
      delivery: deliveryId,
    },
    202,
  );
});
