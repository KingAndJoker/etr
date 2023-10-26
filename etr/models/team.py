"""team model"""
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from etr.models.base import Base
from etr.models.user import User


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
    # TODO: rename to team_name
    teamName: Mapped[str] = mapped_column(type_=String(255))

    users: Mapped[list[User]] = relationship(secondary=teams_users, lazy="selectin")
    submissions: Mapped[list["Submission"]] = relationship("Submission", back_populates="team")
