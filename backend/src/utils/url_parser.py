from typing import Optional, Dict
import re


# GitHub URL Parser
def parse_github_url(url: str) -> Optional[Dict[str, str]]:
    patterns = [
        # HTTPS with optional branch and path
        r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?(?:/tree/(?P<branch>[^/]+)(?:/(?P<path>.*))?)?$",
        # SSH format
        r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$",
        # Git protocol
        r"^git://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$",
        # GitHub shorthand 
        r"^github:(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:#(?P<branch>[^/]+))?$",
    ]

    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            result = match.groupdict()
            if result.get("repo"):
                result["repo"] = result["repo"].replace(".git", "")
            result["branch"] = result.get("branch") or "main"
            return result

    return None


# Example usage
# url = "https://github.com/<github_username>/<repo_name>"
# print(parse_github_url(url))
# {'owner': '<github_username>', 'repo': '<repo_name>', 'branch': 'main', 'path': None}