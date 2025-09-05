from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
import httpx
import logging

from ..schemas import RepoUrl
from ..utils.url_parser import parse_github_url
from ..utils.github import get_repo_info, get_repo_languages, get_repo_topics

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


def create_repo_response(repo_info: Dict[str, Any], branch: str, 
                        languages: Dict[str, int], topics: list[str]) -> Dict[str, Any]:
    """Create a normalized repository response."""
    return {
        "repo": {
            "id": repo_info.get("id"),
            "name": repo_info.get("name"),
            "full_name": repo_info.get("full_name"),
            "description": repo_info.get("description"),
            "is_private": repo_info.get("private", False),
            "is_fork": repo_info.get("fork", False),
            "owner": {
                "login": repo_info.get("owner", {}).get("login"),
                "avatar_url": repo_info.get("owner", {}).get("avatar_url"),
                "profile_url": repo_info.get("owner", {}).get("html_url"),
            },
            "urls": {
                "html": repo_info.get("html_url"),
                "ssh": repo_info.get("ssh_url"),
                "clone": repo_info.get("clone_url"),
            },
            "stats": {
                "stars": repo_info.get("stargazers_count", 0),
                "watchers": repo_info.get("watchers_count", 0),
                "forks": repo_info.get("forks_count", 0),
                "open_issues": repo_info.get("open_issues_count", 0),
            },
            "timestamps": {
                "created_at": repo_info.get("created_at"),
                "updated_at": repo_info.get("updated_at"),
                "pushed_at": repo_info.get("pushed_at"),
            },
            "branch": branch,
            "languages": languages,
            "topics": topics,
        }
    }


async def fetch_additional_repo_data(owner: str, repo: str) -> tuple[Dict[str, int], list[str]]:
    """Fetch repository languages and topics with error handling."""
    languages: Dict[str, int] = {}
    topics: list[str] = []
    
    # Fetch languages
    try:
        languages = await get_repo_languages(owner, repo)
    except Exception as e:
        logger.warning(f"Failed to fetch languages for {owner}/{repo}: {e}")
    
    # Fetch topics
    try:
        topics = await get_repo_topics(owner, repo)
    except Exception as e:
        logger.warning(f"Failed to fetch topics for {owner}/{repo}: {e}")
    
    return languages, topics


@router.post("/parse")
async def parse_github_url_api(data: RepoUrl):
    """
    Parse a GitHub URL and fetch comprehensive repository information.
    
    Args:
        data: RepoUrl schema containing the GitHub URL to parse
        
    Returns:
        Dict containing comprehensive repository information
        
    Raises:
        HTTPException: For various error conditions (400, 404, 503, 500)
    """
    # Parse the GitHub URL
    parsed = parse_github_url(data.url)
    if not parsed:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL format")
    
    # Extract repository components
    owner = parsed.get("owner")
    repo = parsed.get("repo")
    branch = parsed.get("branch") or "main"
    
    if not owner or not repo:
        raise HTTPException(
            status_code=400, 
            detail="URL must contain both repository owner and name"
        )
    
    try:
        # Fetch basic repository information
        repo_info = await get_repo_info(owner, repo, branch)
        if "error" in repo_info:
            raise HTTPException(status_code=404, detail=repo_info["error"])
        
        # Fetch additional repository data (languages and topics)
        languages, topics = await fetch_additional_repo_data(owner, repo)
        
        # Create and return normalized response
        return create_repo_response(repo_info, branch, languages, topics)
        
    except httpx.HTTPStatusError as e:
        logger.error(f"GitHub API HTTP error for {owner}/{repo}: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub API error: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error while fetching {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to GitHub API. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error processing {owner}/{repo}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the repository"
        )