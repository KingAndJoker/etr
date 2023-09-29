"""Contest schema"""
from pydantic import BaseModel, ConfigDict, Field


class ContestSchema(BaseModel):
    """Contest schema"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int = Field(alias="contestId")
    name: str = Field(alias="contestName")
    type: str | None = None
    phase: str | None = None
    frozen: bool | None = None
    duration_seconds: int | None = Field(default=None, alias="durationSeconds")
    start_time_seconds: int | None = Field(
        default=None,
        alias="startTimeSeconds"
    )
    relative_time_seconds: int | None = Field(
        default=None,
        alias="relativeTimeSeconds"
    )
    prepared_by: str | None = Field(default=None, alias="preparedBy")
    website_url: str | None = Field(default=None, alias="websiteUrl")
    description: str | None = None
    difficulty: int | None = None
    kind: str | None = None
    icpc_region: str | None = Field(default=None, alias="icpcRegion")
    country: str | None = None
    city: str | None = None
    season: str | None = None
