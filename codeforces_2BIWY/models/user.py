"""User models"""
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codeforces_2BIWY.models.base import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    handle: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(nullable=True)
    vk_id: Mapped[str] = mapped_column(nullable=True)
    open_id: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    organization: Mapped[str] = mapped_column(nullable=True)
    rank: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[str] = mapped_column(nullable=True)
    max_rank: Mapped[str] = mapped_column(nullable=True)
    max_rating: Mapped[str] = mapped_column(nullable=True)
    last_online_time_seconds: Mapped[int] = mapped_column(nullable=True)
    registration_time_seconds: Mapped[int] = mapped_column(nullable=True)
    friend_of_count: Mapped[int] = mapped_column(nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True)
    title_photo: Mapped[str] = mapped_column(nullable=True)

    watch: Mapped[bool] = mapped_column(default=True)  # Update user info?

    teams: Mapped[list["Team"]] = relationship(secondary="teams_users")
