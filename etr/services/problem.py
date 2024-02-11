from etr.crud.problem import *
from etr.crud.tag import get_tag_by_name
from etr.crud.tag import create_tag
from etr.models.problem import TagOrm


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


def update_tag_by_problem(problem_id: int, tag: str):
    with db.SessionLocal() as session:
        problem_orm = session.query(ProblemOrm).filter_by(id=problem_id).one_or_none()
        tag_orm = session.query(TagOrm).filter_by(tag=tag).one_or_none()
        if problem_orm is None or tag_orm is None:
            return
        problem_orm.tags.append(tag_orm)
        session.add(problem_orm)
        session.commit()


def add_tag_for_problem(problem_id: int, tag: str):
    if get_tag_by_name(tag) is None:
        create_tag(tag)
    update_tag_by_problem(problem_id, tag)


def update_tags_in_problem_of_contest(contest_id: int) -> list[ProblemSchema]:
    cf_problems = convert_codeforces_problems_schema(
        get_problem_with_contest(contest_id)
    )
    problems: list[ProblemSchema] = []
    for cf_problem in cf_problems:
        problem = get_problem(**cf_problem.model_dump())
        if problem is None:
            continue
        for tag in cf_problem.tags:
            if not tag in problem.tags:
                add_tag_for_problem(problem.id, tag)

        problem = get_problem(**cf_problem.model_dump())
        problems.append(problem)

    return problems
