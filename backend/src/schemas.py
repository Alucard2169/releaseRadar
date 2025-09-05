from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

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
