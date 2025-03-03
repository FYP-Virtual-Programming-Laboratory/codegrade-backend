from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import PositiveFloat
from sqlmodel import (
    TIMESTAMP,
    Field,
    Relationship,
    SQLModel,
    UniqueConstraint,
    func,
)

from .enums import EvaluationFlagEnum, SubmissionStatus


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
    title: str | None = Field(default=None, nullable=True)
    description: str | None = Field(default=None, nullable=True)
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
    fullname: str | None = Field(default=None, nullable=True)

    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})

    group_id: uuid.UUID | None = Field(foreign_key="group.id", nullable=True)
    group: Group = Relationship(sa_relationship_kwargs={"lazy": "select"})


class Group(BaseModel, table=True):
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
    question: str = Field(max_length=10000, nullable=False)
    instructions: str | None = Field(max_length=10000, nullable=True)


class EvaluationFlag(BaseModel, table=True):
    exercise_id: uuid.UUID = Field(foreign_key="exercise.id")
    exercise: Exercise = Relationship(sa_relationship_kwargs={"lazy": "select"})
    flag: EvaluationFlagEnum
    score_percentage: PositiveFloat


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
    title: str
    test_input: str
    expected_output: str
    score_percentage: PositiveFloat


class Submission(BaseModel, table=True):
    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: Session = Relationship(sa_relationship_kwargs={"lazy": "select"})

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(sa_relationship_kwargs={"lazy": "select"})

    group_id: uuid.UUID | None = Field(foreign_key="group.id", nullable=True)
    group: Group = Relationship(sa_relationship_kwargs={"lazy": "select"})

    status: SubmissionStatus
    overrall_total: PositiveFloat | None
    reviewed: bool = Field(default=False)
    auto_generated_feedback: str | None = Field(max_length=5000, nullable=False)
    manual_feedback: str | None = Field(max_length=5000, nullable=False)
    exercise_submissions: list[ExerciseSubmission] = Relationship(back_populates='submission')


class ExerciseSubmission(BaseModel, table=True):
    submission_id: uuid.UUID = Field(foreign_key="submission.id")
    submission: Submission = Relationship(
        back_populates='exercise_submissions',
        sa_relationship_kwargs={"lazy": "select"}
    )

    exercise_id: uuid.UUID = Field(foreign_key="exercise.id")
    exercise: Exercise = Relationship(sa_relationship_kwargs={"lazy": "select"})

    graded: bool = Field(default=False)
    total_score: PositiveFloat | None
    auto_generated_feedback: str | None = Field(max_length=5000, nullable=False)
    manual_feedback: str | None = Field(max_length=5000, nullable=False)

    test_case_results: list[TestCaseResult] = Relationship(back_populates='submission')
    evaluation_flag_results: list[EvaluationFlagResult] = Relationship(back_populates='submission')


class TestCaseResult(BaseModel, table=True):
    submission_id: uuid.UUID = Field(foreign_key="exercisesubmission.id")
    submission: ExerciseSubmission = Relationship(
        back_populates='test_case_results',
        sa_relationship_kwargs={"lazy": "select"},
    )

    test_case_id: uuid.UUID = Field(foreign_key="testcase.id")
    test_case: TestCase = Relationship(sa_relationship_kwargs={"lazy": "select"})

    passed: bool
    score: PositiveFloat
    exit_code: int
    std_out: str = Field(max_length=1000)
    adjusted: bool = Field(default=False)


class EvaluationFlagResult(BaseModel, table=True):
    submission_id: uuid.UUID = Field(foreign_key="exercisesubmission.id")
    submission: ExerciseSubmission = Relationship(
        back_populates='evaluation_flag_results',
        sa_relationship_kwargs={"lazy": "select"}
    )
    
    evaluation_flag_id: uuid.UUID = Field(foreign_key="evaluationflag.id")
    evaluation_flag: EvaluationFlag = Relationship(sa_relationship_kwargs={"lazy": "select"})
    
    passed: bool
    score: PositiveFloat
    adjusted: bool = Field(default=False)
