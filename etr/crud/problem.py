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


def _get_problems_db_with_contest_id(contest_id: int) -> ProblemOrm:
    with db.SessionLocal() as session:
        problems = session.query(ProblemOrm).filter(
            ProblemOrm.contest_id == contest_id
        ).all()

        for i, _ in enumerate(problems):
            problems[i].tags = [tag.tag for tag in problems[i].tags]

    return problems


def get_problems_with_contest_id(contest_id: int) -> list[ProblemSchema] | None:
    """ get problems with contest id """

    problems_db = _get_problems_db_with_contest_id(contest_id)

    problems = [
        ProblemSchema.model_validate(problem_db)
        for problem_db in problems_db
    ]

    return problems


def _is_missing_problem(problemSchema: ProblemSchema, contest_id: int) -> bool:
    """ return True if no the task in contest, else False """

    with db.SessionLocal() as session:
        problem_db = session.query(ProblemOrm).filter_by(
            contest_id=contest_id,
            index=problemSchema.index
        ).one_or_none()

    return problem_db is None


def add_missing_problem_with_contest(contest_id: int) -> list[ProblemSchema]:
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

    return added_problems_schema


def __get_problems(session: Session, **kwargs) -> list[ProblemOrm]:
    problems = session.query(ProblemOrm).filter_by(**kwargs).all()
    return problems


def _get_problems(**kwargs):
    with db.SessionLocal() as session:
        problems = __get_problems(session, **kwargs)
        for i, _ in enumerate(problems):
            problems[i].tags = [tag.tag for tag in problems[i].tags]
        problems = [ProblemSchema.model_validate(problem) for problem in problems]
    return problems


def get_problems(**kwargs) -> list[ProblemSchema]:
    problems = _get_problems(**kwargs)
    return problems