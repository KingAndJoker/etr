"""User models"""
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from etr.models.base import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    handle: Mapped[str] = Column("handle", unique=True, type_=String(255))
    email: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    vk_id: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    open_id: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    first_name: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    last_name: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    country: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    city: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    organization: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    rank: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    # TODO: type of raing is int
    rating: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    max_rank: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    # TODO: type of rating is int
    max_rating: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    last_online_time_seconds: Mapped[int] = mapped_column(nullable=True)
    registration_time_seconds: Mapped[int] = mapped_column(nullable=True)
    friend_of_count: Mapped[int] = mapped_column(nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    title_photo: Mapped[str] = mapped_column(nullable=True, type_=String(255))

    watch: Mapped[bool] = mapped_column(default=True)  # Update user info?
    grade: Mapped[int] = mapped_column(nullable=True, default=None)

    teams: Mapped[list["Team"]] = relationship(secondary="teams_users", lazy="selectin")
    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="author"
    )
