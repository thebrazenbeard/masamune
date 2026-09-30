from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Any

import httpx
import jwt

from .settings import Settings


@dataclass(frozen=True)
class GitHubFile:
    path: str
    content: str


class GitHubAppClient:
    def __init__(self, settings: Settings, installation_id: int) -> None:
        self.settings = settings
        self.installation_id = installation_id
        self._token: str | None = None
        self._token_expires_at = 0.0

    def _app_jwt(self) -> str:
        now = int(time.time())
        payload = {
            "iat": now - 30,
            "exp": now + 8 * 60,
            "iss": self.settings.github_app_id,
        }
        return jwt.encode(
            payload,
            self.settings.github_private_key.replace("\\n", "\n"),
            algorithm="RS256",
        )

    async def _installation_token(self) -> str:
        if self._token and time.time() < self._token_expires_at - 60:
            return self._token
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(
                f"{self.settings.github_api_url}/app/installations/{self.installation_id}/access_tokens",
                headers={
                    "Authorization": f"Bearer {self._app_jwt()}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            )
            response.raise_for_status()
            data = response.json()
            self._token = data["token"]
            self._token_expires_at = time.time() + 50 * 60
            return self._token

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        token = await self._installation_token()
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.request(
                method,
                f"{self.settings.github_api_url}{path}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                json=json_body,
                params=params,
            )
            response.raise_for_status()
            if response.status_code == 204:
                return None
            return response.json()

    async def repo(self, full_name: str) -> dict[str, Any]:
        return await self.request("GET", f"/repos/{full_name}")

    async def pull(self, full_name: str, number: int) -> dict[str, Any]:
        return await self.request("GET", f"/repos/{full_name}/pulls/{number}")

    async def issue(self, full_name: str, number: int) -> dict[str, Any]:
        return await self.request("GET", f"/repos/{full_name}/issues/{number}")

    async def default_head(self, full_name: str) -> tuple[str, str]:
        repo = await self.repo(full_name)
        branch = repo["default_branch"]
        ref = await self.request("GET", f"/repos/{full_name}/git/ref/heads/{branch}")
        commit_sha = ref["object"]["sha"]
        commit = await self.request("GET", f"/repos/{full_name}/git/commits/{commit_sha}")
        return commit_sha, commit["tree"]["sha"]

    async def pull_files(self, full_name: str, number: int) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []
        page = 1
        while len(files) < 3000:
            batch = await self.request(
                "GET",
                f"/repos/{full_name}/pulls/{number}/files",
                params={"per_page": 100, "page": page},
            )
            files.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return files[:3000]

    async def collaborator_permission(self, full_name: str, username: str) -> str:
        try:
            data = await self.request(
                "GET",
                f"/repos/{full_name}/collaborators/{username}/permission",
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return "none"
            raise
        return str(data.get("permission") or "none").lower()

    async def commit_tree_sha(self, full_name: str, commit_sha: str) -> str:
        commit = await self.request("GET", f"/repos/{full_name}/git/commits/{commit_sha}")
        return commit["tree"]["sha"]

    async def tree_paths(self, full_name: str, sha: str) -> list[str]:
        data = await self.request(
            "GET",
            f"/repos/{full_name}/git/trees/{sha}",
            params={"recursive": "1"},
        )
        if data.get("truncated"):
            raise RuntimeError(
                "GitHub recursive tree response was truncated; refusing partial tree scan"
            )
        return [
            item["path"]
            for item in data.get("tree", [])
            if item.get("type") == "blob" and isinstance(item.get("path"), str)
        ]

    async def file_text(self, full_name: str, path: str, ref: str) -> str | None:
        try:
            data = await self.request(
                "GET",
                f"/repos/{full_name}/contents/{path}",
                params={"ref": ref},
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in {404, 422}:
                return None
            raise
        if data.get("encoding") != "base64" or "content" not in data:
            return None
        raw = base64.b64decode(data["content"], validate=False)
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return None

    async def create_check(
        self,
        full_name: str,
        head_sha: str,
        name: str,
        title: str,
        summary: str,
        text: str,
    ) -> dict[str, Any]:
        return await self.request(
            "POST",
            f"/repos/{full_name}/check-runs",
            json_body={
                "name": name,
                "head_sha": head_sha,
                "status": "completed",
                "conclusion": "neutral",
                "output": {
                    "title": title[:255],
                    "summary": summary[:65_535],
                    "text": text[:65_535],
                },
            },
        )

    async def issue_comments(self, full_name: str, issue_number: int) -> list[dict[str, Any]]:
        comments: list[dict[str, Any]] = []
        page = 1
        while page <= 10:
            batch = await self.request(
                "GET",
                f"/repos/{full_name}/issues/{issue_number}/comments",
                params={"per_page": 100, "page": page},
            )
            comments.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return comments

    async def has_comment_marker(
        self,
        full_name: str,
        issue_number: int,
        marker: str,
    ) -> bool:
        comments = await self.issue_comments(full_name, issue_number)
        return any(marker in (comment.get("body") or "") for comment in comments)

    async def comment(self, full_name: str, issue_number: int, body: str) -> dict[str, Any]:
        return await self.request(
            "POST",
            f"/repos/{full_name}/issues/{issue_number}/comments",
            json_body={"body": body[:65_000]},
        )
