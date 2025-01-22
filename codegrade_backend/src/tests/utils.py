from unittest import TestCase

from sqlalchemy.orm import close_all_sessions
from sqlmodel import Session, SQLModel

from src.core.db import engine
from src.tests.conftest import TestDBSession


class CustomTestCase(TestCase):
    session: Session

    def setUp(self) -> None:
        self.setUpClass()

    def tearDown(self) -> None:
        self.tearDownClass()

    @classmethod
    def _clear_database(cls) -> None:
        with engine.connect() as connection:
            for table in reversed(SQLModel.metadata.sorted_tables):
                connection.execute(table.delete())
                connection.commit()

    @classmethod
    def setUpClass(cls) -> None:
        """Hook method for setting up class fixture before running tests in the class."""
        close_all_sessions()
        cls.session = TestDBSession()

    @classmethod
    def tearDownClass(cls) -> None:
        """Hook method for deconstructing the class fixture after running all tests in the class."""
        close_all_sessions()
        cls._clear_database()
