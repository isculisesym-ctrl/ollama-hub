"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    model: str = Field(default="")
    system_prompt: str = Field(default="", max_length=10000)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    model: Optional[str] = None
    system_prompt: Optional[str] = Field(default=None, max_length=10000)


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    model: str
    system_prompt: str
    created_at: str
    updated_at: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=50000)
    model: Optional[str] = None
    provider: str = Field(default="ollama", pattern="^(ollama|claude)$")
    project_id: Optional[int] = None
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    model: str
    provider: str
    usage: Optional[dict] = None


class ChatMessage(BaseModel):
    id: int
    project_id: Optional[int]
    role: str
    content: str
    model: str
    provider: str
    created_at: str


class StatusResponse(BaseModel):
    ollama: dict
    claude: dict
    system: dict


class ModelInfo(BaseModel):
    name: str
    size: Optional[str] = None
    modified_at: Optional[str] = None
    digest: Optional[str] = None
    details: Optional[dict] = None
