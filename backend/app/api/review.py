"""Code review API — Haiku orchestrates Ollama specialists"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.services.review_service import review_service

router = APIRouter()


class CodeReviewRequest(BaseModel):
    code: str
    description: str = ""


@router.post("/review/code")
async def review_code(req: CodeReviewRequest):
    """Haiku + Ollama swarm review code via SSE"""
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code is required")

    async def stream_gen():
        async for chunk_json in review_service.review_code_swarm(req.code, req.description):
            yield f"data: {chunk_json}\n\n"

    return StreamingResponse(stream_gen(), media_type="text/event-stream")
