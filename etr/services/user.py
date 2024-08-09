from loguru import logger
from fastapi import HTTPException

from etr.schemas.user import UserSchema
from etr.schemas.contest import ContestSchema
from etr.schemas.team import TeamSchema
from etr.schemas.problem import ProblemSchema
from etr.schemas.problem import ProblemSchemaFrozen
from etr.crud.submission import get_submissions
from etr.crud.team import get_teams
from etr.crud.contest import get_contests
from etr.crud.user import get_user, get_users, add_user, update_user
from etr.crud.user import delete_user
from etr.library.codeforces.codeforces_utils import get_user as get_codeforces_user
from etr.library.dl_gsu_by_codeforces.parse_students import get_students
from etr.utils.codeforces.convert import convert_codeforces_user_schema
from etr.utils.dl_gsu_by_codeforces.convert import convert_dl_to_etr


@logger.catch(reraise=True)
def sync_user_with_dl():
    """функция добавляет отсутствующих пользователей в базу данных или обновляет данные о существующих
    """
    logger.info(f"добавлять из dl пользователей в базу данных")
    logger.debug(f"получаю учеников из dl/codeforces")
    sync_users_schema = convert_dl_to_etr(get_students())

    users_schema = get_users()
    for dl_user in sync_users_schema:
        if dl_user.handle.lower() in (user_schema.handle.lower() for user_schema in users_schema):
            logger.debug(f"обновляю данные о {dl_user.handle=}")
            update_user_schema = get_user(handle=dl_user.handle)
            params = {
                key: value
                for key, value in dl_user.model_dump(exclude=("id")).items()
                if value is not None
            }
            try:
                update_user(update_user_schema.id, **params)
            except Exception as err:
                print(err)
        else:
            logger.debug(f"добавляю пользователя {dl_user.handle=} в базу данных")
            add_user(dl_user)


@logger.catch(reraise=True)
def add_user_from_codeforces(handle: str, lang: str = "ru") -> UserSchema | None:
    """функция получает данные о пользователе из codeforces и добавляет в базу данных

    Args:
        handle (str): handle пользователя
        lang (str, optional): язык результата. Defaults to "ru".

    Returns:
        UserSchema | None: схема добавленного пользователя из базы данных
    """
    logger.info(f"добавляю {handle=} пользователя из codeforces")
    user_schema = convert_codeforces_user_schema(get_codeforces_user(handle, lang=lang))
    return add_user(user_schema)


@logger.catch(reraise=True)
def update_user_info_from_codeforces(handle: str) -> UserSchema | None:
    """обновляет данных о пользователе из codeforces

    Args:
        handle (str): handle пользователя

    Returns:
        UserSchema | None: новая схема данных пользователя
    """
    logger.info(f"пытаюсь обновить данные о {handle=} из codeforces")
    user_new = convert_codeforces_user_schema(get_codeforces_user(handle, lang="ru"))
    if user_new is None:
        logger.error(f"не смог получить данные о {handle=}")
        return None

    user_etr = get_user(handle=handle)
    if user_etr is None:
        logger.warning(f"пользователя {handle=} нету в базе данных")
        return None

    logger.debug(f"обновляю данные о {handle=} в базе данных")
    params = {
        key: value
        for key, value in user_new.model_dump(exclude=("id")).items()
        if value is not None
    }
    return_user = update_user(user_etr.id, **params)
    return return_user


@logger.catch(reraise=True)
def get_user_teams_by_handle(handle: str) -> list[TeamSchema]:
    """функция возвращает все команды пользователя

    Args:
        handle (str): handle пользователя

    Returns:
        list[TeamSchema]: лист команд, в которых состоит пользователь
    """
    return [
        team for team in get_teams() if handle in [user.handle for user in team.users]
    ]


@logger.catch(reraise=True)
def get_user_contests(handle: str) -> list[ContestSchema]:
    """функция возвращает список всех соревнований в которых участвовал пользователь

    Args:
        handle (str): handle пользователя

    Returns:
        list[ContestSchema]: список соревнований, в которых участвовал пользователь
    """
    logger.info(f"хочу получить все соревнования для {handle=}")
    user = get_user(handle)
    teams = get_user_teams_by_handle(handle)
    submissions = get_submissions(author_id=user.id)

    for team in teams:
        submissions += get_submissions(team_id=team.id)
    
    logger.debug(f"составляю список соревнований из {len(submissions)=} посылок")

    contests_id = list(set([submission.contest_id for submission in submissions]))
    
    logger.debug(f"пользователь {handle=} участвовал в {len(contests_id)=} соревнованиях")

    contests = [contest for contest in get_contests() if contest.id in contests_id]
    return contests


@logger.catch(reraise=True)
def services_delete_user(user_id: int) -> UserSchema:
    """функция удаляет 

    Args:
        user_id (int): id удаляемого пользователя

    Raises:
        HTTPException: вызывается при отсутствии пользователя с заданным id в базе данных с кодом 404
        HTTPException: вызывается если функция не удалила или удалила лишних пользователей с кодом 500

    Returns:
        UserSchema: схема удаленного пользователя
    """
    logger.info(f"удаляю пользователя {user_id=} из базы данных")
    users = get_users(id=user_id)
    if users == []:
        # TODO: тут не место HTTPException
        logger.error(f"пользователя с {user_id} нету в базе данных")
        raise HTTPException(404, "Пользователь не найден.")
    user = users[0]

    cnt = delete_user(user_id)
    if cnt != 1:
        logger.error(f"функция удаления вернула {cnt=}")
        raise HTTPException(500, "Количество удаленных пользователей не равно 1.")
    logger.success(f"пользователь {user_id=} {user.handle=} удален из базы данных")
    return user


@logger.catch(reraise=True)
def services_get_solved_problems(id: int, **kwargs) -> list[ProblemSchema]:
    """функция возвращает все задачи на которые пользователь отправлял решения

    Args:
        id (int): id пользователя

    Returns:
        list[ProblemSchema]: список задач для которых есть хотя бы одно отправленное решение
    """
    logger.info(f"пытаюсь получать информацию о задачах пользователя {id=}")
    users = get_users(id=id)
    if users == []:
        logger.error(f"пользователя с {id=} нету в базе данных")
        return []
    user = users[0]
    submissions = get_submissions(author_id=user.id, **kwargs)
    teams = get_user_teams_by_handle(user.handle)
    for team in teams:
        submissions += get_submissions(team_id=team.id, **kwargs)

    logger.debug(f"составляю список задач из {len(submissions)=} посылок")

    problems = list(
        set(
            [
                ProblemSchemaFrozen(**submission.problem.model_dump())
                for submission in submissions
            ]
        )
    )
    logger.success(f"возвращаю {len(submissions)=} задач")
    return problems
