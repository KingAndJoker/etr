"""Codeforces Problem schema"""
from pydantic import (
    BaseModel,
    ConfigDict
)


class CodeforcesProblemSchema(BaseModel):
    """
    Codeforces Problem schema
    https://codeforces.com/apiHelp/objects#Problem
    """
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int | None = None
    contestId: int | None = None
    problemsetName: str | None = None
    index: str
    name: str | None = None
    type: str | None = None
    points: float | None = None
    rating: int | None = None
    tags: list[str] | None = None


class CodeforcesProblemStatistics(BaseModel):
    """Codeforces problem staticstics
    https://codeforces.com/apiHelp/objects#ProblemStatistics
    """
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    contestId: int | None = None
    index: str
    solvedCount: int
