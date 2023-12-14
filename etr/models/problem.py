"""problem model"""
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from etr.db import Base


# Table of associations between problem and tag
problems_tags = Table(
    "problems_tags",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id")),
    Column("problem_id", Integer, ForeignKey("problems.id"))
)


class TagOrm(Base):
    """Tag model"""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(type_=String(255), unique=True)
    problems: Mapped[list["ProblemOrm"]] = relationship(
        "ProblemOrm",
        secondary=problems_tags,
        back_populates="tags"
    )


class ProblemOrm(Base):
    """problem (aka task) model"""

    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contest_id: Mapped[int] = Column(
        "contest_id",
        Integer,
        ForeignKey("contests.id"),
        nullable=True
    )
    problemset_name: Mapped[str] = mapped_column(
        nullable=True,
        type_=String(255)
    )
    index: Mapped[str] = mapped_column(type_=String(255))
    name: Mapped[str] = mapped_column(type_=String(255))
    type: Mapped[str] = mapped_column(nullable=True, type_=String(255))
    points: Mapped[float] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)
    tags: Mapped[list[TagOrm]] = relationship(
        "TagOrm",
        secondary=problems_tags,
        back_populates="problems",
        lazy="selectin"
    )

    submissions: Mapped[list["SubmissionOrm"]] = relationship(
        "SubmissionOrm",
        back_populates="problem"
    )
