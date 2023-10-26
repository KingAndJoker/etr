""" contest services """
from etr.db import get_db
from etr.schemas.contest import ContestSchema
from etr.models.contest import Contest
from etr.library.codeforces.codeforces_utils import get_contest
from etr.utils.codeforces.convert import convert_codeforces_contest_schema
from etr.services.problem import add_problems
from etr.utils.factory import create_contest_model


def add_contest(contest_id: int) -> ContestSchema:
    """ add contest with contest_id """

    contest_schema = convert_codeforces_contest_schema(
        get_contest(contest_id=contest_id)
    )

    with get_db() as session:
        contest = create_contest_model(**contest_schema.model_dump()) # Contest(**contest_schema.model_dump())
        session.add(contest)

        session.commit()

    problems_schema = add_problems(contest_id)
    contest_schema.problems = problems_schema

    return contest_schema


def get_contest_with_db(contest_id: int) -> Contest:
    with get_db() as session:
        contest_db = session.query(Contest).filter_by(
            id=contest_id
        ).one_or_none()
    
    return contest_db


def _update_contest_model_fields(contest: Contest, **kwargs) -> Contest:
    for field, value in kwargs.items():
        setattr(contest, field, value)
    
    return contest


def update_contest(contest_id: int) -> ContestSchema | None:
    contest_schema = convert_codeforces_contest_schema(
        get_contest(contest_id)
    )

    if contest_schema is None:
        return None
    
    contest_db = get_contest_with_db(contest_id)

    if contest_db is None:
        contest_db = create_contest_model(**contest_schema.model_dump())
    else:
        contest_db = _update_contest_model_fields(contest_db, **contest_schema.model_dump())

    return contest_schema
