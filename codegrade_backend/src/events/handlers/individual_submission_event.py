from typing import Any

from src.events.handlers.base import AbstractLifeCycleEventHandler


class IndividualSubmissionEventHandler(AbstractLifeCycleEventHandler):
    """Handler for individual submission events."""

    def handle_event(
        self,
        external_session_id: str,
        event_data: dict[str, Any],
    ) -> None:
        """Handle the event data."""
        pass
