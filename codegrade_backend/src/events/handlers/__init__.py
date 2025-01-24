from src.events.enums import LIfeCycleEvent

from .base import AbstractLifeCycleEventHandler
from .individual_submission_event import IndividualSubmissionEventHandler
from .session_created_event import SessionCreatedEventHandler
from .session_ended_event import SessionEndedEventHandler

MAP: dict[LIfeCycleEvent, AbstractLifeCycleEventHandler] = {
    LIfeCycleEvent.SESSION_CREATED: SessionCreatedEventHandler(),
    LIfeCycleEvent.SESSION_ENDED: SessionEndedEventHandler(),
    LIfeCycleEvent.INDIVIDUAL_SUBMISSION: IndividualSubmissionEventHandler(),
}


__all__ = ["MAP"]
