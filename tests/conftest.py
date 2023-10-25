import pytest
from sqlalchemy import create_engine, Engine

from etr.models.base import Base


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
