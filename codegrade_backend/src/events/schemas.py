from pydantic import BaseModel

from src.events.enums import LIfeCycleEvent
from src.events.handlers.shcemas import (
    InidividualSubmissionEventData,
    SessionCreationEventData,
)


class LifeCycleEventData(BaseModel):
    event: LIfeCycleEvent
    external_session_id: str
    event_data: SessionCreationEventData | InidividualSubmissionEventData
