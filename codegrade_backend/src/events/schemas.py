from pydantic import BaseModel, model_validator
from typing_extensions import Self

from src.events.enums import LIfeCycleEvent
from src.events.handlers.schemas import (
    InidividualSubmissionEventData,
    SessionCreationEventData,
    SessionEndedEventData,
)


class LifeCycleEventData(BaseModel):
    event: LIfeCycleEvent
    external_session_id: str
    event_data: (
        SessionCreationEventData
        | InidividualSubmissionEventData
        | SessionEndedEventData
    )

    @model_validator(mode="after")
    def check_event_type_againt_event_data(self) -> Self:
        """Check that event type matches event data."""
        if self.event == LIfeCycleEvent.SESSION_CREATED:
            if not isinstance(self.event_data, SessionCreationEventData):
                raise ValueError("Event data must be of type SessionCreationEventData.")
        elif self.event == LIfeCycleEvent.INDIVIDUAL_SUBMISSION:
            if not isinstance(self.event_data, InidividualSubmissionEventData):
                raise ValueError(
                    "Event data must be of type InidividualSubmissionEventData."
                )
        elif self.event == LIfeCycleEvent.SESSION_ENDED:
            if not isinstance(self.event_data, SessionEndedEventData):
                raise ValueError("Event data must be of type SessionEndedEventData.")

        return self
