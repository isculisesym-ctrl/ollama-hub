"""Tests for Model Manager — pull and delete"""

import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ConnectError, Response, Request


@pytest.mark.asyncio
async def test_pull_model_streams(client: AsyncClient):
    async def fake_pull(model_name):
        lines = [
            json.dumps({"status": "pulling manifest"}),
            json.dumps({"status": "downloading", "completed": 50, "total": 100}),
            json.dumps({"status": "success"}),
        ]
        for line in lines:
            yield line

    with patch("app.api.ollama.ollama_service.pull_model", side_effect=fake_pull):
        resp = await client.post("/api/models/pull", json={"name": "llama3"})
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("content-type", "")
        assert "pulling manifest" in resp.text


@pytest.mark.asyncio
async def test_pull_model_empty_name(client: AsyncClient):
    resp = await client.post("/api/models/pull", json={"name": ""})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_pull_model_missing_name(client: AsyncClient):
    resp = await client.post("/api/models/pull", json={})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_delete_model(client: AsyncClient):
    with patch("app.api.ollama.ollama_service.delete_model", new_callable=AsyncMock) as mock:
        mock.return_value = {"status": "deleted", "model": "llama3"}
        resp = await client.delete("/api/models/llama3")
        assert resp.status_code == 200
        assert resp.json()["status"] == "deleted"


@pytest.mark.asyncio
async def test_delete_model_not_found(client: AsyncClient):
    from httpx import HTTPStatusError
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_req = MagicMock()
    with patch("app.api.ollama.ollama_service.delete_model", new_callable=AsyncMock) as mock:
        mock.side_effect = HTTPStatusError("not found", request=mock_req, response=mock_resp)
        resp = await client.delete("/api/models/nonexistent")
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_model_ollama_offline(client: AsyncClient):
    with patch("app.api.ollama.ollama_service.delete_model", new_callable=AsyncMock) as mock:
        mock.side_effect = ConnectError("Connection refused")
        resp = await client.delete("/api/models/llama3")
        assert resp.status_code == 503
