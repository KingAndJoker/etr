"""team model"""
from sqlalchemy import (
    Table,
    Column,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from codeforces_2BIWY.models.base import Base
from codeforces_2BIWY.models.user import User


teams_users = Table(
    "teams_users",
    Base.metadata,
    Column("team_id", ForeignKey("teams.id")),
    Column("user_id", ForeignKey("users.id"))
)


class Team(Base):
    """ Team model """

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    teamName: Mapped[str] = mapped_column()

    users: Mapped[list[User]] = relationship(secondary=teams_users)
