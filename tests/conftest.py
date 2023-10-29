import pytest
from flask import Flask
from sqlalchemy import create_engine, Engine

from etr.models.base import Base
from etr.models.contest import Contest
from etr.models.problem import Problem
from etr.models.submission import Submission
from etr import create_app
from tests.seeding import seeding


@pytest.fixture()
def in_memory_db_empty() -> Engine:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture()
def in_memory_db(in_memory_db_empty) -> Engine:
    engine = in_memory_db_empty

    seeding(engine)

    return engine


@pytest.fixture()
def app(in_memory_db):
    app = create_app(in_memory_db)
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    return app.test_cli_runner()
