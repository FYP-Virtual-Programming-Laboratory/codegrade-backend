from src.events.handlers.base import AbstractLifeCycleEventHandler
from src.events.handlers.shcemas import SessionCreationEventData


class SessionEndedEventHandler(AbstractLifeCycleEventHandler):
    """Handler for session ended events."""

    def handle_event(
        self,
        external_session_id: str,
        event_data: SessionCreationEventData,
    ) -> None:
        """Handle the event data."""
        pass
