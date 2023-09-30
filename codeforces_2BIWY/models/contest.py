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
    duration_seconds: Mapped[int] = mapped_column(nullable=True)
    start_time_seconds: Mapped[int] = mapped_column(nullable=True)
    relative_time_seconds: Mapped[int] = mapped_column(nullable=True)
    prepared_by: Mapped[str] = mapped_column(nullable=True)
    website_url: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    difficulty: Mapped[int] = mapped_column(nullable=True)
    kind: Mapped[str] = mapped_column(nullable=True)
    icpc_region: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    season: Mapped[str] = mapped_column(nullable=True)
