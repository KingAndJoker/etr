from etr import db
from etr.models.problem import TagOrm


def create_tag(tag: str) -> str:
    with db.SessionLocal() as session:
        tag_orm = TagOrm(tag=tag)
        session.add(tag_orm)
        session.commit()
    return tag


def get_tag_by_name(tag: str) -> str | None:
    with db.SessionLocal() as session:
        tag_orm = session.query(TagOrm).filter_by(tag=tag).one_or_none()
        if tag_orm is None:
            return None
        return tag_orm.tag
