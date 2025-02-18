from celery import Celery, Task
from celery.signals import task_postrun, task_prerun

from src.core.config import settings
from src.log import logger as main_logger

celery_app = Celery(__name__, include=["src.worker", "src.events.tasks"])
celery_app.conf.broker_url = settings.CELERY_BROKER_URL
celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery_app.conf.task_default_queue = settings.CELERY_DEFAULT_QUEUE


@task_prerun.connect
def _log_task_before_run(task_id: str, task: Task, *args, **kwargs) -> None:  # type: ignore  # noqa
    """Log task before it runs."""
    main_logger.info(f"Stating task: {task.name}")


@task_postrun.connect
def _log_task_after_run(task_id: str, task: Task, *args, **kwargs) -> None:  # type: ignore  # noqa
    """Log task after it runs."""
    main_logger.info(f"Task {task.name} finished")
