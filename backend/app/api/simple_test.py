"""Simple test endpoint — Direct Ollama call, no async magic"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()


class SimpleTestRequest(BaseModel):
    prompt: str = "Hello, what is 2+2?"


@router.post("/test/ollama-simple")
async def test_ollama_simple(req: SimpleTestRequest):
    """Direct synchronous call to Ollama to test if it's working at all"""
    try:
        # Direct HTTP call to Ollama
        with httpx.Client(timeout=60) as client:
            response = client.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "neural-chat",
                    "prompt": req.prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "model": "neural-chat",
                "response": data.get("response", ""),
                "total_duration_ms": data.get("total_duration", 0) / 1_000_000,
            }

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Ollama timeout (60s). Model might be slow. Is it running? Try: ollama serve",
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama on 127.0.0.1:11434. Is it running?",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test/status")
async def test_status():
    """Quick status check of all services"""
    results = {
        "backend": "✅ OK (you're reading this)",
        "ollama": "❓ Checking...",
        "frontend": "⚠️  Check manually at http://localhost:5173",
    }

    # Test Ollama
    try:
        with httpx.Client(timeout=5) as client:
            resp = client.get("http://127.0.0.1:11434/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                model_count = len(data.get("models", []))
                results["ollama"] = f"✅ Running ({model_count} model(s))"
            else:
                results["ollama"] = f"❌ HTTP {resp.status_code}"
    except Exception as e:
        results["ollama"] = f"❌ {str(e)}"

    return results
