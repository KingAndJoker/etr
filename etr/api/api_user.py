"""API problem"""
from loguru import logger
from fastapi import APIRouter

from etr.services.user import get_users
from etr.services.user import add_user_from_codeforces
from etr.services.user import services_delete_user
from etr.services.user import update_user
from etr.services.user import (
    update_user_info_from_codeforces as services_update_user_info_from_codeforces,
)
from etr.services.user import get_user_contests
from etr.services.user import services_get_solved_problems
from etr.schemas.user import UserRequestAddCodeforcesSchema
from etr.schemas.user import UserPatch
from etr.schemas.user import UserSchema
from etr.schemas.contest import ContestSchema
from etr.schemas.problem import ProblemSchema
from etr.schemas.problem import VerdictType
from etr.utils.api.api_user import generate_kwargs_for_get_users


router = APIRouter(prefix="/user", tags=["users"])


@router.get("/")
@logger.catch(reraise=True)
async def get_all_users(
    handles: str | None = None,
    country: str | None = None,
    city: str | None = None,
    organization: str | None = None,
    rank: str | None = None,
    max_rank: str | None = None,
    watch: bool | None = None,
    lang: str | None = "ru",
):
    """функция возвращает список пользователей, подходящих под параметры

    Args:
        handles (str | None, optional): строка с handle интересующих пользователей, разделитель символ ';'. Defaults to None.
        country (str | None, optional): страна. Defaults to None.
        city (str | None, optional): город. Defaults to None.
        organization (str | None, optional): организация. Defaults to None.
        rank (str | None, optional): ранг пользователей. Defaults to None.
        max_rank (str | None, optional): максимальный ранг пользователя. Defaults to None.
        watch (bool | None, optional): флаг слежки за пользователем. Defaults to None.
        lang (str | None, optional): язык результата. Defaults to "ru".

    Returns:
        _type_: возвращает словарь, под ключем 'users' находятся все подходящие пользователи. В случае ошибки возвращает 'status': 'error'
    """
    logger.info("API кто-то хочет получить информацию про пользователей")
    kwargs = generate_kwargs_for_get_users(
        handles=handles,
        country=country,
        city=city,
        organization=organization,
        rank=rank,
        max_rank=max_rank,
        watch=watch,
        lang=lang,
    )

    logger.debug("получаем пользователей")
    users_schema = get_users(**kwargs)

    if users_schema is None:
        logger.error("user_schema is None")
        # TODO: raise Exception
        return {"status": "error"}

    # users = [user_schema.model_dump() for user_schema in users_schema]

    logger.success(f"всё хорошо, получили данные о {len(users_schema)=} пользователях")
    return {"status": "ok", "users": users_schema}


@router.post("/")
@logger.catch(reraise=True)
def new_user(user: UserRequestAddCodeforcesSchema, lang: str | None = "ru"):
    """функция добавляет нового пользователя в базу данных

    Args:
        user (UserRequestAddCodeforcesSchema): класс с handle пользователя
        lang (str | None, optional): язык результата. Defaults to "ru".

    Returns:
        _type_: UserSchema добавленного пользователя
    """
    handle = user.handle
    logger.info(f"API пытаемся добавить в базу данных данные о пользователе {handle=}")

    if handle is None:
        logger.error("handle оказался is None")
        return {"status": "error", "message": "handle is missing"}

    user_schema = add_user_from_codeforces(user.handle)

    if user_schema is None:
        logger.error(f"не получилось получить информацию о пользователе {handle=}")
        return {"status": "error", "message": "user not added"}

    logger.success(f"всё хорошо, добавили пользователя с {handle=} {user_schema.id=}")
    return {"status": "ok", "user": user_schema}


@router.patch("/{user_id}")
@logger.catch(reraise=True)
def patch_user(user_id: int, user: UserPatch):
    """функция изменяет данные о пользователе

    Args:
        user_id (int): id изменяемого пользователя
        user (UserPatch): поля, которые надо изменить

    Returns:
        _type_: новая UserSchema пользователя
    """
    logger.info(f"хотим поменять данные о пользователе {user_id=}")
    data = user.model_dump(exclude_unset=True)

    user_schema = update_user(id=user_id, **data)

    if user_schema is None:
        logger.error(f"API user_schema почему-то is None {user_id=}")
        return {"status": "error"}

    logger.success(f"API данные о {user_id=} обновлены")
    return {"status": "ok", "result": user_schema}


@router.get("/update_codeforces/{handle}")
@logger.catch(reraise=True)
def update_user_from_codeforces(handle: str):
    """функция обновляет данные о пользователе исходя из данных Codeforces

    Args:
        handle (str): handle обновляемого пользователя

    Returns:
        _type_: возвращает схему обновленного пользователя
    """
    logger.info(f"API обновляем данные о {handle=}")
    user = services_update_user_info_from_codeforces(handle)
    if user is None:
        logger.error("что-то пошло не так")
        return {"status": "error"}

    logger.success(f"API данные о {handle=} успешно обновлены")
    return {"status": "ok", "user": user}


@router.get("/{handle}/contests")
@logger.catch(reraise=True)
def api_get_user_contests(handle: str) -> list[ContestSchema]:
    """функция возвращает контесты пользователя с заданным handle

    Args:
        handle (str): handle пользователя

    Returns:
        list[ContestSchema]: список соревнований, в которых участвовал пользователь
    """
    logger.info(f"API получаем соревнования пользователя {handle=}")
    return get_user_contests(handle)


@router.delete("/{user_id}", deprecated=True)
@logger.catch(reraise=True)
def api_delete_user(user_id: int) -> UserSchema:
    """
    Удаляет пользователя из базы данных.

    Не рекомендуется к использованию т.к. пользователь может быть частью команды и при удалении команда будет не полной.

    Рекомендуется изменить поле watch у пользователя, используя **PATCH** метод.
    """
    logger.info(f"API пытаемся удалить данные о пользователе с {user_id=}")
    user = services_delete_user(user_id)
    logger.success(f"API удалили пользователя {user_id=}")
    return user


@router.get("/{user_id}/problems")
@logger.catch(reraise=True)
def api_get_problems_by_user(
    user_id: str, verdict: VerdictType | None = None
) -> list[ProblemSchema]:
    """Метод возвращает задачи пользователя

    Args:

        user_id (str): id пользователя

        verdict (VerdictType | None, optional): Тип вердикта. По умолчанию не нужен.

    Returns:
        list[ProblemSchema]: Возвращает список проблем с которыми взаимодействовал пользователь.
    """
    logger.info(f"API хотим получить задачи, которые решал пользователь с {user_id=}")
    params = {"id": user_id, "verdict": verdict.value}
    params = {
        key: value for key, value in params.items() if value is not None and value
    }
    problems = services_get_solved_problems(**params)
    logger.success(f"API получили {len(problems)=} задач у пользователя {user_id=}")
    return problems
