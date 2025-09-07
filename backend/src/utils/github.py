import base64
from typing import Optional, List, Dict, Any

import httpx
from fastapi import HTTPException



class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "DependencySecurityAnalyzer/1.0",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"

    async def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/repos/{owner}/{repo}", headers=self.headers)
            if response.status_code == 404:
                raise HTTPException(404, "Repository not found")
            elif response.status_code == 403:
                raise HTTPException(403, "Access denied. Repository may be private or rate limit exceeded")
            response.raise_for_status()
            return response.json()

    async def get_repo_languages(self, owner: str, repo: str) -> Dict[str, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/repos/{owner}/{repo}/languages", headers=self.headers)
            return response.json() if response.status_code == 200 else {}

    async def get_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> Optional[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/contents/{path}", headers=self.headers, params={"ref": branch}
            )
            if response.status_code == 404 and branch == "main":
                return await self.get_file_content(owner, repo, path, "master")
            response.raise_for_status()
            data = response.json()
            if data.get("encoding") == "base64":
                return base64.b64decode(data["content"]).decode("utf-8")
            return data.get("content")

    async def get_vulnerability_alerts(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        if not self.token:
            return []
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/repos/{owner}/{repo}/vulnerability-alerts", headers=self.headers)
            if response.status_code in [403, 404]:
                return []
            response.raise_for_status()
            return response.json()
