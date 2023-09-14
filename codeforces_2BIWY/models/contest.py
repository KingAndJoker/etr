"""contest model"""
from sqlalchemy.orm import Mapper, mapped_column

from codeforces_2BIWY.models.base import Base


class Contest(Base):
    id: Mapper[int] = mapped_column(primary_key=True)
    name: Mapper[str] = mapped_column()
    type: Mapper[str] = mapped_column(nullable=True)
    phase: Mapper[str] = mapped_column(nullable=True)
    frozen: Mapper[bool] = mapped_column(nullable=True)
    durationSeconds: Mapper[int] = mapped_column(nullable=True)
    startTimeSeconds: Mapper[int] = mapped_column(nullable=True)
    relativeTimeSeconds: Mapper[int] = mapped_column(nullable=True)
    preparedBy: Mapper[str] = mapped_column(nullable=True)
    websiteUrl: Mapper[str] = mapped_column(nullable=True)
    description: Mapper[str] = mapped_column(nullable=True)
    difficulty: Mapper[int] = mapped_column(nullable=True)
    kind: Mapper[str] = mapped_column(nullable=True)
    icpcRegion: Mapper[str] = mapped_column(nullable=True)
    country: Mapper[str] = mapped_column(nullable=True)
    city: Mapper[str] = mapped_column(nullable=True)
    season: Mapper[str] = mapped_column(nullable=True)
