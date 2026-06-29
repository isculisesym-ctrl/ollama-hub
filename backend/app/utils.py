"""Utility functions — validation, error handling"""

from fastapi import HTTPException
import json


def validate_project_name(name: str) -> str:
    if not name or not name.strip():
        raise HTTPException(status_code=422, detail="Project name cannot be empty")
    if len(name) > 200:
        raise HTTPException(status_code=422, detail="Project name too long (max 200 chars)")
    return name.strip()


def validate_message(content: str) -> str:
    if not content or not content.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")
    if len(content) > 50000:
        raise HTTPException(status_code=422, detail="Message too long (max 50000 chars)")
    return content.strip()


def validate_model_name(model: str) -> str:
    if not model or not model.strip():
        raise HTTPException(status_code=422, detail="Model name cannot be empty")
    if len(model) > 200:
        raise HTTPException(status_code=422, detail="Model name too long")
    return model.strip()


def validate_api_key(key: str) -> str:
    if not key or not key.strip():
        raise HTTPException(status_code=422, detail="API key cannot be empty")
    if len(key) < 10:
        raise HTTPException(status_code=422, detail="API key too short")
    return key.strip()


def safe_json_parse(text: str, default: dict | None = None) -> dict:
    try:
        return json.loads(text) if text else (default or {})
    except json.JSONDecodeError:
        return default or {}
