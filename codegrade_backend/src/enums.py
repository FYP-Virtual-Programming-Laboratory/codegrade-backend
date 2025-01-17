from __future__ import annotations

from enum import Enum


class UserRole(Enum):
    TUTOR: str = "tutor"
    STUDENT: str = "student"


class ExcerciseDificulty(Enum):
    EASY: str = "easy"
    MODERATE: str = "moderate"
    HARD: str = "hard"


class ExcerciseStatus(Enum):
    COMPLEMENTARY: str = "complementary"
    OPTIONAL: str = "optional"
