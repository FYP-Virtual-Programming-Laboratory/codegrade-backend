from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session

from src.core.db import engine
from src.core.security import SECURITY_HEADER, verify_api_key


def require_db_session() -> Generator[Session, None, None]:
    """Get a new database session."""

    with Session(engine) as session:
        yield session


def require_authenticated_service(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(SECURITY_HEADER)],
) -> bool:
    """Check if the provided API key is valid."""
    if not verify_api_key(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return True
