from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from src.core.dependecies import require_db_session
from src.worker import celery

router = APIRouter()


class HealthCheckResponse(BaseModel):
    status: Literal["ok", "error"]
    worker_status: Literal["ok", "error"]
    database_status: Literal["ok", "error"]


@router.get("/health-check/", tags=["health_check"])
def health_check(
    db_session: Annotated[Session, Depends(require_db_session)],
) -> HealthCheckResponse:
    return HealthCheckResponse(
        status="ok",
        database_status=db_session.is_active and "ok" or "error",
        worker_status=celery.control.inspect().ping() and "ok" or "error",
    )
