""" contest services """
from loguru import logger

from etr.schemas.contest import ContestSchema
from etr.schemas.submission import SubmissionSchema
from etr.library.codeforces import contest as codeforces_contest
from etr.library.codeforces.codeforces_utils import (
    get_contest as _get_contest_with_codeforces,
)
from etr.crud.problem import add_problems_with_cf
from etr.crud.user import get_users
from etr.crud.user import get_user
from etr.crud.team import get_teams_with_handle_member
from etr.crud.submission import get_submissions
from etr.crud.submission import update_submission
from etr.crud.submission import add_submission_with_schema
from etr.crud.contest import get_contests
from etr.crud.contest import add_contest_with_schema
from etr.crud.contest import update_contest
from etr.crud.contest import delete_contest
from etr.crud.submission import delete_submissions
from etr.crud.problem import delete_problems
from etr.crud.problem import get_problems
from etr.utils.codeforces.convert import convert_codeforces_contest_schema
from etr.utils.codeforces.convert import convert_codeforces_submissions_schema


@logger.catch(reraise=True)
def get_contest_with_codeforces(contest_id: int) -> ContestSchema | None:
    """функция возвращает соревнование из codeforces

    Args:
        contest_id (int): id соревнования

    Returns:
        ContestSchema | None: pydantic схема соревнования
    """
    logger.info(f"хочу получить данные о {contest_id=} из codeforces")
    contest_schema = convert_codeforces_contest_schema(
        _get_contest_with_codeforces(contest_id)
    )
    return contest_schema


@logger.catch(reraise=True)
def add_contest(contest_id: int) -> ContestSchema:
    """функция доабвляет соревнвоание в базу данных

    Args:
        contest_id (int): id соревнования

    Returns:
        ContestSchema: добавленное соревнование
    """
    logger.info(f"хочу добавить {contest_id=}")
    contests_schema = get_contests(id=contest_id)

    if len(contests_schema) > 0:
        logger.warning(f"соревнование {contest_id=} уже есть в базе данных")
        return contests_schema[0]

    contest_schema = get_contest_with_codeforces(contest_id)

    contest_schema = add_contest_with_schema(contest_schema)
    # TODO: rewrite problems get to event
    problems_schema = add_problems_with_cf(contest_id)
    contest_schema.problems = problems_schema

    return contest_schema


@logger.catch(reraise=True)
def update_contest_with_codeforces(contest_id: int) -> ContestSchema | None:
    """функция обновляет данные о соревнвоании из Codeforces

    Args:
        contest_id (int): id соревнования

    Returns:
        ContestSchema | None: новая информация о соревновании
    """
    logger.info(f"хочу обновить информацию о {contest_id=}")
    contest_cf_schema = get_contest_with_codeforces(contest_id)

    if contest_cf_schema is None:
        logger.error(f"не смог получить {contest_id=} для обновления")
        return None

    contests_schema = get_contests(id=contest_id)
    if contests_schema == []:
        return None
    contest_schema = contests_schema[0]

    contest_schema = update_contest(
        contest_schema.id, **contest_cf_schema.model_dump())

    return contest_schema


@logger.catch(reraise=True)
def get_contest_table_rows(contest_id: int) -> list:
    """функция генерирует таблицу результатов для соревнования

    Args:
        contest_id (int): id соревнования

    Returns:
        list: возвращает список сток таблицы
    """
    logger.info(f"составляю таблицу результатов для {contest_id=}")
    # TODO: write tests
    rows = list()

    users = get_users()

    # TODO: rewrite, if user is contestant, but he has no submissions
    for user in users:
        submissions = get_submissions(contest_id=contest_id, author_id=user.id)
        if len(submissions):
            rows.append({"user": user, "submissions": submissions})

        teams = get_teams_with_handle_member(handle=user.handle)
        for team in teams:
            if team in (row.get("team", None) for row in rows):
                continue
            submissions = get_submissions(
                contest_id=contest_id, team_id=team.id)
            if len(submissions) == 0:
                continue
            rows.append({"team": team, "submissions": submissions})

    return rows


@logger.catch(reraise=True)
def delete_contest_and_deps(contest_id: int) -> ContestSchema:
    """функция удаляет соревнование и всё связанное

    Args:
        contest_id (int): id соревнования

    Returns:
        ContestSchema: схема удаленного контеста
    """
    logger.info(f"удаляю {contest_id=} соревнование")
    contest = delete_contest(contest_id)
    delete_submissions(contest_id=contest_id)
    delete_problems(contest_id=contest_id)
    logger.success(f"удалил {contest_id=} и всё связанное")
    return contest


@logger.catch(reraise=True)
def update_students_cf_submissions(handle: str, contest_id: int) -> list[SubmissionSchema]:
    """функция обновляет посылки для конкретного пользователя для конкретного соревнования

    Args:
        handle (str): handle пользователя
        contest_id (int): id соревнования

    Returns:
        list[SubmissionSchema]: список его решений
    """
    logger.info(f"хочу получить данные о решениях для {contest_id=} {handle=}")
    submissions = convert_codeforces_submissions_schema(
        codeforces_contest.status(contestId=contest_id, handle=handle)
    )
    logger.debug(f"получил {len(submissions)=}")

    submissions_db = get_submissions(contest_id=contest_id)
    submissions_db_id = [
        submission.id
        for submission in submissions_db
    ]

    submissions_added = []

    for submission in submissions:
        if submission.id in submissions_db_id:
            update_submission(submission.id, **submission.model_dump())
        else:
            submission.author = get_user(handle=submission.author.handle)
            try:
                submission.problem = get_problems(
                    contest_id=submission.contest_id,
                    index=submission.problem.index
                )[0]
            except IndexError:
                logger.warning((f"IndexError. Try get problem with "
                                f"{contest_id=} and "
                                f"{submission.problem.index=}"
                                f" from DB."))
            else:
                submissions_added.append(
                    add_submission_with_schema(submission)
                )

    submissions_added = [x for x in submissions_added if x]
    
    logger.success(f"для {contest_id=} {handle=} добавил {len(submissions_added)=} решений")

    return submissions_added
