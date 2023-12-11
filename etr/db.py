"""db utils"""
import os
from flask import Flask
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from etr.models.base import Base
from etr.models.user import User
from etr.models.contest import Contest
from etr.models.submission import Submission
from etr.models.problem import Problem
from etr.models.team import Team, teams_users


engine = None
Session_ = None


# TODO: rewrite to class
# TODO: fix bug sqlite:///:memory: not see
def init_db(database_url: str, echo: bool = False) -> Engine:
    global engine
    engine = create_engine(database_url, echo=echo)
    Base.metadata.create_all(engine)
    global Session_
    Session_ = sessionmaker(engine)
    return engine


def get_db() -> Session:
    return Session_()
