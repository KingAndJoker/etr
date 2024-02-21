from sqlalchemy.orm import Session

from etr import db
from etr.models.contest import ContestOrm
from etr.schemas.contest import ContestSchema
from etr.utils.factory import create_contest_model


def __get_contests_db(
    session: Session,
    contest_index: int | None = None,
    contest_count: int | None = None,
    **kwargs
) -> list[ContestOrm] | None:
    """get contest from db"""
    contest_db = (
        session.query(ContestOrm)
        .filter_by(**kwargs)
        .order_by(ContestOrm.start_time_seconds.desc())
    )
    if contest_index is not None:
        contest_db = contest_db.offset(contest_index)
    if contest_count is not None:
        contest_db = contest_db.limit(contest_count)
    return contest_db.all()


def __update_contest_db(session: Session, contest: ContestOrm, **kwargs) -> ContestOrm:
    """update contest in db"""
    for field, value in kwargs.items():
        setattr(contest, field, value)
    session.add(contest)
    session.commit()
    return session.query(ContestOrm).filter_by(id=contest.id).one()


def __add_contest_db(session: Session, contest_schema: ContestSchema) -> ContestOrm:
    """add contest to db"""
    contest_db = create_contest_model(**contest_schema.model_dump())
    session.add(contest_db)
    session.commit()
    return contest_db


def _get_contests_schema_with_db(**kwargs) -> list[ContestSchema]:
    """get contest from db"""
    with db.SessionLocal() as session:
        contests_db = __get_contests_db(session, **kwargs)
        for contest_db in contests_db:
            contest_db.problems

        contests_schema = [
            ContestSchema.model_validate(contest_db) for contest_db in contests_db
        ]

    return contests_schema


def _add_contest_db(contest_schema: ContestSchema) -> ContestSchema:
    """add contest to db"""
    with db.SessionLocal() as session:
        contest_db = __add_contest_db(session, contest_schema)
        return ContestSchema.model_validate(contest_db)


def _update_contest(contest_schema: ContestSchema, **kwargs) -> ContestSchema:
    """update contest"""
    with db.SessionLocal() as session:
        contest_db = __get_contests_db(session, id=contest_schema.id)[0]
        contest_db = __update_contest_db(session, contest_db, **kwargs)
        contest_schema_return = ContestSchema.model_validate(contest_db)
    return contest_schema_return


def get_contests(**kwargs) -> list[ContestSchema]:
    """get contests"""
    contests_schema = _get_contests_schema_with_db(**kwargs)

    return contests_schema


def add_contest_with_schema(contest: ContestSchema) -> ContestSchema:
    contest_schema = _add_contest_db(contest)

    return contest_schema


def update_contest(contest_id: int, **kwargs):
    contests = get_contests(id=contest_id)
    if contests == []:
        return None
    contest = contests[0]
    contest = _update_contest(contest, **kwargs)
    return contest


def delete_contest(contest_id: int) -> ContestSchema | None:
    with db.SessionLocal() as session:
        contest_orm = session.query(ContestOrm).filter_by(id=contest_id).one_or_none()
        if contest_orm is None:
            return None
        contest = ContestSchema.model_validate(contest_orm)
        session.delete(contest_orm)
        session.commit()
    return contest
