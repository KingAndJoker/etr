"""submission model"""
from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from etr.models.base import Base
from etr.models.problem import Problem
from etr.models.user import User
from etr.models.team import Team


class Submission(Base):
    """
    Submission model
    https://codeforces.com/apiHelp/objects#Submission
    """

    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    contest_id: Mapped[int] = mapped_column(nullable=True)
    creation_time_seconds: Mapped[int] = mapped_column()
    relative_time_seconds: Mapped[int] = mapped_column()
    problem_id: Mapped[int] = mapped_column(Integer, ForeignKey("problems.id"))
    problem: Mapped[Problem] = relationship(
        "Problem",
        back_populates="submissions",
        lazy="selectin"
    )
    author_id: Mapped[int] = Column(
        "author_id",
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )
    author: Mapped[User] = relationship(
        "User",
        back_populates="submissions",
        lazy="selectin"
    )
    team_id: Mapped[Team] = Column(
        "team_id",
        Integer,
        ForeignKey("teams.id"),
        nullable=True,
    )
    team: Mapped[Team] = relationship(
        "Team",
        back_populates="submissions",
        lazy="selectin"
    )
    programming_language: Mapped[str] = mapped_column(type_=String(255))
    verdict: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    testset: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    passed_test_count: Mapped[int] = mapped_column(nullable=True)
    time_consumed_millis: Mapped[int] = mapped_column(nullable=True)
    memory_consumed_bytes: Mapped[int] = mapped_column(nullable=True)
    points: Mapped[int] = mapped_column(nullable=True)
    type_of_member: Mapped[str] = mapped_column(
        nullable=True,
        type_=String(255),
        default="PRACTICE"
    )
