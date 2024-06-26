from sqlalchemy.orm import Session

from etr import db
from etr.library.codeforces.codeforces_utils import get_problem_with_contest
from etr.models.problem import ProblemOrm
from etr.schemas.problem import ProblemSchema
from etr.utils.factory import create_problem_model
from etr.utils.codeforces.convert import convert_codeforces_problems_schema
from etr.utils.factory import create_problem_model


def _add_problem_schema_to_db(problem_schema: ProblemSchema) -> ProblemSchema | None:
    """ add problem schema to db """
    with db.SessionLocal() as session:
        problem = create_problem_model(**problem_schema.model_dump())
        if problem is None:
            return None

        session.add(problem)
        session.commit()

    return problem_schema


def add_problems_with_cf(contest_id: int) -> list[ProblemSchema]:
    """ add contest problems to db """
    problems_schema = convert_codeforces_problems_schema(
        get_problem_with_contest(contest_id)
    )

    added_problems_schema: list[ProblemSchema] = list()

    for problem_schema in problems_schema:
        problem_schema_returned = _add_problem_schema_to_db(problem_schema)
        if problem_schema_returned is not None:
            added_problems_schema.append(problem_schema_returned)

    return added_problems_schema


def _get_problems_db_with_contest_id(contest_id: int) -> list[ProblemSchema]:
    problems = []
    with db.SessionLocal() as session:
        problems_orm = __get_problems(session, contest_id=contest_id)
        for problem_orm in problems_orm:
            problems.append(ProblemSchema.model_validate(problem_orm))
    return problems


def get_problems_with_contest_id(contest_id: int) -> list[ProblemSchema] | None:
    """ get problems with contest id """

    problems_db = _get_problems_db_with_contest_id(contest_id)

    problems = [
        ProblemSchema.model_validate(problem_db)
        for problem_db in problems_db
    ]

    return problems


def is_missing_problem(problemSchema: ProblemSchema, contest_id: int) -> bool:
    """ return True if no the task in contest, else False """

    with db.SessionLocal() as session:
        problem_db = session.query(ProblemOrm).filter_by(
            contest_id=contest_id,
            index=problemSchema.index
        ).one_or_none()

    return problem_db is None


def __get_problems(session: Session, **kwargs) -> list[ProblemOrm]:
    problems = session.query(ProblemOrm).filter_by(**kwargs).all()
    return problems


def _get_problems(**kwargs):
    with db.SessionLocal() as session:
        problems_orm = __get_problems(session, **kwargs)
        problems = [ProblemSchema.model_validate(
            problem) for problem in problems_orm]
        for i, _ in enumerate(problems_orm):
            problems[i].tags = [tag.tag for tag in problems_orm[i].tags]
    return problems


def _fiter_by_tags(tags: list[str], problem: ProblemSchema) -> bool:
    for tag in tags:
        if tag not in problem.tags:
            return False
    return True


def get_problems(tags: list[str] | None = None, **kwargs) -> list[ProblemSchema]:
    problems = _get_problems(**kwargs)
    if tags:
        problems = [
            problem
            for problem in problems
            if _fiter_by_tags(tags=tags, problem=problem)
        ]
    return problems


def __get_problem(session: Session, **kwargs) -> ProblemOrm | None:
    params = kwargs.copy()
    if "id" in params:
        params.pop("id")
    if "tags" in params:
        params.pop("tags")
    return session.query(ProblemOrm).filter_by(**params).one_or_none()


def _get_problem(**kwargs) -> ProblemSchema | None:
    with db.SessionLocal() as session:
        problem_orm = __get_problem(session, **kwargs)
        if problem_orm is None:
            return None
        problem = ProblemSchema.model_validate(problem_orm)
        return problem


def get_problem(**kwargs) -> ProblemSchema | None:
    return _get_problem(**kwargs)


def add_problem(problem: ProblemSchema) -> ProblemSchema:
    _add_problem_schema_to_db(problem)
    problem = get_problems(index=problem.index,
                           contest_id=problem.contest_id)[0]
    return problem


def delete_problems(**kwargs) -> list[ProblemSchema]:
    with db.SessionLocal() as session:
        problems_orm = session.query(ProblemOrm).filter_by(**kwargs).all()
        for problem in problems_orm:
            session.delete(problem)
        problems = [
            ProblemSchema.model_validate(problem)
            for problem in problems_orm
        ]
        session.commit()
    return problems


def get_problems_group_by_rating():
    problems = get_problems()
    group_by_rating: dict[int, list[ProblemSchema]] = dict()
    
    for problem in problems:
        if problem.rating not in group_by_rating:
            group_by_rating[problem.rating] = []
        group_by_rating[problem.rating].append(problem)

    return group_by_rating
