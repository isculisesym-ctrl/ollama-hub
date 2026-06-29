"""Chat API endpoints — send messages via Ollama or Claude"""

from fastapi import APIRouter, HTTPException
import httpx

from app.models.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import ollama_service
from app.services.claude_service import claude_service
from app.services.project_service import project_service
from app.utils import validate_message

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    message = validate_message(req.message)
    project_service.save_chat_message(
        project_id=req.project_id,
        role="user",
        content=message,
        model=req.model or "",
        provider=req.provider,
    )

    try:
        if req.provider == "claude":
            result = await claude_service.generate(
                prompt=message,
                model=req.model,
                system=req.system_prompt,
            )
        else:
            result = await ollama_service.generate(
                prompt=message,
                model=req.model,
                system=req.system_prompt,
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"{req.provider} server is not reachable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"{req.provider} API error")

    project_service.save_chat_message(
        project_id=req.project_id,
        role="assistant",
        content=result["response"],
        model=result["model"],
        provider=result["provider"],
    )

    return ChatResponse(**result)


@router.get("/chat/history/{project_id}")
async def get_chat_history(project_id: int):
    proj = project_service.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    messages = project_service.get_project_chats(project_id)
    return {"project_id": project_id, "messages": messages, "count": len(messages)}
