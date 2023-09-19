"""problem model"""
from sqlalchemy.orm import Mapped, mapped_column
from codeforces_2BIWY.models.base import Base


class Problem(Base):
    """problem (aka task) model"""

    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contestId: Mapped[int] = mapped_column()
    problemsetName: Mapped[str] = mapped_column()
    index: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    points: Mapped[float] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)
    # tags: Mapped[list[str]] = mapped_column(nullable=True)
