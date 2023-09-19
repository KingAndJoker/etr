"""Problem schema"""
from pydantic import BaseModel, ConfigDict


class ProblemSchema(BaseModel):
    """Problem schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    contestId: int | None = None
    problemsetName: str  | None = None
    index: str | None = None
    name: str | None = None
    type: str | None = None
    points: float | None = None
    rating: int | None = None
    # tags: list[str] | None = None
