from typing import Any

from pydantic import UUID4, ValidationError
from sqlmodel import Session

from src.core.config import settings
from src.core.db import engine
from src.events.handlers import MAP
from src.events.schemas import LifeCycleEventData
from src.log import logger
from src.worker import celery_app


@celery_app.task(name="lifecycle_event_handler_task")
def lifecycle_event_handler_task(serialized_event_data: Any) -> None:
    """Handle the lifecycle events in background."""

    try:
        with Session(engine) as session:
            event_data = LifeCycleEventData.model_validate(serialized_event_data)
            handler = MAP[event_data.event](db_session=session)
            handler.handle_event(
                external_session_id=event_data.external_session_id,
                event_data=event_data.event_data,
            )
    except ValidationError as error:
        logger.info(str(error))
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
    except Exception as error:
        session.rollback()  # ensure process is atomic
        logger.error(
            "src:events:tasks:lifecycle_event_handler_task:: Failed to handle event",
            extra={"serialized_event_data": serialized_event_data, "error": str(error)},
        )
        raise error


@celery_app.task(
    name="grading_user_submission_task", queue=settings.CELERY_GRADING_QUEUE
)
def grading_user_submission_task(submission_id: UUID4) -> None:
    """Grade a users submission."""

    # get the users submissin
    # ensure that the state of the submission is queud
    # for each test case send a request to codelab to excute the exercise with the required test case
    # compare results and complete grading.

