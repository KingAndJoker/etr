"""db utils"""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from etr.models.base import Base
from etr.models.user import User
from etr.models.contest import Contest
from etr.models.submission import Submission
from etr.models.problem import Problem
from etr.models.team import Team, teams_users


DATABASE_URL = "sqlite:///users.db"
ECHO = True
engine = None


def init_db(app: Flask) -> None:
    engine = create_engine(DATABASE_URL, echo=ECHO)
    Base.metadata.create_all(engine)


def get_db() -> Session:
    global engine
    if engine:
        return Session(engine)
    else:
        engine = create_engine(DATABASE_URL, echo=ECHO)
        return Session(engine)
