
from fastapi import APIRouter

from app.schemas.health import HealthResponse


router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        service="identity-service",
        status="ok",
        version="1.0.0"
    )
