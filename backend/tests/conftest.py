"""Shared test fixtures"""

import pytest
from httpx import AsyncClient, ASGITransport

from app.database import set_db_path, init_db


@pytest.fixture(autouse=True)
def use_test_db(tmp_path):
    db_file = str(tmp_path / "test.db")
    set_db_path(db_file)
    init_db()
    yield
    set_db_path(None)


@pytest.fixture
def client():
    from app.main import app
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture
def mock_ollama_models():
    return {
        "models": [
            {"name": "llama3:latest", "size": 4_000_000_000, "modified_at": "2024-01-01T00:00:00Z"},
            {"name": "mistral:latest", "size": 3_500_000_000, "modified_at": "2024-01-02T00:00:00Z"},
        ]
    }
