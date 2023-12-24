"""Codeforces Contest schema"""
from pydantic import BaseModel, ConfigDict

from etr.library.codeforces.schemas.problem import CodeforcesProblemSchema


class CodeforcesContestSchema(BaseModel):
    """Codeforces Contest schema"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int
    name: str
    type: str | None = None
    phase: str | None = None
    frozen: bool | None = None
    durationSeconds: int | None = None
    startTimeSeconds: int | None = None
    relativeTimeSeconds: int | None = None
    preparedBy: str | None = None
    websiteUrl: str | None = None
    description: str | None = None
    difficulty: int | None = None
    kind: str | None = None
    icpcRegion: str | None = None
    country: str | None = None
    city: str | None = None
    season: str | None = None
    problems: list[CodeforcesProblemSchema] | None = None
