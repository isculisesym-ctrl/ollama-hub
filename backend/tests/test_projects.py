"""Tests for Projects API — CRUD operations"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_projects_empty(client: AsyncClient):
    resp = await client.get("/api/projects")
    assert resp.status_code == 200
    data = resp.json()
    assert data["projects"] == []
    assert data["count"] == 0


@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    resp = await client.post("/api/projects", json={
        "name": "Test Project",
        "description": "A test project",
        "model": "llama3",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "A test project"
    assert data["model"] == "llama3"
    assert data["id"] >= 1


@pytest.mark.asyncio
async def test_create_project_minimal(client: AsyncClient):
    resp = await client.post("/api/projects", json={"name": "Minimal"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Minimal"
    assert data["description"] == ""


@pytest.mark.asyncio
async def test_create_project_validation_empty_name(client: AsyncClient):
    resp = await client.post("/api/projects", json={"name": ""})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient):
    create = await client.post("/api/projects", json={"name": "Get Me"})
    pid = create.json()["id"]

    resp = await client.get(f"/api/projects/{pid}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Get Me"


@pytest.mark.asyncio
async def test_get_project_not_found(client: AsyncClient):
    resp = await client.get("/api/projects/9999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    create = await client.post("/api/projects", json={"name": "Old Name"})
    pid = create.json()["id"]

    resp = await client.put(f"/api/projects/{pid}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


@pytest.mark.asyncio
async def test_update_project_not_found(client: AsyncClient):
    resp = await client.put("/api/projects/9999", json={"name": "Nope"})
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient):
    create = await client.post("/api/projects", json={"name": "Delete Me"})
    pid = create.json()["id"]

    resp = await client.delete(f"/api/projects/{pid}")
    assert resp.status_code == 200

    resp2 = await client.get(f"/api/projects/{pid}")
    assert resp2.status_code == 404


@pytest.mark.asyncio
async def test_delete_project_not_found(client: AsyncClient):
    resp = await client.delete("/api/projects/9999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_projects_after_create(client: AsyncClient):
    await client.post("/api/projects", json={"name": "Project A"})
    await client.post("/api/projects", json={"name": "Project B"})

    resp = await client.get("/api/projects")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 2
