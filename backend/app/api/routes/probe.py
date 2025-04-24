from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from core.db import async_engine

router = APIRouter()


@router.get("/liveliness", tags=["probe"])
def liveliness():
    return {"status": "alive"}


@router.get("/readiness", tags=["probe"])
async def readiness():
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Readiness check failed: database unreachable"
        )
    return {"status": "ready"}


@router.get("/health", tags=["probe"])
async def health():
    results = {"session": False}
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            results["session"] = True
    except Exception:
        pass

    if not all(results.values()):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail={"status": "unhealthy", **results}
        )
    return {"status": "healthy", **results}
    return {"status": "healthy", **results}
