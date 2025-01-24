from typing import Any

from pydantic import BaseModel

from src.events.enums import LIfeCycleEvent


class LifeCycleEventData(BaseModel):
    event: LIfeCycleEvent
    external_session_id: str

    # This is a JSON object that can be used to store
    # any additional data that needs to be sent with the event.
    # This will be replaced with more specific types in the future.
    event_data: dict[str, Any]
