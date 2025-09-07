import httpx
import json
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta

from src.schemas import VulnerabilityInfo, SeverityLevel, DependencyType


class DependencyAnalyzer:
    def __init__(self):
        self.vulnerability_db_cache = {}
        self.cache_expiry = timedelta(hours=1)

    # ---------------------------
    # JS / Node.js
    # ---------------------------
    async def analyze_package_json(self, content: str, include_dev: bool = True) -> List[Dict[str, Any]]:
        """Analyze Node.js package.json dependencies"""
        try:
            data = json.loads(content)
            dependencies = []

            if "dependencies" in data:
                for name, version in data["dependencies"].items():
                    dependencies.append({
                        "name": name,
                        "version": self._clean_version(version),
                        "type": DependencyType.NPM,
                        "is_dev": False
                    })

            if include_dev and "devDependencies" in data:
                for name, version in data["devDependencies"].items():
                    dependencies.append({
                        "name": name,
                        "version": self._clean_version(version),
                        "type": DependencyType.NPM,
                        "is_dev": True
                    })

            return dependencies
        except json.JSONDecodeError:
            return []

    # ---------------------------
    # Python
    # ---------------------------
    async def analyze_requirements_txt(self, content: str) -> List[Dict[str, Any]]:
        """Analyze Python requirements.txt dependencies"""
        dependencies = []
        lines = content.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            match = re.match(r'^([a-zA-Z0-9\-_\.]+)([>=<!=~]+)?([0-9\.]+)?', line)
            if match:
                name, operator, version = match.groups()
                dependencies.append({
                    "name": name,
                    "version": version or "latest",
                    "type": DependencyType.PIP,
                    "is_dev": False,
                    "operator": operator or "=="
                })

        return dependencies

    # ---------------------------
    # Go
    # ---------------------------
    async def analyze_go_mod(self, content: str) -> List[Dict[str, Any]]:
        """Analyze Go modules from go.mod"""
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("require "):
                parts = line.replace("require", "").strip().split()
                if len(parts) >= 2:
                    name, version = parts[0], parts[1]
                    dependencies.append({
                        "name": name,
                        "version": version,
                        "type": DependencyType.GO,
                        "is_dev": False
                    })
        return dependencies

    # ---------------------------
    # Maven (Java)
    # ---------------------------
    async def analyze_maven_pom(self, content: str) -> List[Dict[str, Any]]:
        """Analyze Maven dependencies from pom.xml (regex-based)"""
        dependencies = []
        matches = re.findall(
            r"<dependency>.*?<groupId>(.*?)</groupId>.*?<artifactId>(.*?)</artifactId>.*?<version>(.*?)</version>.*?</dependency>",
            content,
            re.DOTALL
        )
        for group_id, artifact_id, version in matches:
            dependencies.append({
                "name": f"{group_id}:{artifact_id}",
                "version": version,
                "type": DependencyType.MAVEN,
                "is_dev": False
            })
        return dependencies

    # ---------------------------
    # Cargo (Rust)
    # ---------------------------
    async def analyze_cargo_toml(self, content: str) -> List[Dict[str, Any]]:
        """Analyze Cargo.toml (Rust) dependencies"""
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("["):
                parts = line.split("=")
                if len(parts) == 2:
                    name = parts[0].strip()
                    version = parts[1].strip().strip('"')
                    dependencies.append({
                        "name": name,
                        "version": version,
                        "type": DependencyType.CARGO,
                        "is_dev": False
                    })
        return dependencies

    # ---------------------------
    # Composer (PHP)
    # ---------------------------
    async def analyze_composer_json(self, content: str, include_dev: bool = True) -> List[Dict[str, Any]]:
        """Analyze PHP composer.json dependencies"""
        try:
            data = json.loads(content)
            dependencies = []

            if "require" in data:
                for name, version in data["require"].items():
                    dependencies.append({
                        "name": name,
                        "version": self._clean_version(version),
                        "type": DependencyType.COMPOSER,
                        "is_dev": False
                    })

            if include_dev and "require-dev" in data:
                for name, version in data["require-dev"].items():
                    dependencies.append({
                        "name": name,
                        "version": self._clean_version(version),
                        "type": DependencyType.COMPOSER,
                        "is_dev": True
                    })

            return dependencies
        except json.JSONDecodeError:
            return []

    # ---------------------------
    # Gemfile (Ruby / Bundler)
    # ---------------------------
    async def analyze_gemfile(self, content: str) -> List[Dict[str, Any]]:
        """Analyze Ruby Gemfile dependencies (basic parser)"""
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("gem "):
                parts = re.findall(r'"(.*?)"', line)
                if parts:
                    name = parts[0]
                    version = parts[1] if len(parts) > 1 else "latest"
                    dependencies.append({
                        "name": name,
                        "version": version,
                        "type": DependencyType.GEM,
                        "is_dev": False
                    })
        return dependencies

    # ---------------------------
    # Outdated Checks
    # ---------------------------
    async def check_npm_outdated(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Check if NPM package is outdated"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://registry.npmjs.org/{package_name}")
                if response.status_code != 200:
                    return {"latest_version": current_version, "is_outdated": False}

                data = response.json()
                latest_version = data.get("dist-tags", {}).get("latest", current_version)

                return {
                    "latest_version": latest_version,
                    "is_outdated": latest_version != current_version,
                    "description": data.get("description", ""),
                    "homepage": data.get("homepage", "")
                }
        except Exception:
            return {"latest_version": current_version, "is_outdated": False}

    async def check_pypi_outdated(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Check if PyPI package is outdated"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://pypi.org/pypi/{package_name}/json")
                if response.status_code != 200:
                    return {"latest_version": current_version, "is_outdated": False}

                data = response.json()
                latest_version = data.get("info", {}).get("version", current_version)

                return {
                    "latest_version": latest_version,
                    "is_outdated": latest_version != current_version,
                    "description": data.get("info", {}).get("summary", ""),
                    "homepage": data.get("info", {}).get("home_page", "")
                }
        except Exception:
            return {"latest_version": current_version, "is_outdated": False}

    async def check_go_outdated(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Stub for Go package version check"""
        return {"latest_version": current_version, "is_outdated": False}

    async def check_maven_outdated(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Stub for Maven package version check"""
        return {"latest_version": current_version, "is_outdated": False}

    async def check_cargo_outdated(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Stub for Cargo package version check"""
        return {"latest_version": current_version, "is_outdated": False}

    async def check_composer_outdated(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Stub for Composer (PHP) version check"""
        return {"latest_version": current_version, "is_outdated": False}

    async def check_gem_outdated(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Stub for Ruby gem version check"""
        return {"latest_version": current_version, "is_outdated": False}

    # ---------------------------
    # Vulnerability Check
    # ---------------------------
    async def check_vulnerabilities(self, package_name: str, version: str, dependency_type: DependencyType) -> List[VulnerabilityInfo]:
        """Check for known vulnerabilities in package"""
        vulnerabilities = []
        try:
            async with httpx.AsyncClient() as client:
                query_data = {
                    "package": {
                        "name": package_name,
                        "ecosystem": dependency_type.value
                    },
                    "version": version
                }
                response = await client.post(
                    "https://api.osv.dev/v1/query",
                    json=query_data,
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    for vuln in data.get("vulns", []):
                        vulnerabilities.append(VulnerabilityInfo(
                            id=vuln.get("id", ""),
                            summary=vuln.get("summary", "Unknown vulnerability"),
                            severity=self._map_severity(vuln.get("database_specific", {}).get("severity", "moderate")),
                            published_at=vuln.get("published", datetime.utcnow().isoformat()),
                            references=vuln.get("references", [])
                        ))
        except Exception:
            pass
        return vulnerabilities

    # ---------------------------
    # Helpers
    # ---------------------------
    def _clean_version(self, version: str) -> str:
        """Clean version string by removing operators"""
        return re.sub(r'^[^0-9]*', '', version)

    def _map_severity(self, severity: str) -> SeverityLevel:
        """Map different severity formats to our enum"""
        severity_lower = severity.lower()
        if severity_lower in ["critical", "high"]:
            return SeverityLevel.CRITICAL if "critical" in severity_lower else SeverityLevel.HIGH
        elif severity_lower in ["medium", "moderate"]:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.LOW
