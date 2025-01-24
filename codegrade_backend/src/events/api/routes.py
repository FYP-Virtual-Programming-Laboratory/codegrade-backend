from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.dependecies import require_authenticated_service
from src.events.services import event_handler

router = APIRouter()


@router.post("/lifecycle/", dependencies=[Depends(require_authenticated_service)])
def execute_lifecycle_event(
    _: Annotated[None, Depends(event_handler)],
) -> dict[str, str]:
    """Execute the lifecycle event."""
    return {"message": "Lifecycle event executed"}
