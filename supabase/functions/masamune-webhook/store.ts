import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { ReviewReport } from "./types.ts";

export interface DeliveryClaim {
  accepted: boolean;
  state: string;
}

export class DeliveryStore {
  readonly client: SupabaseClient;

  constructor(url: string, serviceRoleKey: string) {
    this.client = createClient(url, serviceRoleKey, {
      auth: { persistSession: false, autoRefreshToken: false },
      global: {
        headers: { "X-Client-Info": "masamune-edge-v0" },
      },
    });
  }

  async claim(
    deliveryId: string,
    eventName: string,
    payloadSha256: string,
  ): Promise<DeliveryClaim> {
    const now = new Date().toISOString();
    const { error } = await this.client.from("masamune_webhook_delivery")
      .insert({
        delivery_id: deliveryId,
        event_name: eventName,
        state: "ACCEPTED",
        received_at: now,
        updated_at: now,
        payload_sha256: payloadSha256,
        error: null,
      });

    if (!error) return { accepted: true, state: "ACCEPTED" };
    if (error.code !== "23505") {
      throw new Error(
        `delivery claim insert failed: ${error.code} ${error.message}`,
      );
    }

    const { data, error: readError } = await this.client
      .from("masamune_webhook_delivery")
      .select("state, updated_at, event_name, payload_sha256")
      .eq("delivery_id", deliveryId)
      .maybeSingle();

    if (readError) {
      throw new Error(`delivery claim read failed: ${readError.message}`);
    }
    if (!data) return { accepted: false, state: "UNKNOWN" };

    if (
      data.event_name !== eventName ||
      data.payload_sha256 !== payloadSha256
    ) {
      return { accepted: false, state: "CONFLICT" };
    }

    const staleProcessing = data.state === "PROCESSING" &&
      Date.now() - new Date(data.updated_at).getTime() >= 15 * 60_000;

    if (
      data.state === "FAILED" ||
      data.state === "READY_TO_PUBLISH" ||
      staleProcessing
    ) {
      const { error: retryError } = await this.client
        .from("masamune_webhook_delivery")
        .update({
          state: "ACCEPTED",
          updated_at: now,
          error: null,
        })
        .eq("delivery_id", deliveryId);

      if (retryError) {
        throw new Error(`delivery retry claim failed: ${retryError.message}`);
      }
      return { accepted: true, state: "ACCEPTED" };
    }

    return { accepted: false, state: String(data.state) };
  }

  async mark(
    deliveryId: string,
    state: string,
    errorText: string | null = null,
  ): Promise<void> {
    const { error } = await this.client
      .from("masamune_webhook_delivery")
      .update({
        state,
        updated_at: new Date().toISOString(),
        error: errorText?.slice(0, 2_000) ?? null,
      })
      .eq("delivery_id", deliveryId);

    if (error) {
      throw new Error(`delivery state update failed: ${error.message}`);
    }
  }

  async claimReviewBudget(
    reviewId: string,
    repository: string,
    globalLimit: number,
    repoLimit: number,
  ): Promise<boolean> {
    const { data, error } = await this.client.rpc(
      "masamune_claim_review_budget",
      {
        p_review_id: reviewId,
        p_repository: repository,
        p_global_limit: globalLimit,
        p_repo_limit: repoLimit,
      },
    );
    if (error) {
      throw new Error(`review budget claim failed: ${error.message}`);
    }
    return data === true;
  }

  async claimExecutionLease(
    reviewId: string,
    ttlSeconds = 240,
  ): Promise<boolean> {
    const { data, error } = await this.client.rpc(
      "masamune_claim_execution_lease",
      {
        p_review_id: reviewId,
        p_ttl_seconds: ttlSeconds,
      },
    );
    if (error) {
      throw new Error(`execution lease claim failed: ${error.message}`);
    }
    return data === true;
  }

  async releaseExecutionLease(reviewId: string): Promise<void> {
    const { error } = await this.client.rpc(
      "masamune_release_execution_lease",
      { p_review_id: reviewId },
    );
    if (error) {
      throw new Error(`execution lease release failed: ${error.message}`);
    }
  }

  async getReview(reviewId: string): Promise<ReviewReport | null> {
    const { data, error } = await this.client
      .from("masamune_review_receipt")
      .select("result_json")
      .eq("review_id", reviewId)
      .maybeSingle();

    if (error) {
      throw new Error(`review receipt read failed: ${error.message}`);
    }
    if (!data?.result_json) return null;
    return data.result_json as ReviewReport;
  }

  async saveReview(
    reviewId: string,
    deliveryId: string,
    report: ReviewReport,
  ): Promise<void> {
    const { error } = await this.client.from("masamune_review_receipt").upsert(
      {
        review_id: reviewId,
        delivery_id: deliveryId,
        repository: report.subject.repository,
        subject_kind: report.subject.kind,
        subject_number: report.subject.number ?? null,
        head_sha: report.subject.head_sha,
        result_json: report,
        created_at: new Date().toISOString(),
      },
      { onConflict: "review_id" },
    );
    if (error) throw new Error(`review receipt write failed: ${error.message}`);
  }
}
