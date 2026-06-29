"""Admin API endpoints — logs, stats, auth management"""

import os
from fastapi import APIRouter, Depends, Query

from app.auth import require_api_key
from app.database import get_db, get_db_path
from app.logging_middleware import get_logs, get_log_stats

router = APIRouter()


@router.get("/admin/logs")
async def view_logs(
    limit: int = Query(default=50, ge=1, le=500),
    method: str | None = None,
    path_prefix: str | None = None,
    _key=Depends(require_api_key),
):
    return {"logs": get_logs(limit=limit, method=method, path_prefix=path_prefix)}


@router.get("/admin/logs/stats")
async def log_stats(_key=Depends(require_api_key)):
    return get_log_stats()


@router.get("/admin/stats")
async def system_stats(_key=Depends(require_api_key)):
    db_path = get_db_path()
    db_size_bytes = os.path.getsize(db_path) if os.path.exists(db_path) else 0

    with get_db() as conn:
        project_count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        chat_count = conn.execute("SELECT COUNT(*) FROM chats").fetchone()[0]

        provider_counts = conn.execute(
            "SELECT provider, COUNT(*) as count FROM chats GROUP BY provider"
        ).fetchall()
        providers = {row["provider"]: row["count"] for row in provider_counts}

        model_counts = conn.execute(
            "SELECT model, COUNT(*) as count FROM chats WHERE role='assistant' AND model != '' "
            "GROUP BY model ORDER BY count DESC LIMIT 10"
        ).fetchall()
        top_models = {row["model"]: row["count"] for row in model_counts}

        recent_activity = conn.execute(
            "SELECT DATE(created_at) as day, COUNT(*) as count FROM chats "
            "GROUP BY day ORDER BY day DESC LIMIT 7"
        ).fetchall()
        daily_activity = {row["day"]: row["count"] for row in recent_activity}

    return {
        "database": {
            "path": db_path,
            "size_bytes": db_size_bytes,
            "size_mb": round(db_size_bytes / (1024 * 1024), 2),
        },
        "projects": {"total": project_count},
        "chats": {
            "total": chat_count,
            "by_provider": providers,
            "top_models": top_models,
        },
        "daily_activity": daily_activity,
    }


@router.get("/admin/auth/status")
async def auth_status():
    from app.config import settings
    return {
        "auth_enabled": settings.AUTH_ENABLED,
        "api_key_set": bool(settings.API_KEY),
    }
