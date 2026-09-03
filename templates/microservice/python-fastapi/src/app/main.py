from fastapi import FastAPI

from app.api.orders import router as orders_router


app = FastAPI(title="__PROJECT_NAME__", version="0.1.0")
app.include_router(orders_router, prefix="/api/v1")


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["operations"])
def ready() -> dict[str, str]:
    return {"status": "ready"}