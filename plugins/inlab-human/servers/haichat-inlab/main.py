"""HAI-Chat In-Lab Console — a clinical model console you can embed in a thread.

Serves the console SPA, the deterministic prediction REST API, and the HaiChat
agent WebSocket (/ws/haichat — standalone mode only; embedded beside a HAI-Chat
thread the drawer is hidden, *Mattermost is the chat* there and the agent is
haichat-me-agent). This service is the panel that sits beside the conversation
(HAI-Chat renders any URL as a per-thread iframe embed), showing the clinician
the patient, the raw record, the available models, and the endpoint's score.

Run (dev):
    INLAB_PATIENT_STORE=... INLAB_ENDPOINT_STORE=... INLAB_REGISTRY=... \
        uvicorn main:app --port 8091

Docker: see Dockerfile / the haichat-inlab service in docker-compose.yml.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from console_api import router
from haichat_api import router as haichat_router
from labeling_api import router as labeling_router
from message_api import router as message_router
from tasks_api import router as tasks_router

app = FastAPI(title="HAI-Chat In-Lab Console", version="0.1.0")

# The console is embedded cross-origin (a HAI-Chat thread iframe), and in dev the
# SPA is served by Vite on another port.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(haichat_router)
app.include_router(labeling_router)
app.include_router(tasks_router)
app.include_router(message_router)

# Built SPA, if present. Absent in dev (Vite serves it) — don't fail, just say so.
DIST = Path(__file__).parent / "web" / "dist"
if DIST.is_dir():
    # SPA scope routes: /individual and /group are client-side routes owned by the
    # React router — the server just hands back index.html so a refresh (or a
    # bookmarked link) on either one loads the app instead of 404ing. Registered
    # BEFORE the greedy "/" mount so they win.
    _index = DIST / "index.html"

    @app.get("/individual")
    @app.get("/group")
    def _spa_scope():
        return FileResponse(_index)

    app.mount("/", StaticFiles(directory=str(DIST), html=True), name="console")
else:
    @app.get("/")
    def no_build():
        return JSONResponse({
            "error": "console SPA is not built",
            "fix": "cd web && npm install && npm run build",
            "api": "/api/health",
        }, status_code=503)
