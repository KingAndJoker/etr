from etr.utils.codeforces.convert import convert_codeforces_problems_schema
from etr.utils.factory import create_problem_model
from etr.library.codeforces.codeforces_utils import get_problem_with_contest
from etr.db import get_db
from etr.models.problem import Problem



def add_problems(contest_id: int):
    """ add contest problems to db """
    problems_schema = convert_codeforces_problems_schema(
        get_problem_with_contest(contest_id)
    )

    with get_db() as session:
        problems = [
            create_problem_model(**problem_schema.model_dump())
            for problem_schema in problems_schema
        ]
        session.add_all(problems)

        session.commit()

    return problems_schema
