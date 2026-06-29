"""Claude API endpoints — test connection"""

from fastapi import APIRouter, HTTPException

from app.services.claude_service import claude_service

router = APIRouter()


@router.post("/claude/test")
async def test_claude():
    health = await claude_service.health_check()
    if health["status"] not in ("connected",):
        status_code = 401 if health["status"] == "auth_error" else 503
        raise HTTPException(status_code=status_code, detail=health.get("detail", "Claude API error"))
    return health
