"""User models"""
from sqlalchemy.orm import Mapped, mapped_column, relationship


from codeforces_2BIWY.models.base import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    handle: Mapped[str] = mapped_column(nullable=False)

    teams: Mapped[list["Team"]] = relationship(secondary="teams_users")
