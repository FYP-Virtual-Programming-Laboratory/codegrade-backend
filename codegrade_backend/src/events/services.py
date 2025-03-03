from typing import Annotated

from fastapi import Body, Path

from src.events.schemas import LifeCycleEventData
from src.events.tasks import lifecycle_event_handler_task


def event_handler(event_data: Annotated[LifeCycleEventData, Body(...)]) -> None:
    """Handle the event data."""
    lifecycle_event_handler_task.delay(event_data.model_dump(mode="json"))
