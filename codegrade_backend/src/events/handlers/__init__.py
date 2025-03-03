from src.events.enums import LIfeCycleEvent

from .base import AbstractLifeCycleEventHandler
from .individual_submission_event import IndividualSubmissionEventHandler
from .session_created_event import SessionCreatedEventHandler
from .session_ended_event import SessionEndedEventHandler
from .user_joined_session_event import UserJoinedSessionEventHandler

MAP: dict[LIfeCycleEvent, type[AbstractLifeCycleEventHandler]] = {
    LIfeCycleEvent.SESSION_CREATED: SessionCreatedEventHandler,
    LIfeCycleEvent.SESSION_ENDED: SessionEndedEventHandler,
    LIfeCycleEvent.INDIVIDUAL_SUBMISSION: IndividualSubmissionEventHandler,
    LIfeCycleEvent.USER_JOINED_SESSION: UserJoinedSessionEventHandler,
}


__all__ = ["MAP"]
