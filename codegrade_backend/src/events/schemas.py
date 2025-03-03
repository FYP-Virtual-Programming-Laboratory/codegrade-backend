from pydantic import BaseModel, PositiveFloat, model_validator
from src.enums import EvaluationFlagEnum, SubmissionStatus
from typing_extensions import Self

import uuid
from src.events.enums import LIfeCycleEvent
from src.events.handlers.schemas import (
    UserJoinedSessionEventData,
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
        | UserJoinedSessionEventData
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
        
        elif self.event == LIfeCycleEvent.USER_JOINED_SESSION:
            if not isinstance(self.event_data, UserJoinedSessionEventData):
                raise ValueError("Event data must be of type UserJoinedSessionEventData.")

        return self
