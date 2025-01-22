import os
from collections.abc import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError
from sqlmodel import Session, SQLModel

patch.dict(os.environ, {"ENVIRONMENT": "staging"}).start()  # noqa
from sqlalchemy import orm  # noqa

from src.core.db import engine, init_db  # noqa
from src.main import app  # noqa

TestDBSession = orm.scoped_session(orm.sessionmaker(bind=engine, class_=Session))
TestDBSession.configure(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def manage_test_database():
    """Manage test database."""

    # setup actions
    # create a new test database
    try:
        # clear database
        SQLModel.metadata.drop_all(engine)
        # create database tables
        SQLModel.metadata.create_all(engine)
    except ProgrammingError:
        # database already empty just pass
        pass

    # create database tables
    SQLModel.metadata.create_all(engine)

    yield

    # tear down actions
    # clear test data-base
    SQLModel.metadata.drop_all(engine)
