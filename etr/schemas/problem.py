"""Problem schema"""
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    validator
)

from etr.models.problem import TagOrm


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
    tags: list[str] = []

    @validator("tags", pre=True)
    def check_tags(cls, tags: list[TagOrm] | list[str]):
        """Check tags"""
        if len(tags) == 0:
            return tags
        if isinstance(tags[0], str):
            return tags
        return [
            tag.tag
            for tag in tags
        ]


class ProblemSchemaFrozen(ProblemSchema):
    model_config = ConfigDict(frozen=True)
    tags: tuple[str, ...] | None = None


class VerdictType(str, Enum):
    FAILED = "FAILED"
    OK = "OK"
    PARTIAL = "PARTIAL"
    COMPILATION_ERROR = "COMPILATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    WRONG_ANSWER = "WRONG_ANSWER"
    PRESENTATION_ERROR = "PRESENTATION_ERROR"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    IDLENESS_LIMIT_EXCEEDED = "IDLENESS_LIMIT_EXCEEDED"
    SECURITY_VIOLATED = "SECURITY_VIOLATED"
    CRASHED = "CRASHED"
    INPUT_PREPARATION_CRASHED = "INPUT_PREPARATION_CRASHED"
    CHALLENGED = "CHALLENGED"
    SKIPPED = "SKIPPED"
    TESTING = "TESTING"
    REJECTED = "REJECTED"
