"""Tests for Status API — health checks"""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_status_endpoint(client: AsyncClient):
    with patch("app.api.status.ollama_service.health_check", new_callable=AsyncMock) as mock_ollama, \
         patch("app.api.status.claude_service.health_check", new_callable=AsyncMock) as mock_claude:
        mock_ollama.return_value = {"status": "running", "url": "http://127.0.0.1:11434"}
        mock_claude.return_value = {"status": "connected", "model": "claude-opus-4-8"}

        resp = await client.get("/api/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ollama"]["status"] == "running"
        assert data["claude"]["status"] == "connected"
        assert "cpu_percent" in data["system"]
        assert "memory_used_percent" in data["system"]


@pytest.mark.asyncio
async def test_status_ollama_offline(client: AsyncClient):
    with patch("app.api.status.ollama_service.health_check", new_callable=AsyncMock) as mock_ollama, \
         patch("app.api.status.claude_service.health_check", new_callable=AsyncMock) as mock_claude:
        mock_ollama.return_value = {"status": "offline", "detail": "Cannot connect"}
        mock_claude.return_value = {"status": "not_configured", "detail": "API key not set"}

        resp = await client.get("/api/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ollama"]["status"] == "offline"
        assert data["claude"]["status"] == "not_configured"


@pytest.mark.asyncio
async def test_ollama_status_endpoint(client: AsyncClient):
    with patch("app.api.status.ollama_service.health_check", new_callable=AsyncMock) as mock:
        mock.return_value = {"status": "running", "url": "http://127.0.0.1:11434"}
        resp = await client.get("/api/status/ollama")
        assert resp.status_code == 200
        assert resp.json()["status"] == "running"


@pytest.mark.asyncio
async def test_claude_status_endpoint(client: AsyncClient):
    with patch("app.api.status.claude_service.health_check", new_callable=AsyncMock) as mock:
        mock.return_value = {"status": "connected", "model": "claude-opus-4-8"}
        resp = await client.get("/api/status/claude")
        assert resp.status_code == 200
        assert resp.json()["status"] == "connected"
