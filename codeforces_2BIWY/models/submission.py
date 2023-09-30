"""submission model"""
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codeforces_2BIWY.models.base import Base
from codeforces_2BIWY.models.problem import Problem
from codeforces_2BIWY.models.user import User
from codeforces_2BIWY.models.team import Team


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
    )
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author: Mapped[User] = relationship("User", back_populates="submissions")
    team_id: Mapped[Team] = mapped_column(Integer, ForeignKey("teams.id"))
    team: Mapped[Team] = relationship("Team", back_populates="submissions")
    programming_language: Mapped[str] = mapped_column()
    verdict: Mapped[str] = mapped_column(nullable=True)
    testset: Mapped[str] = mapped_column(nullable=True)
    passed_test_count: Mapped[int] = mapped_column(nullable=True)
    time_consumed_millis: Mapped[int] = mapped_column(nullable=True)
    memory_consumed_bytes: Mapped[int] = mapped_column(nullable=True)
    points: Mapped[int] = mapped_column(nullable=True)
