from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.catalog import router as catalog_router
from app.routes.agent import router as agent_router

app = FastAPI(
    title="Setu Agent Commerce API",
    description="Agent-readable commerce interface for Setu",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalog_router)
app.include_router(agent_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "setu-agent-commerce",
    }