"""Ollama API endpoints"""
from fastapi import APIRouter
router = APIRouter()

@router.get("/models")
async def list_models():
    return {"models": []}

@router.post("/ollama/test")
async def test_ollama():
    return {"status": "ok"}
