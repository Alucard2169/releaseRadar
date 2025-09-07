from datetime import datetime
import asyncio
import logging
from typing import Dict, Any, Optional, List, cast

import httpx
from fastapi import APIRouter, HTTPException, Depends

from src.schemas import (
    SeverityLevel,
    DependencyType,
    OutdatedDependency,
    RepositoryAnalysisRequest,
    RepositoryAnalysisResponse,
    RepoUrl,
)
from src.utils.github_dependency import DependencyAnalyzer
from src.utils.url_parser import parse_github_url
from src.utils.github_token import get_github_token
from src.utils.github import GitHubService 

logger = logging.getLogger(__name__)
router = APIRouter()


def create_repo_response(
    repo_info: Dict[str, Any],
    branch: str,
    languages: Dict[str, int],
    topics: List[str],
) -> Dict[str, Any]:
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
            "urls": {"ssh": repo_info.get("ssh_url")},
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


@router.post("/parse")
async def parse_github_url_api(data: RepoUrl):
    """Parse a GitHub URL and fetch repository information."""
    try:
        parsed = parse_github_url(data.url)
        if not parsed:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL format")
    except Exception as e:
        logger.error(f"URL parsing error for {data.url}: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid GitHub URL format")

    owner, repo = parsed.get("owner"), parsed.get("repo")
    branch = parsed.get("branch") or "main"

    if not owner or not repo:
        raise HTTPException(400, "URL must contain both repository owner and name")

    github_service = GitHubService()

    try:
        repo_info = await github_service.get_repo_info(owner, repo)
        languages = await github_service.get_repo_languages(owner, repo)

        topics_raw = repo_info.get("topics", [])
        topics = (
            [str(t) for t in topics_raw if isinstance(t, (str, int))]
            if isinstance(topics_raw, list)
            else [str(topics_raw)]
        )

        return create_repo_response(repo_info, branch, languages, topics)

    except httpx.HTTPStatusError as e:
        logger.error(f"GitHub API error for {owner}/{repo}: {e}")
        raise HTTPException(e.response.status_code, f"GitHub API error: {e}")
    except httpx.RequestError as e:
        logger.error(f"Network error for {owner}/{repo}: {e}")
        raise HTTPException(503, "Unable to connect to GitHub API. Try again later.")
    except Exception as e:
        logger.error(f"Unexpected error for {owner}/{repo}: {e}")
        raise HTTPException(500, "Unexpected server error")


