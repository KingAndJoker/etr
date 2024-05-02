"""Recommendation schema file"""
from pydantic import BaseModel, ConfigDict

from etr.schemas.user import UserSchema
from etr.schemas.problem import ProblemSchema


class RecommendationSchema(BaseModel):
    """Recommendation pydantic schema"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int | None = None
    user: UserSchema
    problem: ProblemSchema


class RecommendationResponseSchema(BaseModel):
    """Recommendation pydantic schema"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int | None = None
    problem: ProblemSchema
