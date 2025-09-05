from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Repo(Base):
    __tablename__ = "repos"
    
    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String, index=True)
    owner_name = Column(String, index=True)
    repo_link = Column(String, unique=True, index=True)
    branch = Column(String, default="main")
    stars_count = Column(Integer, default=0)
    forks_count = Column(Integer, default=0)
    issues_count = Column(Integer, default=0)
    date_added = Column(DateTime, default=datetime.utcnow)
    last_fetched = Column(DateTime, default=datetime.utcnow)
    technologies = Column(String) 
    description = Column(String)
    tags = Column(String)
    
    dependencies = relationship("Dependency", back_populates="repo")


class Dependency(Base):
    __tablename__ = "dependencies"
    
    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"))
    name = Column(String, index=True)
    version = Column(String)
    latest_version = Column(String)
    author = Column(String, nullable=True)
    outdated = Column(Boolean, default=False)
    
    repo = relationship("Repo", back_populates="dependencies")
