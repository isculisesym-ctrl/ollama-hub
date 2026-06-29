"""Tests for service layer — direct unit tests"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from app.services.ollama_service import OllamaService
from app.services.claude_service import ClaudeService
from app.services.project_service import ProjectService


class TestOllamaService:
    @pytest.mark.asyncio
    async def test_health_check_running(self):
        svc = OllamaService(base_url="http://localhost:11434")
        mock_resp = MagicMock(status_code=200)
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
            result = await svc.health_check()
            assert result["status"] == "running"

    @pytest.mark.asyncio
    async def test_health_check_offline(self):
        svc = OllamaService(base_url="http://localhost:11434")
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, side_effect=httpx.ConnectError("refused")):
            result = await svc.health_check()
            assert result["status"] == "offline"

    @pytest.mark.asyncio
    async def test_health_check_error_status(self):
        svc = OllamaService(base_url="http://localhost:11434")
        mock_resp = MagicMock(status_code=500)
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
            result = await svc.health_check()
            assert result["status"] == "error"


class TestClaudeService:
    @pytest.mark.asyncio
    async def test_health_check_no_key(self):
        svc = ClaudeService(api_key="")
        result = await svc.health_check()
        assert result["status"] == "not_configured"

    @pytest.mark.asyncio
    async def test_generate_no_key_raises(self):
        svc = ClaudeService(api_key="")
        with pytest.raises(ValueError, match="not configured"):
            await svc.generate("hello")


class TestProjectService:
    def test_create_and_get(self):
        svc = ProjectService()
        project = svc.create_project(name="Test", description="desc", model="llama3")
        assert project["name"] == "Test"
        assert project["model"] == "llama3"

        fetched = svc.get_project(project["id"])
        assert fetched["name"] == "Test"

    def test_update_partial(self):
        svc = ProjectService()
        project = svc.create_project(name="Original", description="original desc")
        updated = svc.update_project(project["id"], description="new desc")
        assert updated["name"] == "Original"
        assert updated["description"] == "new desc"

    def test_update_no_fields(self):
        svc = ProjectService()
        project = svc.create_project(name="Stable")
        result = svc.update_project(project["id"])
        assert result["name"] == "Stable"

    def test_save_and_get_chats(self):
        svc = ProjectService()
        project = svc.create_project(name="Chat Project")
        svc.save_chat_message(project["id"], "user", "Hello", "llama3", "ollama")
        svc.save_chat_message(project["id"], "assistant", "Hi there", "llama3", "ollama")
        chats = svc.get_project_chats(project["id"])
        assert len(chats) == 2
        assert chats[0]["role"] == "user"
        assert chats[1]["role"] == "assistant"
