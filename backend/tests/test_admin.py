"""Tests for Admin API — logs, stats"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_stats(client: AsyncClient):
    await client.post("/api/projects", json={"name": "Stats Project"})

    resp = await client.get("/api/admin/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["projects"]["total"] >= 1
    assert "database" in data
    assert "size_mb" in data["database"]
    assert "chats" in data
    assert "daily_activity" in data


@pytest.mark.asyncio
async def test_admin_stats_with_chats(client: AsyncClient):
    from unittest.mock import AsyncMock, patch

    await client.post("/api/projects", json={"name": "Chat Stats"})
    with patch("app.api.chat.ollama_service.generate", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "response": "Hello!",
            "model": "llama3",
            "provider": "ollama",
            "usage": None,
        }
        await client.post("/api/chat", json={
            "message": "Hi",
            "provider": "ollama",
            "project_id": 1,
        })

    resp = await client.get("/api/admin/stats")
    data = resp.json()
    assert data["chats"]["total"] >= 2
    assert "ollama" in data["chats"]["by_provider"]


@pytest.mark.asyncio
async def test_admin_logs(client: AsyncClient):
    resp = await client.get("/api/admin/logs")
    assert resp.status_code == 200
    data = resp.json()
    assert "logs" in data
    assert isinstance(data["logs"], list)


@pytest.mark.asyncio
async def test_admin_logs_with_filters(client: AsyncClient):
    resp = await client.get("/api/admin/logs?limit=10&method=GET")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_admin_log_stats(client: AsyncClient):
    resp = await client.get("/api/admin/logs/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_requests" in data
    assert "methods" in data
    assert "avg_duration_ms" in data
