"""Projects API endpoints — full CRUD"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import project_service

router = APIRouter()


@router.get("/projects")
async def list_projects():
    projects = project_service.list_projects()
    return {"projects": projects, "count": len(projects)}


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    project = project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/projects", response_model=ProjectResponse, status_code=201)
async def create_project(req: ProjectCreate):
    project = project_service.create_project(
        name=req.name,
        description=req.description,
        model=req.model,
        system_prompt=req.system_prompt,
    )
    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, req: ProjectUpdate):
    project = project_service.update_project(
        project_id,
        name=req.name,
        description=req.description,
        model=req.model,
        system_prompt=req.system_prompt,
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    deleted = project_service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted"}
