from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from src.grading.services import (
    list_submissions_services, 
    get_submission_by_id_services, 
    mark_submission_as_reviewed_services,
    get_exercise_submission_by_id_service,
    update_execution_flag_result_service,
    update_exercise_submission_service,
    update_testcases_result_service,
)
from src.grading.schemas import EvaluationFlagResultUpdateSchema, ExerciseSubmissionPublicSchema, SubmissionPublicSchema, TestCaseResultPublicSchema
from typing import Annotated


router = APIRouter()


@router.get('/{external_session_id}/submissions/')
def list_submissions(
    submissions: Annotated[
        list[SubmissionPublicSchema],
        Depends(list_submissions_services)
    ]
) -> list[SubmissionPublicSchema]:
    """List submissions for a given session."""
    return submissions


@router.get('/{external_session_id}/submissions/{submission_id}/')
def get_submission_details(
    submission: Annotated[
        SubmissionPublicSchema,
        Depends(get_submission_by_id_services),
    ]
) -> SubmissionPublicSchema:
    """Get submission by ID."""
    return submission


@router.post('/{external_session_id}/submissions/{submission_id}/')
def mark_submission_as_reviewed(
    submission: Annotated[
        SubmissionPublicSchema,
        Depends(mark_submission_as_reviewed_services),
    ]
) -> SubmissionPublicSchema:
    """Mark submission as reviewed."""
    return submission


@router.get(
    '/{external_session_id}/submissions/{submission_id}/exercises/{exercise_id}/'
)
def get_exercise_submission(
    exercise_submission: Annotated[
        ExerciseSubmissionPublicSchema,
        Depends(get_exercise_submission_by_id_service),
    ]
) -> ExerciseSubmissionPublicSchema:
    """Get exercise submission by ID."""
    return exercise_submission


@router.put(
    '/{external_session_id}/submissions/{submission_id}/exercises/{exercise_id}/'
)
def update_exercise_submission(
    exercise_submission: Annotated[
        ExerciseSubmissionPublicSchema,
        Depends(update_exercise_submission_service),
    ]
) -> ExerciseSubmissionPublicSchema:
    """Get exercise submission by ID."""
    return exercise_submission


@router.patch(
    '/{external_session_id}/submissions/'
    '{submission_id}/exercises/{exercise_id}/testcases/{testcase_id}'
)
def update_testcase_submission(
    testcase_result: Annotated[
        TestCaseResultPublicSchema,
        Depends(update_testcases_result_service),
    ]
) -> TestCaseResultPublicSchema:
    """Update testcase result."""
    return testcase_result


@router.patch(
    '/{external_session_id}/submissions/'
    '{submission_id}/exercises/{exercise_id}/flags/{executionflag_id}'
)
def update_evaluation_flag_submission(
    executionflag_result: Annotated[
        EvaluationFlagResultUpdateSchema,
        Depends(update_execution_flag_result_service),
    ]
) -> EvaluationFlagResultUpdateSchema:
    """Update testcase result."""
    return executionflag_result


@router.post('/{external_session_id}/submissions/{submission_id}/report')
def generate_student_report() -> FileResponse:
    """Generate student report."""
    # TODO: Use the report service to build the HTML report
    # convert it to PDF format and return it here 
    return FileResponse('report.pdf')
