"""Problem schema"""
from pydantic import BaseModel, ConfigDict


class ProblemSchema(BaseModel):
    """Problem schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int 
    contestId: int
    problemsetName: str
    index: str
    name: str
    type: str
    points: float | None = None
    rating: int | None = None
    tags: list[str] | None = None
