from typing import Any

from src.events.handlers.base import AbstractLifeCycleEventHandler


class SessionCreatedEventHandler(AbstractLifeCycleEventHandler):
    """Handler for session created events."""

    def handle_event(
        self,
        external_session_id: str,
        event_data: dict[str, Any],
    ) -> None:
        """Handle the event data."""
