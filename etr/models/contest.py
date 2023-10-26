"""contest model"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from etr.models.base import Base


class Contest(Base):
    """Contest model"""

    __tablename__ = "contests"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(type_=String(255))
    type: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    phase: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    frozen: Mapped[bool] = mapped_column(nullable=True)
    duration_seconds: Mapped[int] = mapped_column(nullable=True)
    start_time_seconds: Mapped[int] = mapped_column(nullable=True)
    relative_time_seconds: Mapped[int] = mapped_column(nullable=True)
    prepared_by: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    website_url: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    description: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    difficulty: Mapped[int] = mapped_column(nullable=True)
    kind: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    icpc_region: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    country: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    city: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    season: Mapped[str] = mapped_column(nullable=True, type_=String(255))

    problems: Mapped[list["Problem"]] = relationship(
        "Problem",
        lazy="selectin"
    )
