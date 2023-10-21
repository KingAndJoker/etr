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

    return contest_schema
