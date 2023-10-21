from etr.utils.codeforces.convert import convert_codeforces_problems_schema
from etr.utils.factory import create_problem_model
from etr.library.codeforces.codeforces_utils import get_problem_with_contest
from etr.db import get_db
from etr.models.problem import Problem
from etr.schemas.problem import ProblemSchema



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


def get_problems_with_contest_id(contest_id: int) -> list[dict] | None:
    """ get problems with contest id """
    with get_db() as session:
        problems = session.query(Problem).filter(Problem.contest_id == contest_id).all()

        # TODO: Bad code
        # code should work without this loop
        for i, _ in enumerate(problems):
            problems[i].tags = [tag.tag for tag in problems[i].tags]

    problems = [
        ProblemSchema.model_validate(problem).model_dump()
        for problem in problems
    ]

    return problems
