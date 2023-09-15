"""submission model"""
from sqlalchemy.orm import Mapped, mapped_column

from codeforces_2BIWY.models.base import Base


class Submission(Base):
    """
    Submission model
    without field:
      author
      testset
      partial problem

    https://codeforces.com/apiHelp/objects#Submission
    """

    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    contestId: Mapped[int] = mapped_column()
    creationTimeSeconds: Mapped[int] = mapped_column()
    relativeTimeSeconds: Mapped[int] = mapped_column()
    problemName: Mapped[str] = mapped_column()
    problemIndex: Mapped[str] = mapped_column()
    programmingLanguage: Mapped[str] = mapped_column()
    verdict: Mapped[str] = mapped_column()
    passedTestCount: Mapped[int] = mapped_column()
    timeConsumedMillis: Mapped[int] = mapped_column()
    memoryConsumedBytes: Mapped[int] = mapped_column()
    points: Mapped[int] = mapped_column()
