from sqlalchemy.exc import NoResultFound
from sqlmodel import or_, select

from src.enums import SubmissionStatus
from src.events.handlers.base import AbstractLifeCycleEventHandler
from src.events.handlers.shcemas import InidividualSubmissionEventData
from src.log import logger
from src.models import (
    Exercise,
    ExerciseSubmission,
    Session,
    StudentGroup,
    Submission,
    User,
)


class IndividualSubmissionEventHandler(AbstractLifeCycleEventHandler):
    """Handler for individual submission events."""

    def _get_session(self, external_session_id: str) -> Session:
        """Get the session."""
        return self.db_session.exec(
            select(Session).where(Session.external_id == external_session_id)
        ).one()

    def _get_student_group(
        self, session: Session, external_group_id: str
    ) -> StudentGroup:
        """Get the student group."""
        return self.db_session.exec(
            select(StudentGroup).where(
                StudentGroup.session_id == session.id,
                StudentGroup.external_id == external_group_id,
            )
        ).one()

    def _get_user(self, session: Session, external_user_id: str) -> User:
        """Get the user."""
        return self.db_session.exec(
            select(User).where(
                User.session_id == session.id,
                User.external_id == external_user_id,
            )
        ).one()

    def _create_submission(
        self,
        session: Session,
        user: User | None,
        group: StudentGroup | None,
        event_data: InidividualSubmissionEventData,
    ) -> Submission | None:
        """Create the submission."""

        submission = self.db_session.exec(
            select(Submission)
            .where(Submission.session_id == session.id)
            .where(
                or_(
                    Submission.user_id == (user.id if user else None),
                    Submission.group_id == (group.id if group else None),
                )
            )
        ).first()

        if submission:
            return None

        submission = Submission(
            session_id=session.id,
            user_id=user.id if user else None,
            status=SubmissionStatus.QUEUED,
            total_score=None,
            group_id=group.id if group else None,
        )

        # selected the excersises the user submitted
        submitted_excersises = self.db_session.exec(
            select(Exercise).where(
                Exercise.external_id.in_(event_data.external_exercise_ids)  # type: ignore
            )
        ).all()

        # created excersise submission to indicate the execersise the user submitted
        exercise_submissions = [
            ExerciseSubmission(
                submission_id=submission.id,
                exercise_id=exercise.id,
            )
            for exercise in submitted_excersises
        ]

        self.db_session.add_all([submission, *exercise_submissions])
        self.db_session.commit()
        return submission

    def handle_event(
        self,
        external_session_id: str,
        event_data: InidividualSubmissionEventData,  # type: ignore
    ) -> None:
        """Handle the event data."""

        try:
            session = self._get_session(external_session_id)

            group = None
            user = None

            if event_data.external_group_id:
                group = self._get_student_group(session, event_data.external_group_id)

            if event_data.external_student_id:
                user = self._get_user(session, event_data.external_student_id)

            submission = self._create_submission(session, user, group, event_data)

            if submission:
                # TODO: send the submission into grading queue.
                pass
        except NoResultFound as error:
            self.db_session.rollback()
            logger.error(
                "src:events:handlers:individual_submission_event_handler:: No result found for session or user or group",
                extra={"external_session_id": external_session_id, "error": str(error)},
            )
