from sqlmodel import select

from src.models import (
    Exercise,
    ExerciseSubmission,
    Session,
    StudentGroup,
    Submission,
    TestCase,
    TestCaseResult,
    User,
)
from src.tests.factories import (
    ExerciseFactory,
    ExerciseSubmissionFactory,
    SessionFactory,
    StudentGroupFactory,
    SubmissionFactory,
    TestCaseFactory,
    TestCaseResultFactory,
    UserFactory,
)
from src.tests.utils import CustomTestCase


class SessionTests(CustomTestCase):
    def test_model(self) -> None:
        session = SessionFactory()
        records = self.session.exec(select(Session)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], session)


class StudentGroupTests(CustomTestCase):
    def test_model(self) -> None:
        student_group = StudentGroupFactory()
        records = self.session.exec(select(StudentGroup)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], student_group)


class UserTests(CustomTestCase):
    def test_model(self) -> None:
        user = UserFactory()
        records = self.session.exec(select(User)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], user)


class ExerciseTests(CustomTestCase):
    def test_model(self) -> None:
        exercise = ExerciseFactory()
        records = self.session.exec(select(Exercise)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], exercise)


class TestCaseTests(CustomTestCase):
    def test_model(self) -> None:
        test_case = TestCaseFactory()
        records = self.session.exec(select(TestCase)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], test_case)


class SubmissionTests(CustomTestCase):
    def test_model(self) -> None:
        submission = SubmissionFactory()
        records = self.session.exec(select(Submission)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], submission)


class ExerciseSubmissionTests(CustomTestCase):
    def test_model(self) -> None:
        exercise_submission = ExerciseSubmissionFactory()
        records = self.session.exec(select(ExerciseSubmission)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], exercise_submission)


class TestCaseResultTests(CustomTestCase):
    def test_model(self) -> None:
        test_case_result = TestCaseResultFactory()

        records = self.session.exec(select(TestCaseResult)).all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], test_case_result)
