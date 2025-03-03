from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlmodel import col, select

from src.enums import SubmissionStatus
from src.events.handlers.base import AbstractLifeCycleEventHandler
from src.events.handlers.schemas import SessionEndedEventData
from src.log import logger
from src.models import Session, Submission, User


class SessionEndedEventHandler(AbstractLifeCycleEventHandler):
    """Handler for session ended events."""

    def _get_session(self, external_session_id: str) -> Session:
        """Get the session."""
        return self.db_session.exec(
            select(Session).where(
                Session.external_id == external_session_id,
                Session.is_active == True,  # Only active sessions are considered
            )
        ).one()

    def _collect_user_submissions(self, session: Session) -> list[Submission]:
        """Collect user submissions."""

        user_that_have_not_submitted = self.db_session.exec(
            select(User).where(
                User.session_id == session.id,
                col(User.id).notin_(
                    select(Submission.user_id).where(
                        Submission.session_id == session.id,
                    )
                ),
            )
        )

        # create submission for users that have not submitted
        submissions = [
            Submission(
                user_id=user.id,
                session_id=session.id,
                status=SubmissionStatus.QUEUED,
                group_id=user.group_id,
                total_score=None,
            )
            for user in user_that_have_not_submitted
        ]

        self.db_session.add_all(submissions)
        self.db_session.commit()
        return submissions

    def _send_submissions_to_grading_queue(
        self, submissions: Sequence[Submission]
    ) -> None:
        """Send submissions to grading queue."""
        pass

    def _deactivate_session(self, session: Session) -> None:
        """Deactivate session."""
        session.is_active = False
        self.db_session.add(session)
        self.db_session.commit()

    def handle_event(
        self,
        external_session_id: str,
        event_data: SessionEndedEventData,  # type: ignore
    ) -> None:
        """Handle the event data."""

        try:
            session = self._get_session(external_session_id)
            user_submissions = self._collect_user_submissions(session)
            self._send_submissions_to_grading_queue(user_submissions)

            # deactivate the session once all submissions have been sent to the grading queue.
            # to ensure that we cant take any more lifecycle events for this session
            self._deactivate_session(session)
        except NoResultFound as error:
            self.db_session.rollback()
            logger.error(
                "src:events:handlers:session_ended_event_handler:: No result found for session",
                extra={"external_session_id": external_session_id, "error": str(error)},
            )
