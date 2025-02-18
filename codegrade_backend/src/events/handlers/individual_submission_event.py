from src.events.handlers.base import AbstractLifeCycleEventHandler
from src.events.handlers.shcemas import SessionCreationEventData


class IndividualSubmissionEventHandler(AbstractLifeCycleEventHandler):
    """Handler for individual submission events."""

    def handle_event(
        self,
        external_session_id: str,
        event_data: SessionCreationEventData,
    ) -> None:
        """Handle the event data."""
        pass
