"""contest model"""
from sqlalchemy.orm import Mapped, mapped_column

from codeforces_2BIWY.models.base import Base


class Contest(Base):
    """Contest model"""

    __tablename__ = "contests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column(nullable=True)
    phase: Mapped[str] = mapped_column(nullable=True)
    frozen: Mapped[bool] = mapped_column(nullable=True)
    durationSeconds: Mapped[int] = mapped_column(nullable=True)
    startTimeSeconds: Mapped[int] = mapped_column(nullable=True)
    relativeTimeSeconds: Mapped[int] = mapped_column(nullable=True)
    preparedBy: Mapped[str] = mapped_column(nullable=True)
    websiteUrl: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    difficulty: Mapped[int] = mapped_column(nullable=True)
    kind: Mapped[str] = mapped_column(nullable=True)
    icpcRegion: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    season: Mapped[str] = mapped_column(nullable=True)
