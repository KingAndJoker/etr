"""db utils"""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from codeforces_2BIWY.models.base import Base
from codeforces_2BIWY.models.user import User
from codeforces_2BIWY.models.contest import Contest
from codeforces_2BIWY.models.submission import Submission
from codeforces_2BIWY.models.problem import Problem
from codeforces_2BIWY.models.team import Team, teams_users


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