@router.post("/analyze-repository", response_model=RepositoryAnalysisResponse)
async def analyze_repository(
    request: RepositoryAnalysisRequest,
    github_token: Optional[str] = Depends(get_github_token),
):
    try:
        # Parse repo URL
        result = parse_github_url(request.repo_url)
        if not result:
            raise ValueError("Invalid GitHub repository URL")
        owner, repo = result["owner"], result["repo"]

        github_service = GitHubService(github_token)
        analyzer = DependencyAnalyzer()
        repo_info, repo_languages = await asyncio.gather(
            github_service.get_repo_info(owner, repo),
            github_service.get_repo_languages(owner, repo)
        )

        # Supported files and language map
        file_analyzers = {
            "package.json": analyzer.analyze_package_json,
            "requirements.txt": analyzer.analyze_requirements_txt,
            "go.mod": analyzer.analyze_go_mod,
            "pom.xml": analyzer.analyze_maven_pom,
            "Cargo.toml": analyzer.analyze_cargo_toml,
            "composer.json": analyzer.analyze_composer_json,
            "Gemfile": analyzer.analyze_gemfile,
        }

        language_file_map = {
            "package.json": "JavaScript",
            "requirements.txt": "Python",
            "go.mod": "Go",
            "pom.xml": "Java",
            "Cargo.toml": "Rust",
            "composer.json": "PHP",
            "Gemfile": "Ruby",
        }

        # Fetch all relevant files concurrently
        fetch_tasks = {
            filename: github_service.get_file_content(owner, repo, filename)
            for filename, lang in language_file_map.items()
            if lang in repo_languages
        }
        file_contents = await asyncio.gather(*fetch_tasks.values())
        dependencies: List[Dict[str, Any]] = []

        # Analyze files
        for filename, content in zip(fetch_tasks.keys(), file_contents):
            if content:
                analyzer_func = file_analyzers[filename]
                if filename in ["package.json", "composer.json"]:
                    deps = await analyzer_func(content, request.include_dev_dependencies)
                else:
                    deps = await analyzer_func(content)
                dependencies.extend(deps)

        # Early exit if no dependencies
        if not dependencies:
            return RepositoryAnalysisResponse(
                repository=repo_info["name"],
                owner=repo_info["owner"]["login"],
                analyzed_at=datetime.utcnow().isoformat(),
                total_dependencies=0,
                outdated_dependencies=0,
                vulnerable_dependencies=0,
                risk_summary={"critical": 0, "high": 0, "moderate": 0, "low": 0},
                dependencies=[]
            )

        # Group tasks per dependency type
        tasks, dep_map = [], []
        for dep in dependencies:
            dep_type = dep["type"]
            check_func = {
                DependencyType.NPM: analyzer.check_npm_outdated,
                DependencyType.PIP: analyzer.check_pypi_outdated,
                DependencyType.GO: analyzer.check_go_outdated,
                DependencyType.MAVEN: analyzer.check_maven_outdated,
                DependencyType.CARGO: analyzer.check_cargo_outdated,
                DependencyType.COMPOSER: analyzer.check_composer_outdated,
                DependencyType.GEM: analyzer.check_gem_outdated,
       
            }.get(dep_type)
            if check_func:
                tasks.append(check_func(dep["name"], dep["version"]))
                dep_map.append(dep)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        analyzed_dependencies: List[OutdatedDependency] = []

        for dep, result in zip(dep_map, results):
            if isinstance(result, Exception):
                logger.error(f"Dependency check failed for {dep['name']}: {result}")
                latest_version = dep["version"]
                is_outdated = False
            else:
                result = cast(Dict[str, Any], result)
                latest_version = result.get("latest_version", dep["version"])
                is_outdated = result.get("is_outdated", False)

            vulnerabilities: List = []
            if request.check_vulnerabilities and is_outdated:
                try:
                    vulnerabilities = await analyzer.check_vulnerabilities(
                        dep["name"], dep["version"], dep["type"]
                    )
                except Exception as e:
                    logger.error(f"Vulnerability check failed for {dep['name']}: {e}")

            risk_level = SeverityLevel.LOW
            if vulnerabilities:
                risk_level = max((v.severity for v in vulnerabilities), default=SeverityLevel.LOW)
            elif is_outdated:
                risk_level = SeverityLevel.MODERATE

            analyzed_dependencies.append(
                OutdatedDependency(
                    name=dep["name"],
                    current_version=dep["version"],
                    latest_version=latest_version,
                    dependency_type=dep["type"],
                    is_outdated=is_outdated,
                    vulnerabilities=vulnerabilities,
                    risk_level=risk_level,
                    update_available=is_outdated,
                )
            )

        total = len(analyzed_dependencies)
        risk_summary = {
            "critical": sum(dep.risk_level == SeverityLevel.CRITICAL for dep in analyzed_dependencies),
            "high": sum(dep.risk_level == SeverityLevel.HIGH for dep in analyzed_dependencies),
            "moderate": sum(dep.risk_level == SeverityLevel.MODERATE for dep in analyzed_dependencies),
            "low": sum(dep.risk_level == SeverityLevel.LOW for dep in analyzed_dependencies),
        }

        return RepositoryAnalysisResponse(
            repository=repo_info["name"],
            owner=repo_info["owner"]["login"],
            analyzed_at=datetime.utcnow().isoformat(),
            total_dependencies=total,
            outdated_dependencies=sum(dep.is_outdated for dep in analyzed_dependencies),
            vulnerable_dependencies=sum(bool(dep.vulnerabilities) for dep in analyzed_dependencies),
            risk_summary=risk_summary,
            dependencies=analyzed_dependencies,
        )

    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(500, f"Analysis failed: {e}")
