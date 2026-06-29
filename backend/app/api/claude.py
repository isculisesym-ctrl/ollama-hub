"""Claude API endpoints"""
from fastapi import APIRouter
router = APIRouter()

@router.post("/claude/test")
async def test_claude():
    return {"status": "ok"}
