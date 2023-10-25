import pytest
from sqlalchemy import create_engine, Engine

from etr.models.base import Base
from etr.models.contest import Contest
from etr.models.problem import Problem
from etr.models.submission import Submission


@pytest.fixture()
def in_memory_db_empty(uri: str | None = None) -> Engine:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture()
def in_memory_db(uri: str | None = None) -> Engine:
    engine = in_memory_db_empty(uri)

    # TODO: seeding database
    ...

    return engine
