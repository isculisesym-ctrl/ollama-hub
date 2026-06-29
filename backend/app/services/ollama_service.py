"""Ollama service — communicates with local Ollama server"""

import json
from collections.abc import AsyncGenerator

import httpx
from app.config import settings


class OllamaService:
    def __init__(self, base_url: str | None = None, timeout: int | None = None):
        self.base_url = (base_url or settings.OLLAMA_HOST).rstrip("/")
        self.timeout = timeout or settings.OLLAMA_TIMEOUT

    async def health_check(self) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(self.base_url)
                if resp.status_code == 200:
                    return {"status": "running", "url": self.base_url}
                return {"status": "error", "detail": f"HTTP {resp.status_code}"}
        except httpx.ConnectError:
            return {"status": "offline", "detail": "Cannot connect to Ollama"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}

    async def list_models(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{self.base_url}/api/tags")
            resp.raise_for_status()
            data = resp.json()
            return data.get("models", [])

    async def get_model_info(self, model_name: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{self.base_url}/api/show",
                json={"name": model_name},
            )
            resp.raise_for_status()
            return resp.json()

    async def generate(self, prompt: str, model: str | None = None, system: str | None = None) -> dict:
        model = model or settings.OLLAMA_MODEL
        payload = {"model": model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "response": data.get("response", ""),
                "model": model,
                "provider": "ollama",
                "usage": {
                    "total_duration": data.get("total_duration"),
                    "eval_count": data.get("eval_count"),
                },
            }


    async def generate_stream(
        self, prompt: str, model: str | None = None, system: str | None = None
    ) -> AsyncGenerator[str, None]:
        model = model or settings.OLLAMA_MODEL
        payload = {"model": model, "prompt": prompt, "stream": True}
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST", f"{self.base_url}/api/generate", json=payload
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    token = chunk.get("response", "")
                    if token:
                        yield json.dumps({"token": token, "model": model, "provider": "ollama"})
                    if chunk.get("done"):
                        yield json.dumps({
                            "done": True,
                            "model": model,
                            "provider": "ollama",
                            "usage": {
                                "total_duration": chunk.get("total_duration"),
                                "eval_count": chunk.get("eval_count"),
                            },
                        })


ollama_service = OllamaService()
