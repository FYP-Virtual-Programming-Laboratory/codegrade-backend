from __future__ import annotations

from enum import Enum, StrEnum


class EvaluationFlagEnum(StrEnum):
    execution = 'execution'
    compilation = 'compilation'
    code_quality = 'code_quality'


class SubmissionStatus(StrEnum):
    QUEUED = "queued"
    GRADING = "grading"
    GRADED = "graded"
    FAILED = "failed"
