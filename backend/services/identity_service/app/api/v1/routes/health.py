
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.health import (
    HealthResponse,
    DatabaseHealthResponse,
)


router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        service="identity-service",
        status="ok",
        version="1.0.0",
    )


@router.get(
    "/health/db",
    response_model=DatabaseHealthResponse,
)
def database_health(
    db: Session = Depends(get_db),
) -> DatabaseHealthResponse:
    try:
        db.execute(text("SELECT 1"))

        return DatabaseHealthResponse(
            database="connected"
        )

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from exc
