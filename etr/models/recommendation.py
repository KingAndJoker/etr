"""User models"""
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from etr.models.base import Base
from etr.models.user import UserOrm
from etr.models.problem import ProblemOrm


class RecommendationOrm(Base):
    """Recommendation model"""

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    problem_id: Mapped[int] = mapped_column(Integer, ForeignKey("problems.id"))
    problem: Mapped[ProblemOrm] = relationship(
        "ProblemOrm",
        backref="recommendations",
        lazy="selectin"
    )
    user_id: Mapped[int] = Column(
        "author_id",
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )
    user: Mapped[UserOrm] = relationship(
        "UserOrm",
        backref="recommendations",
        lazy="selectin"
    )
