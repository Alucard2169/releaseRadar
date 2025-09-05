
from typing import Dict
import httpx

# Helper function to fetch repo infor from GitHub API
async def get_repo_info(owner: str, repo: str, branch: str): 
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        return {"error": f"Failed to fetch repo info: {response.status_code}"}

# Helper function to fetch repo topics from GitHub API
async def get_repo_topics(owner: str, repo: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{owner}/{repo}/topics"
        headers = {"Accept": "application/vnd.github.mercy-preview+json"}
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("names", [])
        return []


# Helper function to fetch repo languages from GitHub API
async def get_repo_languages(owner: str, repo: str) -> Dict[str, int]:
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{owner}/{repo}/languages"
        response = await client.get(url)
        if response.status_code == 200:
            # GitHub returns languages as {"Python": 12345, "JavaScript": 6789, ...}
            return response.json()
        return {}