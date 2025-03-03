from pydantic import BaseModel, Field, PositiveInt, model_validator
from typing_extensions import Self


class TestCaseCreationSchema(BaseModel):
    external_id: str
    title: str
    test_input: str
    expected_output: str
    score_percentage: PositiveInt = Field(ge=1, lt=100)


class ExerciseCreationSchema(BaseModel):
    external_id: str
    title: str
    question: str = Field(max_length=10000)
    instructions: str | None = Field(max_length=10000, default=None)
    test_cases: list[TestCaseCreationSchema] = Field(min_length=1)


class UserCreationSchema(BaseModel):
    external_id: str


class GroupCreationSchema(BaseModel):
    external_id: str
    students: list[UserCreationSchema] = Field(min_length=1)


class SessionCreationEventData(BaseModel):
    session_title: str | None = None
    session_description: str | None = Field(default=None, max_length=500)
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


class SessionEndedEventData(BaseModel):
    pass


class InidividualSubmissionEventData(BaseModel):
    external_group_id: str | None = None
    external_student_id: str | None = None

    @model_validator(mode="after")
    def check_group_or_student_set(self) -> Self:
        """Check that at least one of group or student is set."""
        if not self.external_group_id and not self.external_student_id:
            raise ValueError("At least one of group or student must be set.")

        if self.external_group_id and self.external_student_id:
            raise ValueError("Only one of group or student can be set.")

        return self


class UserJoinedSessionEventData(BaseModel):
    external_user_id: str
    fullname: str

