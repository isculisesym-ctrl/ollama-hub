"""Ollama API endpoints — model listing and info"""

from fastapi import APIRouter, HTTPException
import httpx

from app.services.ollama_service import ollama_service

router = APIRouter()


@router.get("/models")
async def list_models():
    try:
        models = await ollama_service.list_models()
        return {"models": models, "count": len(models)}
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Ollama server is not running")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Ollama API error")


@router.get("/models/{model_name}")
async def get_model_info(model_name: str):
    try:
        info = await ollama_service.get_model_info(model_name)
        return info
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Ollama server is not running")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")
        raise HTTPException(status_code=e.response.status_code, detail="Ollama API error")


@router.post("/ollama/test")
async def test_ollama():
    health = await ollama_service.health_check()
    if health["status"] != "running":
        raise HTTPException(status_code=503, detail=health.get("detail", "Ollama is not running"))
    return health
