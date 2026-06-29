"""Claude API service — communicates with Anthropic API"""

import httpx
from app.config import settings

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


class ClaudeService:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.CLAUDE_API_KEY
        self.model = model or settings.CLAUDE_MODEL

    def _headers(self) -> dict:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    async def health_check(self) -> dict:
        if not self.api_key:
            return {"status": "not_configured", "detail": "API key not set"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    ANTHROPIC_API_URL,
                    headers=self._headers(),
                    json={
                        "model": self.model,
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "ping"}],
                    },
                )
                if resp.status_code == 200:
                    return {"status": "connected", "model": self.model}
                if resp.status_code == 401:
                    return {"status": "auth_error", "detail": "Invalid API key"}
                return {"status": "error", "detail": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}

    async def generate(self, prompt: str, model: str | None = None, system: str | None = None) -> dict:
        if not self.api_key:
            raise ValueError("Claude API key not configured")

        model = model or self.model
        payload = {
            "model": model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                ANTHROPIC_API_URL,
                headers=self._headers(),
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data.get("content", [{}])
            text = content[0].get("text", "") if content else ""
            return {
                "response": text,
                "model": model,
                "provider": "claude",
                "usage": data.get("usage"),
            }


claude_service = ClaudeService()
