"""Tests for Ollama API — models listing"""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ConnectError, Response, Request


@pytest.mark.asyncio
async def test_list_models(client: AsyncClient, mock_ollama_models):
    with patch("app.api.ollama.ollama_service.list_models", new_callable=AsyncMock) as mock:
        mock.return_value = mock_ollama_models["models"]
        resp = await client.get("/api/models")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == 2
        assert data["models"][0]["name"] == "llama3:latest"


@pytest.mark.asyncio
async def test_list_models_empty(client: AsyncClient):
    with patch("app.api.ollama.ollama_service.list_models", new_callable=AsyncMock) as mock:
        mock.return_value = []
        resp = await client.get("/api/models")
        assert resp.status_code == 200
        assert resp.json()["count"] == 0


@pytest.mark.asyncio
async def test_list_models_ollama_offline(client: AsyncClient):
    with patch("app.api.ollama.ollama_service.list_models", new_callable=AsyncMock) as mock:
        mock.side_effect = ConnectError("Connection refused")
        resp = await client.get("/api/models")
        assert resp.status_code == 503


@pytest.mark.asyncio
async def test_get_model_info(client: AsyncClient):
    model_info = {"modelfile": "FROM llama3", "parameters": "temperature 0.7"}
    with patch("app.api.ollama.ollama_service.get_model_info", new_callable=AsyncMock) as mock:
        mock.return_value = model_info
        resp = await client.get("/api/models/llama3")
        assert resp.status_code == 200
        assert resp.json()["modelfile"] == "FROM llama3"


@pytest.mark.asyncio
async def test_test_ollama_running(client: AsyncClient):
    with patch("app.api.ollama.ollama_service.health_check", new_callable=AsyncMock) as mock:
        mock.return_value = {"status": "running", "url": "http://127.0.0.1:11434"}
        resp = await client.post("/api/ollama/test")
        assert resp.status_code == 200
        assert resp.json()["status"] == "running"


@pytest.mark.asyncio
async def test_test_ollama_offline(client: AsyncClient):
    with patch("app.api.ollama.ollama_service.health_check", new_callable=AsyncMock) as mock:
        mock.return_value = {"status": "offline", "detail": "Cannot connect"}
        resp = await client.post("/api/ollama/test")
        assert resp.status_code == 503
