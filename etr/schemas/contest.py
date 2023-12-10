"""Contest schema"""
import datetime
from pydantic import BaseModel, ConfigDict, Field, computed_field

from etr.schemas.problem import ProblemSchema


class ContestSchema(BaseModel):
    """Contest schema"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int
    name: str
    type: str | None = None
    phase: str | None = None
    frozen: bool | None = None
    duration_seconds: int | None = None
    start_time_seconds: int | None = None
    relative_time_seconds: int | None = None
    prepared_by: str | None = None
    website_url: str | None = None
    description: str | None = None
    difficulty: int | None = None
    kind: str | None = None
    icpc_region: str | None = None
    country: str | None = None
    city: str | None = None
    season: str | None = None

    problems: list[ProblemSchema] | None = None

    url: str | None = None
    type_of_source: str | None = None
    type_of_contest: str | None = None

    @computed_field
    @property
    def duration_time(self) -> str | None:
        if self.duration_seconds:
            return str(datetime.timedelta(seconds=self.duration_seconds))
        return None

    @computed_field
    @property
    def start_datatime(self) -> str | None:
        if self.start_time_seconds:
            utc_time = datetime.datetime.fromtimestamp(self.start_time_seconds, datetime.timezone.utc)
            local_time = utc_time.astimezone()
            return local_time.strftime("%d %m %Y %H:%M:%S")
        return None


class ContestUrl(BaseModel):
    protocol: str
    host: str
    port: str | None = None
    path: str
    params: str | None = None
