"""Problem schema"""
from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class ProblemSchema(BaseModel):
    """Problem schema"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int | None = None
    contest_id: int | None = Field(default=None, alias="contestId")
    problemset_name: str | None = Field(default=None, alias="problemsetName")
    index: str
    name: str | None = None
    type: str | None = None
    points: float | None = None
    rating: int | None = None
    # tags: list[str] | None = None
