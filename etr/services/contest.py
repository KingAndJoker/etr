""" contest services """
from sqlalchemy.orm import Session

from etr.db import get_db
from etr.schemas.contest import ContestSchema
from etr.models.contest import ContestOrm
from etr.library.codeforces.codeforces_utils import get_contest as get_contest_with_codeforces
from etr.services.problem import add_problems
from etr.services.user import get_users
from etr.services.team import get_teams_with_handle_member
from etr.services.submission import get_submissions
from etr.utils.factory import create_contest_model
from etr.utils.codeforces.convert import convert_codeforces_contest_schema


def __get_contests_db(session: Session, **kwargs) -> list[ContestOrm] | None:
    """ get contest from db """
    contest_db = session.query(
        ContestOrm
    ).filter_by(
        **kwargs
    ).order_by(
        ContestOrm.start_time_seconds.desc()
    ).all()

    return contest_db


def __update_contest_db(session: Session, contest: ContestOrm, **kwargs) -> ContestOrm:
    """ update contest in db """
    for field, value in kwargs.items():
        setattr(contest, field, value)
    session.add(contest)
    session.commit()

    contest = session.query(ContestOrm).filter_by(id=contest.id).one()

    return contest


def __add_contest_db(session: Session, contest_schema: ContestSchema) -> ContestOrm:
    """ add contest to db """
    contest_db = create_contest_model(**contest_schema.model_dump())
    session.add(contest_db)
    session.commit()

    return contest_db


def _get_contests_schema_with_db(**kwargs) -> list[ContestSchema]:
    """ get contest from db """
    with get_db() as session:
        contests_db = __get_contests_db(session, **kwargs)
        for contest_db in contests_db:
            contest_db.problems

        contests_schema = [
            ContestSchema.model_validate(contest_db)
            for contest_db in contests_db
        ]

    return contests_schema


def _get_contest_with_codeforces(contest_id: int) -> ContestSchema | None:
    """ get contest from codeforces """
    contest_schema = convert_codeforces_contest_schema(
        get_contest_with_codeforces(contest_id)
    )
    return contest_schema


def _add_contest_db(contest_schema: ContestSchema) -> ContestSchema:
    """ add contest to db """
    with get_db() as session:
        contest_db = __add_contest_db(session, contest_schema)
        contest_schema_return = ContestSchema.model_validate(contest_db)

    return contest_schema_return


def _update_contest(contest_schema: ContestSchema, **kwargs) -> ContestSchema:
    """ update contest """
    with get_db() as session:
        contest_db = __get_contests_db(session, id=contest_schema.id)[0]
        contest_db = __update_contest_db(session, contest_db, **kwargs)
        contest_schema_return = ContestSchema.model_validate(contest_db)

    return contest_schema_return


def get_contests(**kwargs) -> list[ContestSchema]:
    """ get contests """
    contests_schema = _get_contests_schema_with_db(**kwargs)

    return contests_schema


def add_contest(contest_id: int) -> ContestSchema:
    """ add contest with contest_id """

    contests_schema = _get_contests_schema_with_db(id=contest_id)

    if len(contests_schema) > 0:
        return contests_schema[0]

    contest_schema = _get_contest_with_codeforces(contest_id)

    contest_schema = _add_contest_db(contest_schema)

    problems_schema = add_problems(contest_id)
    contest_schema.problems = problems_schema

    return contest_schema


def add_contest_with_schema(contest: ContestSchema) -> ContestSchema:
    contest_schema = _add_contest_db(contest)
    # TODO: rewrite problems get to event
    problems_schema = add_problems(contest_schema.id)
    contest_schema.problems = problems_schema

    return contest_schema


def update_contest_with_codeforces(contest_id: int) -> ContestSchema | None:
    contest_cf_schema = _get_contest_with_codeforces(contest_id)

    if contest_cf_schema is None:
        return None

    contest_schema = _get_contests_schema_with_db(id=contest_id)
    if contest_schema is None:
        return None

    contest_schema = _update_contest(
        contest_schema, **contest_cf_schema.model_dump())

    return contest_schema


def get_contest_table_rows(contest_id: int) -> list:
    # TODO: write tests
    rows = list()

    users = get_users()

    # TODO: rewrite, if user is contestant, but he has no submissions
    for user in users:
        submissions = get_submissions(contest_id=contest_id, author_id=user.id)
        if len(submissions):
            rows.append({
                "user": user,
                "submissions": submissions
            })

        teams = get_teams_with_handle_member(handle=user.handle)
        for team in teams:
            if team in (row.get("team", None) for row in rows):
                continue
            submissions = get_submissions(contest_id=contest_id, team_id=team.id)
            if len(submissions) == 0:
                continue
            rows.append({
                "team": team,
                "submissions": submissions
            })

    return rows


def update_contest(contest_id: int, **kwargs):
    contests = get_contests(id=contest_id)
    if contests == []:
        return None
    contest = contests[0]
    contest = _update_contest(contest, **kwargs)
    return contest
