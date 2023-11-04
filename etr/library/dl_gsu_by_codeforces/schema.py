from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict


class StudentSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    first_name: str | None = None
    last_name: str | None = None
    handle: str = Field(alias="nick_name")
    organization: str | None = Field(default=None, alias="school_name")
    grade: int | None = None
