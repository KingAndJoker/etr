""" contest services """
from etr.db import get_db
from etr.schemas.contest import ContestSchema
from etr.models.contest import Contest
from etr.models.problem import Problem
from etr.library.codeforces.codeforces_utils import get_contest, get_problem_with_contest
from etr.utils.codeforces.convert import (
    convert_codeforces_contest_schema,
    convert_codeforces_problems_schema
)


def add_contest(contest_id: int) -> ContestSchema:
    """ add contest with contest_id """

    contest_schema = convert_codeforces_contest_schema(
        get_contest(contest_id=contest_id)
    )
    problems_schema = convert_codeforces_problems_schema(
        get_problem_with_contest(contest_id)
    )

    with get_db() as session:
        contest = Contest(**contest_schema.model_dump())
        session.add(contest)

        problems = [
            Problem(**problem_schema.model_dump())
            for problem_schema in problems_schema
        ]
        session.add_all(problems)

        session.commit()

    return contest_schema
