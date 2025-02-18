from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import PositiveFloat, PositiveInt
from sqlmodel import (
    TIMESTAMP,
    Column,
    Enum,
    Field,
    Relationship,
    SQLModel,
    UniqueConstraint,
    func,
)

from .enums import ExerciseDificulty, ExerciseStatus, SubmissionStatus, UserRole


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    created_at: datetime = Field(
        nullable=False,
        # SQLModel does not have an overload for this but it'll work in SQLAlchemy
        sa_type=TIMESTAMP(),  # type: ignore
        sa_column_kwargs={"server_default": func.now()},
    )

    updated_at: datetime | None = Field(
        default=None,
        nullable=True,
        # SQLModel does not have an overload for this but it'll work in SQLAlchemy
        sa_type=TIMESTAMP(),  # type: ignore
        sa_column_kwargs={"onupdate": func.now()},
    )


class Session(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    title: str
    description: str
    is_active: bool


class User(BaseModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "external_id",
            name="session_id_unique_together_with_external_id",
        ),
    )
    external_id: str = Field(index=True)
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})
    first_name: str
    last_name: str
    email: str
    role: UserRole = Field(sa_column=Column(Enum(UserRole, name="user__role")))

    group_id: uuid.UUID | None = Field(foreign_key="studentgroup.id", nullable=True)
    group: StudentGroup = Relationship(sa_relationship_kwargs={"lazy": "select"})


class StudentGroup(BaseModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "external_id",
            name="session_id_unique_together_with_external_id",
        ),
    )

    external_id: str = Field(index=True)
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})
    group_title: str


class Exercise(BaseModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "external_id",
            name="session_id_unique_together_with_external_id",
        ),
    )

    external_id: str = Field(index=True)
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})
    title: str
    question: str = Field(max_length=10000, nullable=False)
    instructions: str = Field(max_length=10000, nullable=True)
    difficulty: ExerciseDificulty = Field(
        sa_column=Column(Enum(ExerciseDificulty, name="exercise__difficulty"))
    )
    status: ExerciseStatus = Field(
        sa_column=Column(Enum(ExerciseStatus, name="exercise__status"))
    )
    max_score: PositiveInt


class TestCase(BaseModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "exercise_id",
            "external_id",
            name="exercise_id_unique_together_with_external_id",
        ),
    )

    external_id: str = Field(index=True)
    exercise_id: uuid.UUID = Field(foreign_key="exercise.id")
    exercise: Exercise = Relationship(sa_relationship_kwargs={"lazy": "select"})

    test_input: str
    expected_output: str
    percentage_score: PositiveFloat
    max_score: PositiveInt


class Submission(BaseModel, table=True):
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})
    user_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)
    user: User = Relationship(
        sa_relationship_kwargs={
            "lazy": "select",
            "primaryjoin": "and_(Submission.user_id==User.id, User.role=='STUDENT')",
        },
    )
    status: SubmissionStatus = Field(
        sa_column=Column(Enum(SubmissionStatus, name="submission__status"))
    )
    total_score: PositiveFloat | None
    group_id: uuid.UUID | None = Field(foreign_key="studentgroup.id", nullable=True)
    group: StudentGroup = Relationship(sa_relationship_kwargs={"lazy": "select"})


class ExerciseSubmission(BaseModel, table=True):
    submission_id: uuid.UUID = Field(foreign_key="submission.id")
    submission: Submission = Relationship(
        sa_relationship_kwargs={"lazy": "select"},
    )

    exercise_id: uuid.UUID = Field(foreign_key="exercise.id")
    exercise: Exercise = Relationship(sa_relationship_kwargs={"lazy": "select"})
    graded: bool = Field(default=False)
    total_score: PositiveFloat | None


class TestCaseResult(BaseModel, table=True):
    submission_id: uuid.UUID = Field(foreign_key="exercisesubmission.id")
    submission: ExerciseSubmission = Relationship(
        sa_relationship_kwargs={"lazy": "select"}
    )

    test_case_id: uuid.UUID = Field(foreign_key="testcase.id")
    test_case: TestCase = Relationship(sa_relationship_kwargs={"lazy": "select"})

    passed: bool
    std_out: str = Field(max_length=10000)
    exit_code: int
