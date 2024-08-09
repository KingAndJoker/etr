from loguru import logger

from etr import db
from etr.models.problem import TagOrm


@logger.catch(reraise=True)
def create_tag(tag: str) -> str:
    logger.info(f"создаем тег {tag=}")
    with db.SessionLocal() as session:
        tag_orm = TagOrm(tag=tag)
        session.add(tag_orm)
        session.commit()
    return tag


def get_tag_by_name(tag: str) -> str | None:
    logger.info(f"хочу получить экземпляр из базы данных тега {tag=}")
    with db.SessionLocal() as session:
        tag_orm = session.query(TagOrm).filter_by(tag=tag).one_or_none()
        if tag_orm is None:
            return None
        return tag_orm.tag


def get_tags() -> list[str]:
    logger.info("получаю все теги")
    with db.SessionLocal() as session:
        tags = session.query(TagOrm).all()
        return [tag.tag for tag in tags]
