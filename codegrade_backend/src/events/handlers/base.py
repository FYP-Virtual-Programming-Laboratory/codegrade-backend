from abc import ABC, abstractmethod
from typing import Any


class AbstractLifeCycleEventHandler(ABC):
    """Abstract base class for lifecycle event handlers."""

    @abstractmethod
    def handle_event(
        self,
        external_session_id: str,
        event_data: dict[str, Any],
    ) -> None:
        """Handle the event data."""
