"""
Enterprise Kirana AI Forecasting Platform - Main Application
Production-ready FastAPI backend with CORS, health checks, and static serving.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from api.routes import router

app = FastAPI(
    title="Kirana AI Platform",
    description="Enterprise AI Forecasting Platform for Indian Kirana Stores",
    version="1.0.0",
)

# CORS - Allow all origins in dev, restrict in production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Serve frontend static files if they exist (for single-container deployment)
frontend_dist = Path(__file__).parent / "static"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend SPA - fallback to index.html for client-side routing."""
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(frontend_dist / "index.html"))
