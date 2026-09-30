import { signGithubAppJwt } from "./crypto.ts";

export interface GithubConfig {
  appId: string;
  privateKey: string;
  apiUrl: string;
  timeoutMs: number;
}

export interface GithubPull {
  head: { sha: string };
  base: { sha: string };
  title?: string | null;
  body?: string | null;
  html_url: string;
}

export interface GithubIssue {
  title?: string | null;
  body?: string | null;
  html_url: string;
}

export interface GithubPullFile {
  filename: string;
  status?: string;
  additions?: number;
  deletions?: number;
  changes?: number;
  patch?: string;
}

interface GithubRepo {
  default_branch: string;
  private?: boolean;
}

interface GithubRef {
  object: { sha: string };
}

interface GithubCommit {
  tree: { sha: string };
}

interface GithubTree {
  truncated?: boolean;
  tree?: Array<{ type?: string; path?: string }>;
}

interface GithubContent {
  encoding?: string;
  content?: string;
}

interface GithubPermission {
  permission?: string;
}

interface GithubComment {
  body?: string | null;
}

type JsonObject = Record<string, unknown>;

export class GitHubAppClient {
  #token: string | null = null;
  #tokenExpiresAt = 0;

  constructor(
    private readonly config: GithubConfig,
    private readonly installationId: number,
  ) {}

  async #installationToken(): Promise<string> {
    if (this.#token && Date.now() < this.#tokenExpiresAt - 60_000) {
      return this.#token;
    }
    const appJwt = await signGithubAppJwt(
      this.config.appId,
      this.config.privateKey,
    );
    const response = await this.#raw(
      "POST",
      `/app/installations/${this.installationId}/access_tokens`,
      appJwt,
    );
    const data = await response.json() as { token?: unknown };
    this.#token = String(data.token);
    this.#tokenExpiresAt = Date.now() + 50 * 60_000;
    return this.#token;
  }

  async #raw(
    method: string,
    path: string,
    bearer: string,
    body?: unknown,
    params?: Record<string, string | number>,
  ): Promise<Response> {
    const url = new URL(`${this.config.apiUrl}${path}`);
    for (const [key, value] of Object.entries(params ?? {})) {
      url.searchParams.set(key, String(value));
    }
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.config.timeoutMs);
    try {
      const response = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${bearer}`,
          Accept: "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
          ...(body === undefined ? {} : { "Content-Type": "application/json" }),
        },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal,
      });
      if (!response.ok) {
        const text = await response.text();
        const error = new Error(
          `GitHub ${method} ${path} failed: ${response.status} ${
            text.slice(0, 500)
          }`,
        ) as Error & { status?: number };
        error.status = response.status;
        throw error;
      }
      return response;
    } finally {
      clearTimeout(timer);
    }
  }

  async request<T>(
    method: string,
    path: string,
    body?: unknown,
    params?: Record<string, string | number>,
  ): Promise<T> {
    const token = await this.#installationToken();
    const response = await this.#raw(method, path, token, body, params);
    if (response.status === 204) return undefined as T;
    return await response.json() as T;
  }

  repo(fullName: string): Promise<GithubRepo> {
    return this.request("GET", `/repos/${fullName}`);
  }

  pull(fullName: string, number: number): Promise<GithubPull> {
    return this.request("GET", `/repos/${fullName}/pulls/${number}`);
  }

  issue(fullName: string, number: number): Promise<GithubIssue> {
    return this.request("GET", `/repos/${fullName}/issues/${number}`);
  }

  async pullFiles(
    fullName: string,
    number: number,
  ): Promise<GithubPullFile[]> {
    const files: GithubPullFile[] = [];
    for (let page = 1; page <= 30; page++) {
      const batch = await this.request<GithubPullFile[]>(
        "GET",
        `/repos/${fullName}/pulls/${number}/files`,
        undefined,
        { per_page: 100, page },
      );
      files.push(...batch);
      if (batch.length < 100) break;
    }
    return files;
  }

  async defaultHead(
    fullName: string,
  ): Promise<{ commitSha: string; treeSha: string }> {
    const repo = await this.repo(fullName);
    const branch = String(repo.default_branch);
    const ref = await this.request<GithubRef>(
      "GET",
      `/repos/${fullName}/git/ref/heads/${encodeURIComponent(branch)}`,
    );
    const commitSha = String(ref.object.sha);
    const commit = await this.request<GithubCommit>(
      "GET",
      `/repos/${fullName}/git/commits/${commitSha}`,
    );
    return { commitSha, treeSha: String(commit.tree.sha) };
  }

  async treePaths(fullName: string, treeSha: string): Promise<string[]> {
    const data = await this.request<GithubTree>(
      "GET",
      `/repos/${fullName}/git/trees/${treeSha}`,
      undefined,
      { recursive: 1 },
    );
    if (data.truncated) {
      throw new Error(
        "GitHub recursive tree response was truncated; refusing partial tree scan",
      );
    }
    return (data.tree ?? [])
      .filter(
        (item): item is { type?: string; path: string } =>
          item.type === "blob" && typeof item.path === "string",
      )
      .map((item) => item.path);
  }

  async fileText(
    fullName: string,
    path: string,
    ref: string,
  ): Promise<string | null> {
    try {
      const data = await this.request<GithubContent>(
        "GET",
        `/repos/${fullName}/contents/${
          path.split("/").map(encodeURIComponent).join("/")
        }`,
        undefined,
        { ref },
      );
      if (data.encoding !== "base64" || typeof data.content !== "string") {
        return null;
      }
      const normalized = data.content.replace(/\s+/g, "");
      const bytes = Uint8Array.from(
        atob(normalized),
        (char) => char.charCodeAt(0),
      );
      return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    } catch (error) {
      const status = (error as Error & { status?: number }).status;
      if (status === 404 || status === 422) return null;
      if (error instanceof TypeError) return null;
      throw error;
    }
  }

  async collaboratorPermission(
    fullName: string,
    username: string,
  ): Promise<string> {
    try {
      const data = await this.request<GithubPermission>(
        "GET",
        `/repos/${fullName}/collaborators/${
          encodeURIComponent(username)
        }/permission`,
      );
      return String(data.permission ?? "none").toLowerCase();
    } catch (error) {
      if ((error as Error & { status?: number }).status === 404) return "none";
      throw error;
    }
  }

  async issueComments(
    fullName: string,
    issueNumber: number,
  ): Promise<GithubComment[]> {
    const comments: GithubComment[] = [];
    for (let page = 1; page <= 10; page++) {
      const batch = await this.request<GithubComment[]>(
        "GET",
        `/repos/${fullName}/issues/${issueNumber}/comments`,
        undefined,
        { per_page: 100, page },
      );
      comments.push(...batch);
      if (batch.length < 100) break;
    }
    return comments;
  }

  async hasCommentMarker(
    fullName: string,
    issueNumber: number,
    marker: string,
  ): Promise<boolean> {
    const comments = await this.issueComments(fullName, issueNumber);
    return comments.some((comment) =>
      String(comment.body ?? "").includes(marker)
    );
  }

  comment(
    fullName: string,
    issueNumber: number,
    body: string,
  ): Promise<JsonObject> {
    return this.request(
      "POST",
      `/repos/${fullName}/issues/${issueNumber}/comments`,
      { body: body.slice(0, 65_000) },
    );
  }
}
