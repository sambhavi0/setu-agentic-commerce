from fastapi import FastAPI

from app.routes.catalog import router as catalog_router


app = FastAPI(
    title="Setu Agent Commerce API",
    description="Agent-readable commerce interface for Setu",
    version="0.1.0",
)


app.include_router(catalog_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "setu-agent-commerce",
    }