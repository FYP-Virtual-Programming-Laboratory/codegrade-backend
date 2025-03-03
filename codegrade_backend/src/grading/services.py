import uuid
from fastapi import Body, HTTPException, Path, Depends
from typing import Annotated
from sqlmodel import (
    select,
    Session as DbSession
)
from src.models import EvaluationFlagResult, ExerciseSubmission, Session, Submission, TestCaseResult
from src.core.dependecies import require_authenticated_service, require_db_session
from src.grading.schemas import EvaluationFlagResultUpdateSchema, ExerciseSubmissionUpdateSchema, SubmissionPublicSchema, ExerciseSubmissionPublicSchema, TestCaseResultPublicSchema, TestCaseResultUpdateSchema


def get_session_by_external_id_service(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    external_session_id: Annotated[str, Path()],
) -> Session:
    """Get session by external ID."""
    session = db_session.exec(
        select(Session).where(Session.external_id == external_session_id)
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


def list_submissions_services(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    session: Annotated[Session, Depends(get_session_by_external_id_service)],
) -> list[SubmissionPublicSchema]:
    """List submissions for a given session."""
    
    submissions = db_session.exec(
        select(Submission).where(Submission.session_id == session.id)
    ).all()

    return [
        SubmissionPublicSchema.model_validate(submission, from_attributes=True) 
        for submission in submissions
    ]


def get_submission_by_id_services(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    session: Annotated[Session, Depends(get_session_by_external_id_service)],
    submission_id: Annotated[uuid.UUID, Path()],
) -> SubmissionPublicSchema:
    """Get submission by ID."""
    
    submission = db_session.exec(
        select(Submission).where(
            Submission.session_id == session.id,
            Submission.id == submission_id,
        )
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return SubmissionPublicSchema.model_validate(submission, from_attributes=True)


def mark_submission_as_reviewed_services(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    session: Annotated[Session, Depends(get_session_by_external_id_service)],
    submission_id: Annotated[uuid.UUID, Path()],
) -> SubmissionPublicSchema:
    """Mark submission as reviewed."""
    
    submission = db_session.exec(
        select(Submission).where(
            Submission.session_id == session.id,
            Submission.id == submission_id,
        )
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission.reviewed = True
    db_session.commit()
    db_session.refresh(submission)
    return SubmissionPublicSchema.model_validate(submission, from_attributes=True)


def get_exercise_submission_by_id_service(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    session: Annotated[Session, Depends(get_session_by_external_id_service)],
    submission_id: Annotated[uuid.UUID, Path()],
    exercise_id: Annotated[uuid.UUID, Path()],
) -> ExerciseSubmissionPublicSchema:
    """Get exercise submission by ID."""

    exercise_submission = db_session.exec(
        select(ExerciseSubmission).where(
            Submission.session_id == session.id,
            Submission.id == submission_id,
            ExerciseSubmission.exercise_id == exercise_id,
        )
    ).first()

    if not exercise_submission:
        raise HTTPException(status_code=404, detail="Exercise submission not found")

    return ExerciseSubmissionPublicSchema.model_validate(exercise_submission, from_attributes=True)


def update_exercise_submission_service(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    session: Annotated[Session, Depends(get_session_by_external_id_service)],
    submission_id: Annotated[uuid.UUID, Path()],
    exercise_id: Annotated[uuid.UUID, Path()],
    update_data: Annotated[ExerciseSubmissionUpdateSchema, Body()],
)  -> ExerciseSubmissionPublicSchema:
    """Update exercise submission."""

    exercise_submission = db_session.exec(
        select(ExerciseSubmission).where(
            ExerciseSubmission.submission_id == submission_id,
            ExerciseSubmission.id == exercise_id,
        )
    ).first()

    if not exercise_submission:
        raise HTTPException(status_code=404, detail="Exercise submission not found")

    exercise_submission.manual_feedback = update_data.manual_feedback
    db_session.add(exercise_submission)
    db_session.commit()
    db_session.refresh(exercise_submission)
    return ExerciseSubmissionPublicSchema.model_validate(exercise_submission, from_attributes=True)


def update_testcases_result_service(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    session: Annotated[Session, Depends(get_session_by_external_id_service)],
    submission_id: Annotated[uuid.UUID, Path()],
    testcase_id: Annotated[uuid.UUID, Path()],
    update_data: Annotated[TestCaseResultUpdateSchema, Body()],
) -> TestCaseResultPublicSchema:
    """Update testcase result."""

    testcase_result = db_session.exec(
        select(TestCaseResult).where(
            TestCaseResult.submission_id == submission_id,
            TestCaseResult.id == testcase_id,
        )
    ).first()

    if not testcase_result:
        raise HTTPException(status_code=404, detail="Testcase result not found")

    testcase_result.sqlmodel_update(update_data.model_dump(exclude_unset=True))
    testcase_result.adjusted = True
    db_session.add(testcase_result)
    db_session.commit()
    db_session.refresh(testcase_result)
    return TestCaseResultPublicSchema.model_validate(testcase_result, from_attributes=True)


def update_execution_flag_result_service(
    _: Annotated[bool, Depends(require_authenticated_service)],
    db_session: Annotated[DbSession, Depends(require_db_session)],
    session: Annotated[Session, Depends(get_session_by_external_id_service)],
    submission_id: Annotated[uuid.UUID, Path()],
    executionflag_id: Annotated[uuid.UUID, Path()],
    update_data: Annotated[EvaluationFlagResultUpdateSchema, Body()],
) -> EvaluationFlagResultUpdateSchema:
    """Update testcase result."""

    evaluation_flag_result = db_session.exec(
        select(EvaluationFlagResult).where(
            EvaluationFlagResult.submission_id == submission_id,
            EvaluationFlagResult.id == executionflag_id,
        )
    ).first()

    if not evaluation_flag_result:
        raise HTTPException(status_code=404, detail="Result not found")

    evaluation_flag_result.sqlmodel_update(update_data.model_dump(exclude_unset=True))
    evaluation_flag_result.adjusted = True
    db_session.add(evaluation_flag_result)
    db_session.commit()
    db_session.refresh(evaluation_flag_result)
    return EvaluationFlagResultUpdateSchema.model_validate(evaluation_flag_result, from_attributes=True)
