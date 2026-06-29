"""OllamaHub FastAPI Application"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.logging_middleware import RequestLoggingMiddleware
from app.api import status, ollama, claude, chat, projects, admin, review, simple_test


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


# Create FastAPI app
app = FastAPI(
    title="OllamaHub API",
    description="Professional IDE for Local LLMs + Claude Integration",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Include routers
app.include_router(status.router, prefix="/api", tags=["Status"])
app.include_router(ollama.router, prefix="/api", tags=["Ollama"])
app.include_router(claude.router, prefix="/api", tags=["Claude"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(projects.router, prefix="/api", tags=["Projects"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])
app.include_router(review.router, prefix="/api", tags=["Review"])
app.include_router(simple_test.router, prefix="/api", tags=["Test"])

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to OllamaHub API",
        "docs": "/api/docs",
        "version": "0.1.0",
    }

# Health check
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
