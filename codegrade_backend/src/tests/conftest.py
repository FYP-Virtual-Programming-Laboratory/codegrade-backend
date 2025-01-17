from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.core.db import engine, init_db
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
