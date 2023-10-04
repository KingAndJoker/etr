"""problem model"""
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from etr.models.base import Base


# Table of associations between problem and tag
problems_tags = Table(
    "problems_tags",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id")),
    Column("problem_id", Integer, ForeignKey("problems.id"))
)


class Tag(Base):
    """Tag model"""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(type_=String(255))
    problems: Mapped[list["Problem"]] = relationship(
        "Problem",
        secondary=problems_tags,
        back_populates="tags"
    )


class Problem(Base):
    """problem (aka task) model"""

    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contest_id: Mapped[int] = mapped_column(nullable=True)
    problemset_name: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    index: Mapped[str] = mapped_column(type_=String(255))
    name: Mapped[str] = mapped_column(type_=String(255))
    type: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    points: Mapped[float] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)
    tags: Mapped[list[str]] = relationship(
        "Tag",
        secondary=problems_tags,
        back_populates="problems"
    )

    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="problem"
    )