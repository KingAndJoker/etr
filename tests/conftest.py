import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from etr.models.base import Base
from etr.models.contest import Contest
from etr.models.problem import Problem, Tag, problems_tags
from etr.models.submission import Submission
from etr.models.team import Team, teams_users
from etr.models.user import User


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
