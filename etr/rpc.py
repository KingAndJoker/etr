"""Remote Procedure Call module"""
from threading import Thread

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import text
from loguru import logger

from etr import config
from etr.services.problem import add_missing_problem_with_contest
from etr.services.problem import add_tag_for_problem
from etr.services.problem import update_tags_in_problem_of_contest
from etr.services.contest import update_contest_with_codeforces
from etr.services.contest import update_students_cf_submissions
from etr.services.contest import get_contests
from etr.services.submission import update_submissions_with_codeforces
from etr.services.submission import update_submissions_for_user_with_codeforces
from etr.services.submission import update_submissions_for_all_users_with_codeforces
from etr.services.user import sync_user_with_dl
from etr.library.codeforces.codeforces_utils import (
    get_contest as get_codeforces_contest,
)
from etr import db
from etr.utils.codeforces.convert import convert_codeforces_problems_schema


router = APIRouter()



@router.get("/contest/{contest_id}")
@logger.catch(reraise=True)
def update_contest_info(contest_id: int):
    """функция обновляет данные о контесте

    Args:
        contest_id (int): id контеста

    Returns:
        _type_: возвращает ContestCchema или None если что-то пошло не так
    """
    logger.info(f"обновляем данные о контесте {contest_id=}")
    contest_schema = update_contest_with_codeforces(contest_id)
    logger.info(f"обновили данные для контеста {contest_id=}")

    return contest_schema


@router.get("/submission/{contest_id}")
@logger.catch(reraise=True)
def update_submission_info(contest_id: int):
    """update submissions with codeforces in db"""

    logger.info(f"создаем поток для обновления посылок для контеста {contest_id=}")
    Thread(target=update_submissions_with_codeforces,
           args=(contest_id,)).start()

    return {"status": "ok"}


@router.get("/submission/user/{handle}")
@logger.catch(reraise=True)
def update_submission_for_user(handle: str, start_with_unix: int = 0):
    """обновить все отправки заданного пользователя

    Запускает поток в котором выполняется вся необходимая работа

    Args:

        handle (str): хендл пользователя

    Returns:

        _type_: возвращает {status: ok}
    """
    logger.info(f"создаем поток для обновления всех отправок для пользователя с {handle=}")
    Thread(target=update_submissions_for_user_with_codeforces,
           args=(handle, start_with_unix)).start()
    return {"status": "ok"}


@router.get("/problem/update_tag")
@logger.catch(reraise=True)
def update_tag_codeforces():
    """функция обновляет теги у всех контестов для задач

    Returns:
        _type_: {"status": "ok"}
    """
    logger.info("обновляем теги у всех задач контестов")
    
    logger.debug("получаем все контесты из базы данных")
    contests = get_contests()
    for contest in contests:
        if not contest.type_of_source.startswith("codeforces"):
            continue
        
        logger.debug(f"проверяю теги для задач контеста {contest.id=}")
        logger.debug(f"пытаюсь получить контест {contest.id=} из Codeforces")
        codeforces_contest = get_codeforces_contest(contest.id)
        cf_problems = convert_codeforces_problems_schema(
            codeforces_contest.problems
        )
        for problem in contest.problems:
            logger.debug(f"обновляю теги для задачи {problem.id=}")
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
@logger.catch(reraise=True)
def update_missing_problems(contest_id: int):
    """функция добавляет отсутствующие задачи в контесте

    Args:
        contest_id (int): id контеста

    Returns:
        _type_: возвращает список отсутствующих задач
    """
    logger.info(f"добавляем отсутствующие контесты для {contest_id=}")
    added_problems = add_missing_problem_with_contest(contest_id)
    return added_problems


@router.get("/user/swdl")
@logger.catch(reraise=True)
def sync_with_dl():
    """функция синхронизирует записи в базе данных с dl.gsu.by

    Returns:
        _type_: {"status": "ok"}
    """
    logger.info("обновляем данные с dl.gsu.by")
    try:
        sync_user_with_dl()
    except Exception as exp:
        raise

    return {"status": "ok"}


@router.get("/sql_exec/")
@logger.catch(reraise=True)
def sql_exec(sql: str, password: str) -> list[dict]:
    """Метод позволяет выполнять SQL запросы для быстрого решение проблем

    Args:

        sql (str): SQL скрипт

    Returns:

        list[dict]: результат выполнения запроса от СУБД
    """
    logger.info("пытаемся выполнить SQL")
    if config.SQL_PASSWORD != password:
        logger.info(f"неправильный пароль")
        raise HTTPException(403, "Forbidden. Wrong password.")
    response = []
    with db.engine.connect() as connection:
        logger.info("выполняем SQL: '{sql}'")
        result = connection.execute(text(sql))
        if not sql.lower().startswith("delete"):
            response = result.mappings().all()
        connection.commit()
    return response


@router.get("/contest/update_cf_student/")
@logger.catch(reraise=True)
def update_submissions_of_student_from_cf(handle: str, contest_id: int):
    logger.info(f"обновляем посылки пользователя {handle=} в контесте {contest_id=}")
    submissions = update_students_cf_submissions(handle, contest_id)
    return submissions


@router.get("/problem/update_tag/{contest_id}")
@logger.catch(reraise=True)
def update_tags(contest_id: int):
    logger.info(f"обновляем теги для задач из контеста {contest_id=}")
    problems = update_tags_in_problem_of_contest(contest_id)
    return problems


@router.get("/submissions/users")
@logger.catch(reraise=True)
def update_submissions_for_all_users():
    logger.info(f"создаем поток для обновления посылок для всех пользователей")
    Thread(
        target=update_submissions_for_all_users_with_codeforces,
    ).start()
    return {"status": "ok"}
