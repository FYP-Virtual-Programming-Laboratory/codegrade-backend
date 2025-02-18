from pydantic import BaseModel, EmailStr, Field, PositiveInt, model_validator
from typing_extensions import Self

from src.enums import ExerciseDificulty, ExerciseStatus


class TestCaseCreationSchema(BaseModel):
    external_id: str
    test_input: str
    expected_output: str
    percentage_score: PositiveInt = Field(ge=1, lt=100)
    max_score: PositiveInt = Field(ge=1, lt=100)


class ExerciseCreationSchema(BaseModel):
    external_id: str
    title: str
    question: str = Field(max_length=10000)
    instructions: str | None = Field(max_length=10000, default=None)
    score: PositiveInt = Field(ge=1, lt=100)
    difficulty: ExerciseDificulty = Field(default=ExerciseDificulty.MODERATE)
    status: ExerciseStatus = Field(default=ExerciseStatus.COMPLEMENTARY)
    test_cases: list[TestCaseCreationSchema] = Field(min_length=1)


class UserCreationSchema(BaseModel):
    external_id: str
    first_name: str
    last_name: str
    email: EmailStr


class GroupCreationSchema(BaseModel):
    external_id: str
    group_title: str
    students: list[UserCreationSchema] = Field(min_length=1)


class SessionCreationEventData(BaseModel):
    session_title: str
    session_description: str = Field(max_length=500)
    exercises: list[ExerciseCreationSchema] = Field(min_length=1)
    groups: list[GroupCreationSchema] | None = None
    students: list[UserCreationSchema] | None = None

    @model_validator(mode="after")
    def check_students_or_groups_set(self) -> Self:
        """Check that at least one of students or groups is set."""
        if not self.students and not self.groups:
            raise ValueError("At least one of students or groups must be set.")

        if self.students and self.groups:
            raise ValueError("Only one of students or groups can be set.")

        return self
