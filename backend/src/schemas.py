from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum


class RepoUrl(BaseModel):
    url: str


class DependencyBase(BaseModel):
    name: str
    version: str
    latest_version: Optional[str] = None
    author: Optional[str] = None
    outdated: bool = False


class RepoBase(BaseModel):
    repo_name: str
    owner_name: str
    repo_link: str
    branch: str = "main"
    stars_count: int = 0
    forks_count: int = 0
    issues_count: int = 0
    technologies: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    date_added: datetime
    last_fetched: datetime


class RepoWithDeps(RepoBase):
    dependencies: List[DependencyBase] = []
    
    class Config:
        orm_mode = True



# ----


class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"

class DependencyType(str, Enum):
    NPM = "npm"          
    PIP = "pip"          
    MAVEN = "maven"      
    GRADLE = "gradle"    
    COMPOSER = "composer" 
    NUGET = "nuget"      
    GO = "go"            
    CARGO = "cargo"      
    GEM = "gem"          

class VulnerabilityInfo(BaseModel):
    id: str
    summary: str
    severity: SeverityLevel
    cvss_score: Optional[float] = None
    published_at: str
    patched_versions: List[str] = []
    references: List[str] = []

class OutdatedDependency(BaseModel):
    name: str
    current_version: str
    latest_version: str
    dependency_type: DependencyType
    is_outdated: bool
    vulnerabilities: List[VulnerabilityInfo] = []
    risk_level: SeverityLevel
    update_available: bool

class RepositoryAnalysisRequest(BaseModel):
    repo_url: str
    include_dev_dependencies: bool = True
    check_vulnerabilities: bool = True

class RepositoryAnalysisResponse(BaseModel):
    repository: str
    owner: str
    analyzed_at: str
    total_dependencies: int
    outdated_dependencies: int
    vulnerable_dependencies: int
    risk_summary: Dict[str, int]  # Count by severity level
    dependencies: List[OutdatedDependency]