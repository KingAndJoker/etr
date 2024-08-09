from loguru import logger

from etr import db
from etr.crud.problem import *
from etr.crud.tag import get_tag_by_name
from etr.crud.tag import create_tag
from etr.crud.contest import get_contests
from etr.models.problem import ProblemOrm, TagOrm
from etr.library.codeforces import problemset
from etr.utils.codeforces.convert import convert_codeforces_problems_schema
from etr.utils.codeforces.convert import convert_codeforces_problems_statistics


@logger.catch(reraise=True)
def add_missing_problem_with_contest(contest_id: int) -> list[ProblemSchema]:
    """функция добавляет отсутствующие задачи

    Args:
        contest_id (int): id соревнования

    Returns:
        list[ProblemSchema]: список добавленных задач
    """
    logger.info(f"добавляю отсутствующие задачи для {contest_id=}")
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


@logger.catch(reraise=True)
def update_tag_by_problem(problem_id: int, tag: str):
    """процедура обновляет теги у задач

    Args:
        problem_id (int): id задачи из базы данных
        tag (str): новый тег
    """
    with db.SessionLocal() as session:
        problem_orm = session.query(ProblemOrm).filter_by(
            id=problem_id
        ).one_or_none()
        tag_orm = session.query(TagOrm).filter_by(tag=tag).one_or_none()
        if problem_orm is None or tag_orm is None:
            return
        problem_orm.tags.append(tag_orm)
        session.add(problem_orm)
        session.commit()


@logger.catch(reraise=True)
def add_tag_for_problem(problem_id: int, tag: str):
    """функция создает новый тег (если его нету) и добавляет к задаче

    Args:
        problem_id (int): _description_
        tag (str): _description_
    """
    if get_tag_by_name(tag) is None:
        create_tag(tag)
    update_tag_by_problem(problem_id, tag)


@logger.catch(reraise=True)
def update_missing_tags_for_problems():
    """функция добавляет отсутствующие теги у задач
    """
    contests = get_contests()
    for contest in contests:
        for problem in contest.problems:
            if problem.tags == []:
                update_tags_in_problem_of_contest(contest.id)
                break


@logger.catch(reraise=True)
def update_tags_in_problem_of_contest(contest_id: int) -> list[ProblemSchema]:
    """обновляет теги для соревнования

    Args:
        contest_id (int): id соревнования

    Returns:
        list[ProblemSchema]: список задач с новыми тегами
    """
    logger.info(f"хочу обновить теги задач из {contest_id=}")
    cf_problems = convert_codeforces_problems_schema(
        get_problem_with_contest(contest_id)
    )
    problems: list[ProblemSchema] = []
    for cf_problem in cf_problems:
        problem = get_problem(index=cf_problem.index, contest_id=contest_id)
        if problem is None:
            continue
        for tag in cf_problem.tags:
            if not tag in problem.tags:
                add_tag_for_problem(problem.id, tag)

        problem = get_problem(index=cf_problem.index, contest_id=contest_id)
        problems.append(problem)

    return problems


@logger.catch(reraise=True)
def update_solved_count():
    """функция обновляет статистику решений с сайта codeforces по каждой задаче
    """
    _, problems_statistics_codeforces = problemset.problems()
    problems_statistics = convert_codeforces_problems_statistics(
        problems_statistics_codeforces
    )

    with db.SessionLocal() as session:  # неправильно, но зато быстро
        for problem_statistics in problems_statistics:
            if problem_statistics.contest_id is not None:
                problem_orm = session.query(ProblemOrm).filter_by(
                    contest_id=problem_statistics.contest_id,
                    index=problem_statistics.index
                ).one_or_none()
                if problem_orm is not None:
                    problem_orm.solved_count = problem_statistics.solved_count
                    session.add(problem_orm)
        session.commit()
