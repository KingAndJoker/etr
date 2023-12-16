"""db utils"""
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from etr import config
from etr.models.base import Base
from etr.models.contest import ContestOrm
from etr.models.problem import ProblemOrm, TagOrm, problems_tags
from etr.models.submission import SubmissionOrm
from etr.models.team import TeamOrm, teams_users
from etr.models.user import UserOrm


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(engine)


SQLALCHEMY_DATABASE_URL = config.DATABASE_URL
SQLALCHEMY_ECHO = config.SQLALCHEMY_ECHO

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
