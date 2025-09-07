from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os



security = HTTPBearer(auto_error=False)


def get_github_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[str]:
    """Extract GitHub token from Authorization header"""
    if credentials:
        return credentials.credentials
    return os.getenv("GITHUB_TOKEN")