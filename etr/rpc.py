"""Remote Procedure Call module"""
from threading import Thread

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import text

from etr import config
from etr.services.problem import add_missing_problem_with_contest
from etr.services.problem import add_tag_for_problem
from etr.services.problem import update_tags_in_problem_of_contest
from etr.services.contest import update_contest_with_codeforces
from etr.services.contest import update_students_cf_submissions
from etr.services.contest import get_contests
from etr.services.submission import update_submissions_with_codeforces
from etr.services.user import sync_user_with_dl
from etr.library.codeforces.codeforces_utils import (
    get_contest as get_codeforces_contest,
)
from etr import db
from etr.utils.codeforces.convert import convert_codeforces_problems_schema


router = APIRouter()


@router.get("/contest/{contest_id}")
def update_contest_info(contest_id: int):
    contest_schema = update_contest_with_codeforces(contest_id)

    return contest_schema


@router.get("/submission/{contest_id}")
def update_submission_info(contest_id: int):
    """update submissions with codeforces in db"""

    # TODO: write update submissions for specific user
    Thread(target=update_submissions_with_codeforces,
           args=(contest_id,)).start()

    return {"status": "ok"}


@router.get("/problem/update_tag")
def update_tag_codeforces():
    contests = get_contests()
    for contest in contests:
        if not contest.type_of_source.startswith("codeforces"):
            continue
        codeforces_contest = get_codeforces_contest(contest.id)
        cf_problems = convert_codeforces_problems_schema(
            codeforces_contest.problems)
        for problem in contest.problems:
            [cf_problem] = [
                cf_problem
                for cf_problem in cf_problems
                if cf_problem.index == problem.index
            ]
            cf_tags = cf_problem.tags
            for cf_tag in cf_tags:
                add_tag_for_problem(problem_id=problem.id, tag=cf_tag)
    return {"status": "ok"}


@router.get("/problem/{contest_id}")
def update_missing_problems(contest_id: int):
    added_problems = add_missing_problem_with_contest(contest_id)
    return added_problems


@router.get("/user/swdl")
def sync_with_dl():
    try:
        sync_user_with_dl()
    except Exception as exp:
        raise

    return {"status": "ok"}


@router.get("/sql_exec/")
def sql_exec(sql: str, password: str) -> list[dict]:
    """Метод позволяет выполнять SQL запросы для быстрого решение проблем

    Args:

        sql (str): SQL скрипт

    Returns:

        list[dict]: результат выполнения запроса от СУБД
    """
    if config.SQL_PASSWORD != password:
        raise HTTPException(403, "Forbidden. Wrong password.")
    response = []
    with db.engine.connect() as connection:
        result = connection.execute(text(sql))
        if not sql.lower().startswith("delete"):
            response = result.mappings().all()
        connection.commit()
    return response


@router.get("/contest/update_cf_student/")
def update_submissions_of_student_from_cf(handle: str, contest_id: int):
    submissions = update_students_cf_submissions(handle, contest_id)
    return submissions


@router.get("/problem/update_tag/{contest_id}")
def update_tags(contest_id: int):
    problems = update_tags_in_problem_of_contest(contest_id)
    return problems
