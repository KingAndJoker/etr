from etr.crud.problem import *


def add_missing_problem_with_contest(contest_id: int) -> list[ProblemSchema]:
    """ add missing problem to db. Return list of added problems. """

    problems_schema = convert_codeforces_problems_schema(
        get_problem_with_contest(contest_id)
    )

    added_problems_schema: list[ProblemSchema] = list()

    for problem_schema in problems_schema:
        if is_missing_problem(problem_schema, contest_id):
            problem_schema_returned = add_problem(problem_schema)
            if problem_schema_returned is not None:
                added_problems_schema.append(problem_schema_returned)
        else:
            pass

    return added_problems_schema
