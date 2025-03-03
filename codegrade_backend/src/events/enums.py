from enum import Enum


class LIfeCycleEvent(Enum):
    """
    Enum for the different types of events that can be triggered in the system.

    Attributes: \n
        SESSION_CREATED: Event triggered when a session is created.
        SESSION_ENDED: Event triggered when a session is ended.
        INDIVIDUAL_SUBMISSION: Event triggered when an individual submission is made before session ends.
        USER_JOINED_SESSION: Event triggered when a user joins a session.
    """

    SESSION_CREATED = "session_created"
    SESSION_ENDED = "session_ended"
    INDIVIDUAL_SUBMISSION = "individual_submission"
    USER_JOINED_SESSION = "user_joined_session"
