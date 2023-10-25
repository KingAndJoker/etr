from etr.utils.codeforces.convert import convert_codeforces_problems_schema
from etr.utils.factory import create_problem_model
from etr.library.codeforces.codeforces_utils import get_problem_with_contest
from etr.db import get_db
from etr.models.problem import Problem
from etr.schemas.problem import ProblemSchema
from etr.utils.factory import create_problem_model


def _add_problem_schema_to_db(problem_schema: ProblemSchema) -> ProblemSchema | None:
    """ add problem schema to db """

    problem = create_problem_model(**problem_schema.model_dump())
    if problem is None:
        return None

    try:
        with get_db() as session:
            session.add(problem)
            session.commit()
    except:
        return None

    return problem_schema


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
        problems = session.query(Problem).filter(
            Problem.contest_id == contest_id
        ).all()

        # TODO: Bad code
        # code should work without this loop
        for i, _ in enumerate(problems):
            problems[i].tags = [tag.tag for tag in problems[i].tags]

    problems = [
        ProblemSchema.model_validate(problem).model_dump()
        for problem in problems
    ]

    return problems


def _is_missing_problem(problemSchema: ProblemSchema, contest_id: int) -> bool:
    """ return True if no the task in contest, else False """

    with get_db() as session:
        problem_db = session.query(Problem).filter_by(
            contest_id=contest_id,
            index=problemSchema.index
        ).one_or_none()

    return problem_db is None


def add_missing_problem_with_contest(contest_id: int) -> list[dict]:
    """ add missing problem to db. Return list of added problems. """

    problems_schema = convert_codeforces_problems_schema(
        get_problem_with_contest(contest_id)
    )

    added_problems_schema: list[ProblemSchema] = list()

    for problem_schema in problems_schema:
        if _is_missing_problem(problem_schema, contest_id):
            problem_schema_returned = _add_problem_schema_to_db(problem_schema)
            if problem_schema_returned is not None:
                added_problems_schema.append(problem_schema_returned)
        else:
            pass

    return None
