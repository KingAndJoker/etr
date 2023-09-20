""" User models """
from sqlalchemy.orm import Mapped, mapped_column
from codeforces_2BIWY.models.base import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    handler: Mapped[str] = mapped_column(nullable=False)
