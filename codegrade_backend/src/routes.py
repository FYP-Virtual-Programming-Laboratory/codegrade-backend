from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from src.core.dependecies import require_db_session
from src.events.api.routes import router as events_router
from src.grading.routers import router as grading_routers
from src.worker import celery_app

router = APIRouter()
router.include_router(events_router, prefix="/events", tags=["events"])
router.include_router(grading_routers, prefix="/grading", tags=["grading"])


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
        worker_status=celery_app.control.inspect().ping() and "ok" or "error",
    )
