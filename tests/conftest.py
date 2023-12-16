import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from etr import db
from etr import create_app
from tests.seeding import seeding


@pytest.fixture()
def in_memory_db_empty() -> Engine:
    db.engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    db.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db.engine)
    db.init_db(db.engine)
    return db.engine


@pytest.fixture()
def in_memory_db(in_memory_db_empty) -> Engine:
    engine = in_memory_db_empty

    seeding(engine)

    return engine


@pytest.fixture()
def app(in_memory_db):
    app = create_app()
    return app


@pytest.fixture()
def client(app: FastAPI):
    return TestClient(app)
