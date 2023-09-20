"""submission model"""
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column

from codeforces_2BIWY.models.base import Base


class Submission(Base):
    """
    Submission model
    https://codeforces.com/apiHelp/objects#Submission
    """

    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    contestId: Mapped[int] = mapped_column()
    creationTimeSeconds: Mapped[int] = mapped_column()
    relativeTimeSeconds: Mapped[int] = mapped_column()
    problem_id: Mapped[int] = Column(ForeignKey("problems.id"))
    author_id: Mapped[int] = Column(ForeignKey("users.id"))
    team_id: Mapped[int] = Column(ForeignKey("teams.id"))
    programmingLanguage: Mapped[str] = mapped_column()
    verdict: Mapped[str] = mapped_column()
    passedTestCount: Mapped[int] = mapped_column()
    timeConsumedMillis: Mapped[int] = mapped_column()
    memoryConsumedBytes: Mapped[int] = mapped_column()
    points: Mapped[int] = mapped_column()
