"""Tests for Chat API — send messages and history"""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ConnectError


@pytest.mark.asyncio
async def test_chat_ollama(client: AsyncClient):
    await client.post("/api/projects", json={"name": "Chat Project"})

    with patch("app.api.chat.ollama_service.generate", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "response": "Hello from Ollama!",
            "model": "llama3",
            "provider": "ollama",
            "usage": {"total_duration": 1000, "eval_count": 10},
        }
        resp = await client.post("/api/chat", json={
            "message": "Hello",
            "provider": "ollama",
            "project_id": 1,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["response"] == "Hello from Ollama!"
        assert data["provider"] == "ollama"


@pytest.mark.asyncio
async def test_chat_claude(client: AsyncClient):
    with patch("app.api.chat.claude_service.generate", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "response": "Hello from Claude!",
            "model": "claude-opus-4-8",
            "provider": "claude",
            "usage": {"input_tokens": 5, "output_tokens": 10},
        }
        resp = await client.post("/api/chat", json={
            "message": "Hello",
            "provider": "claude",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["response"] == "Hello from Claude!"
        assert data["provider"] == "claude"


@pytest.mark.asyncio
async def test_chat_validation_empty_message(client: AsyncClient):
    resp = await client.post("/api/chat", json={
        "message": "",
        "provider": "ollama",
    })
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_chat_validation_invalid_provider(client: AsyncClient):
    resp = await client.post("/api/chat", json={
        "message": "Hello",
        "provider": "openai",
    })
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_chat_ollama_offline(client: AsyncClient):
    with patch("app.api.chat.ollama_service.generate", new_callable=AsyncMock) as mock:
        mock.side_effect = ConnectError("Connection refused")
        resp = await client.post("/api/chat", json={
            "message": "Hello",
            "provider": "ollama",
        })
        assert resp.status_code == 503


@pytest.mark.asyncio
async def test_chat_history(client: AsyncClient):
    await client.post("/api/projects", json={"name": "History Project"})

    with patch("app.api.chat.ollama_service.generate", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "response": "Response 1",
            "model": "llama3",
            "provider": "ollama",
            "usage": None,
        }
        await client.post("/api/chat", json={
            "message": "Message 1",
            "provider": "ollama",
            "project_id": 1,
        })

    resp = await client.get("/api/chat/history/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 2  # user + assistant


@pytest.mark.asyncio
async def test_chat_history_not_found(client: AsyncClient):
    resp = await client.get("/api/chat/history/9999")
    assert resp.status_code == 404
