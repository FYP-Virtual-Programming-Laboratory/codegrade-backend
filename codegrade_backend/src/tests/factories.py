import random
import uuid

from factory import LazyAttribute, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.enums import ExerciseDificulty, ExerciseStatus, UserRole
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
from src.tests.conftest import TestDBSession

fake = Faker()


class SessionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Session
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    title = Sequence(lambda n: "test session %d" % n)
    description = LazyAttribute(lambda o: fake.text())
    is_active = True


class StudentGroupFactory(SQLAlchemyModelFactory):
    class Meta:
        model = StudentGroup
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    session = LazyAttribute(lambda o: SessionFactory())
    group_title = Sequence(lambda n: "test group %d" % n)


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    session = LazyAttribute(lambda o: SessionFactory())
    first_name = LazyAttribute(lambda o: fake.first_name())
    last_name = LazyAttribute(lambda o: fake.last_name())
    email = LazyAttribute(lambda o: fake.email())
    role = UserRole.STUDENT
    group = LazyAttribute(lambda o: StudentGroupFactory(session=o.session))


class ExerciseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Exercise
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    session = LazyAttribute(lambda o: SessionFactory())
    title = Sequence(lambda n: "test exercise %d" % n)
    question = LazyAttribute(lambda o: fake.text())
    difficulty = ExerciseDificulty.EASY
    status = ExerciseStatus.COMPLEMENTARY
    max_score = 100


class TestCaseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = TestCase
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    exercise = LazyAttribute(lambda o: ExerciseFactory())
    test_input = LazyAttribute(lambda o: fake.text())
    expected_output = LazyAttribute(lambda o: fake.text())
    percentage_score = 1.0
    max_score = 100


class SubmissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Submission
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    user = LazyAttribute(lambda o: UserFactory())
    exercise = LazyAttribute(lambda o: ExerciseFactory())
    graded = False


class ExerciseSubmissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExerciseSubmission
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    submission = LazyAttribute(lambda o: SubmissionFactory())
    exercise = LazyAttribute(lambda o: ExerciseFactory())
    total_score = LazyAttribute(lambda o: float(random.randint(1, 100) / 100))


class TestCaseResultFactory(SQLAlchemyModelFactory):
    class Meta:
        model = TestCaseResult
        sqlalchemy_session = TestDBSession

    external_id = LazyAttribute(lambda o: str(uuid.uuid4()))
    test_case = LazyAttribute(lambda o: TestCaseFactory())
    submission = LazyAttribute(lambda o: ExerciseSubmissionFactory())
    passed = True
    std_out = LazyAttribute(lambda o: fake.text())
    exit_code = LazyAttribute(lambda o: float(random.randint(0, 200)))
