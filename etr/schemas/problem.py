"""Problem schema"""
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    validator
)

from etr.models.problem import Tag


class ProblemSchema(BaseModel):
    """Problem schema"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int | None = None
    contest_id: int | None = None
    problemset_name: str | None = None
    index: str
    name: str | None = None
    type: str | None = None
    points: float | None = None
    rating: int | None = None
    tags: list[str] | None = None

    @validator("tags", pre=True)
    def check_tags(cls, tags: list[Tag] | list[str]):
        """Check tags"""
        if len(tags) == 0:
            return tags
        if isinstance(tags[0], str):
            return tags
        return [
            tag.tag
            for tag in tags
        ]
