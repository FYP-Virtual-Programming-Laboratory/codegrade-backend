from pydantic import BaseModel, PositiveFloat
from src.enums import EvaluationFlagEnum, SubmissionStatus
import uuid



class GroupPublicSchema(BaseModel):
    id: uuid.UUID
    external_id: str


class UserPublicSchema(BaseModel):
    id: uuid.UUID
    external_id: str
    fullname: str
    group: GroupPublicSchema | None = None


class ExercisePublicSchema(BaseModel):
    id: uuid.UUID
    external_id: str
    question: str
    instructions: str | None


class TestCasePublicSchema(BaseModel):
    id: uuid.UUID
    title: str
    test_input: str
    external_id: str
    expected_output: str
    score_percentage: PositiveFloat


class TestCaseResultPublicSchema(BaseModel):
    id: uuid.UUID
    score: PositiveFloat
    exit_code: int
    std_out: str
    adjusted: bool
    test_case: TestCasePublicSchema


class EvaluationFlagPublicSchema(BaseModel):
    flag: EvaluationFlagEnum
    score_percentage: PositiveFloat


class EvaluationFlagResultPublicSchema(TestCasePublicSchema):
    id: uuid.UUID
    passed: bool
    adjusted: bool
    score: PositiveFloat
    evaluation_flag: EvaluationFlagPublicSchema


class ExerciseSubmissionPublicSchema(BaseModel):
    id: uuid.UUID
    graded: bool
    total_score: PositiveFloat | None
    auto_generated_feedback: str | None
    manual_feedback: str | None
    exercise: ExercisePublicSchema
    test_case_results: list[TestCaseResultPublicSchema]
    evaluation_flag_results: list[EvaluationFlagResultPublicSchema]


class SubmissionPublicSchema(BaseModel):
    id: uuid.UUID
    user: UserPublicSchema
    group: GroupPublicSchema | None = None
    status: SubmissionStatus
    overrall_total: PositiveFloat | None = None
    reviewed: bool
    auto_generated_feedback: str | None
    manual_feedback: str | None
    exercise_submissions: list[ExerciseSubmissionPublicSchema]


class ExerciseSubmissionUpdateSchema(BaseModel):
    manual_feedback: str


class TestCaseResultUpdateSchema(BaseModel):
    passed: bool | None = None
    score: PositiveFloat | None = None


class EvaluationFlagResultUpdateSchema(BaseModel):
    passed: bool | None = None
    score: PositiveFloat | None = None


