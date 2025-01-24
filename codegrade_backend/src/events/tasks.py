from typing import Any

from pydantic import ValidationError

from src.events.handlers import MAP
from src.events.schemas import LifeCycleEventData
from src.log import logger
from src.worker import celery_app


@celery_app.task(name="lifecycle_event_handler_task")
def lifecycle_event_handler_task(serialized_event_data: Any) -> None:
    """Handle the lifecycle events in background."""

    try:
        event_data = LifeCycleEventData.model_validate(serialized_event_data)
        handler = MAP[event_data.event]
    except ValidationError as error:
        logger.error(
            "src:events:tasks:lifecycle_event_handler_task:: Failed to validate event data",
            extra={
                "serialized_event_data": serialized_event_data,
                "validation_error": error.json(),
            },
        )
        return
    except KeyError as error:
        logger.error(
            f"src:events:tasks:lifecycle_event_handler_task:: Unhandled event: {error}",
            extra={"serialized_event_data": serialized_event_data},
        )
        return

    handler.handle_event(
        external_session_id=event_data.external_session_id,
        event_data=event_data.event_data,
    )
