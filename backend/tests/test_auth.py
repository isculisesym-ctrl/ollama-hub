"""Tests for API key authentication"""

import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_disabled_allows_all(client: AsyncClient):
    """With AUTH_ENABLED=False, protected endpoints work without a key"""
    with patch("app.api.admin.get_logs", return_value=[]):
        resp = await client.get("/api/admin/logs")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_auth_enabled_rejects_missing_key(client: AsyncClient):
    with patch("app.auth.settings") as mock_settings:
        mock_settings.AUTH_ENABLED = True
        mock_settings.API_KEY = "test-secret-key-12345"
        resp = await client.get("/api/admin/logs")
        assert resp.status_code == 401
        assert "Missing API key" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_auth_enabled_rejects_wrong_key(client: AsyncClient):
    with patch("app.auth.settings") as mock_settings:
        mock_settings.AUTH_ENABLED = True
        mock_settings.API_KEY = "test-secret-key-12345"
        resp = await client.get(
            "/api/admin/logs",
            headers={"X-API-Key": "wrong-key-00000"},
        )
        assert resp.status_code == 401
        assert "Invalid API key" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_auth_enabled_accepts_correct_key(client: AsyncClient):
    with patch("app.auth.settings") as mock_settings:
        mock_settings.AUTH_ENABLED = True
        mock_settings.API_KEY = "test-secret-key-12345"
        resp = await client.get(
            "/api/admin/logs",
            headers={"X-API-Key": "test-secret-key-12345"},
        )
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_auth_status_endpoint(client: AsyncClient):
    resp = await client.get("/api/admin/auth/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "auth_enabled" in data
    assert "api_key_set" in data


@pytest.mark.asyncio
async def test_public_endpoints_not_affected(client: AsyncClient):
    """Status and health endpoints should never require auth"""
    with patch("app.auth.settings") as mock_settings:
        mock_settings.AUTH_ENABLED = True
        mock_settings.API_KEY = "test-secret-key-12345"
        resp = await client.get("/health")
        assert resp.status_code == 200
