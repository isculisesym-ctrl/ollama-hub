"""Status API endpoints — health checks for Ollama, Claude, and system"""

import psutil
from fastapi import APIRouter

from app.services.ollama_service import ollama_service
from app.services.claude_service import claude_service

router = APIRouter()


@router.get("/status")
async def get_status():
    ollama_health = await ollama_service.health_check()
    claude_health = await claude_service.health_check()

    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()

    return {
        "ollama": ollama_health,
        "claude": claude_health,
        "system": {
            "status": "ok",
            "cpu_percent": cpu_percent,
            "memory_total_gb": round(memory.total / (1024**3), 1),
            "memory_used_percent": memory.percent,
        },
    }


@router.get("/status/ollama")
async def get_ollama_status():
    return await ollama_service.health_check()


@router.get("/status/claude")
async def get_claude_status():
    return await claude_service.health_check()
