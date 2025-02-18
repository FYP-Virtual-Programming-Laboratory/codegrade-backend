from src.events.handlers.base import AbstractLifeCycleEventHandler
from src.events.handlers.shcemas import (
    GroupCreationSchema,
    SessionCreationEventData,
    UserCreationSchema,
)
from src.models import Exercise, Session, StudentGroup, TestCase, User


class SessionCreatedEventHandler(AbstractLifeCycleEventHandler):
    """Handler for session created events."""

    def _create_session(
        self,
        external_session_id: str,
        event_data: SessionCreationEventData,
    ) -> Session:
        """Create a new session."""
        session = Session(
            external_id=external_session_id,
            title=event_data.session_title,
            description=event_data.session_description,
            is_active=True,
        )

        self.db_session.add(session)
        self.db_session.commit()
        self.db_session.refresh(session)
        return session

    def _create_exercise(
        self, session: Session, event_data: SessionCreationEventData
    ) -> None:
        """Create exercises and its associated test cases."""
        for exercise in event_data.exercises:
            exercise_record = Exercise(
                external_id=exercise.external_id,
                session_id=session.id,
                title=exercise.title,
                question=exercise.question,
                instructions=exercise.instructions,
                difficulty=exercise.difficulty,
                status=exercise.status,
                max_score=exercise.score,
            )

            test_cases = [
                TestCase(
                    external_id=test_case.external_id,
                    exercise_id=exercise_record.id,
                    test_input=test_case.test_input,
                    expected_output=test_case.expected_output,
                    percentage_score=test_case.percentage_score,
                    max_score=test_case.max_score,
                )
                for test_case in exercise.test_cases
            ]

            self.db_session.add_all([exercise_record, *test_cases])

        self.db_session.commit()

    def _create_users(
        self,
        session: Session,
        user_data: list[UserCreationSchema],
        group: StudentGroup | None = None,
    ) -> list[User]:
        """Create new users."""
        users = [
            User(
                external_id=user.external_id,
                session_id=session.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                group_id=group.id if group else None,
            )
            for user in user_data
        ]

        self.db_session.add_all(users)
        self.db_session.commit()
        return users

    def _create_groups(
        self,
        session: Session,
        group_data: list[GroupCreationSchema],
    ) -> None:
        """Create new groups."""
        for group in group_data:
            group_record = StudentGroup(
                external_id=group.external_id,
                session_id=session.id,
                group_title=group.group_title,
            )

            users = self._create_users(
                session=session,
                user_data=group.students,
                group=group_record,
            )
            self.db_session.add_all([group_record, *users])

        self.db_session.commit()

    def handle_event(
        self,
        external_session_id: str,
        event_data: SessionCreationEventData,  # type: ignore
    ) -> None:
        """Handle the event data."""

        # first create the session
        session = self._create_session(external_session_id, event_data)

        # create excesises and their associated test cases
        self._create_exercise(session, event_data)

        # finally create all users and groups
        if event_data.students:
            self._create_users(session, event_data.students)

        if event_data.groups:
            self._create_groups(session, event_data.groups)
