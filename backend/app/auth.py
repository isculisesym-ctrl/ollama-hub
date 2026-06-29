"""API key authentication dependency"""

import secrets
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(key: str | None = Security(api_key_header)) -> str | None:
    if not settings.AUTH_ENABLED:
        return None
    if not key:
        raise HTTPException(status_code=401, detail="Missing API key")
    if not secrets.compare_digest(key, settings.API_KEY):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key


def optional_api_key(key: str | None = Security(api_key_header)) -> str | None:
    return key
