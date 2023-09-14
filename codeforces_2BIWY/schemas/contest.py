"""Contest schema"""
from pydantic import BaseModel, ConfigDict


class Contest(BaseModel):
    """Contest schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str = None
    phase: str = None
    frozen: bool = None
    durationSeconds: int = None
    startTimeSeconds: int = None
    relativeTimeSeconds: int = None
    preparedBy: str = None
    websiteUrl: str = None
    description: str = None
    difficulty: int = None
    kind: str = None
    icpcRegion: str = None
    country: str = None
    city: str = None
    season: str = None
