"""Status API endpoints"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def get_status():
    """Get overall system status"""
    return {
        "ollama": {"status": "checking..."},
        "claude": {"status": "checking..."},
        "system": {"status": "ok"},
    }
