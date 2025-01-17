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
    func,
)

from .enums import ExcerciseDificulty, ExcerciseStatus, UserRole


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


class StudentGroup(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})
    group_title: str

    students: list[User] = Relationship(
        back_populates="group", sa_relationship_kwargs={"lazy": "select"}
    )

    submission: Submission | None = Relationship(back_populates="group")


class User(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})
    first_name: str
    last_name: str
    email: str
    role: UserRole = Field(sa_column=Column(Enum(UserRole, name="user__role")))

    group_id: uuid.UUID | None = Field(foreign_key="studentgroup.id", nullable=True)
    group: StudentGroup | None = Relationship(
        back_populates="students", sa_relationship_kwargs={"lazy": "select"}
    )

    submission: Submission | None = Relationship(back_populates="user")


class Exercise(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})
    title: str
    question: str = Field(max_length=5000, nullable=False)
    difficulty: ExcerciseDificulty = Field(
        sa_column=Column(Enum(ExcerciseDificulty, name="exercise__difficulty"))
    )
    status: ExcerciseStatus = Field(
        sa_column=Column(Enum(ExcerciseStatus, name="exercise__status"))
    )
    max_score: PositiveInt
    test_cases: list[TestCase] = Relationship(back_populates="excercise")


class TestCase(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    exercise_id: uuid.UUID = Field(foreign_key="exercise.id")
    exercise: Exercise = Relationship(
        back_populates="test_cases",
        sa_relationship_kwargs={"lazy": "select"},
    )

    test_input: str
    expected_output: str
    percentage_score: PositiveFloat
    max_score: PositiveInt


class Submission(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    user_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)
    user: User | None = Relationship(
        back_populates="submission",
        sa_relationship_kwargs={
            "lazy": "select",
            "primaryjoin": "and_(Submission.user_id==User.id, User.role=='STUDENT')",
        },
    )
    graded: bool = Field(default=False)
    total_score: PositiveFloat | None
    group_id: uuid.UUID | None = Field(foreign_key="studentgroup.id", nullable=True)
    group: StudentGroup | None = Relationship(
        back_populates="submission", sa_relationship_kwargs={"lazy": "select"}
    )

    excercise_submissions: list[ExcerciseSubmission] = Relationship(
        back_populates="submission", sa_relationship_kwargs={"lazy": "select"}
    )


class ExcerciseSubmission(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    submission_id: uuid.UUID = Field(foreign_key="submission.id")
    submission: Submission = Relationship(
        back_populates="excercise_submissions",
        sa_relationship_kwargs={"lazy": "select"},
    )

    exercise_id: uuid.UUID = Field(foreign_key="exercise.id")
    exercise: Exercise = Relationship(sa_relationship_kwargs={"lazy": "select"})

    test_case_results: list[TestCaseResult] = Relationship(
        back_populates="submission", sa_relationship_kwargs={"lazy": "select"}
    )

    total_score: PositiveFloat | None


class TestCaseResult(BaseModel, table=True):
    external_id: str = Field(index=True, unique=True)
    submission_id: uuid.UUID = Field(foreign_key="excercisesubmission.id")
    submission: Submission = Relationship(
        back_populates="test_case_results",
        sa_relationship_kwargs={"lazy": "select"},
    )

    test_case_id: uuid.UUID = Field(foreign_key="testcase.id")
    test_case: TestCase = Relationship(sa_relationship_kwargs={"lazy": "select"})

    passed: bool
    std_out: str = Field(max_length=10000)
    exit_code: int
