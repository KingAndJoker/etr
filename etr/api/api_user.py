"""API problem"""
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

    users_schema = get_users(**kwargs)

    if users_schema is None:
        return {"status": "error"}

    users = [user_schema.model_dump() for user_schema in users_schema]

    return {"status": "ok", "users": users}


@router.post("/")
def new_user(user: UserRequestAddCodeforcesSchema, lang: str | None = "ru"):
    handle = user.handle

    if handle is None:
        return {"status": "error", "message": "handle is missing"}

    user_schema = add_user_from_codeforces(user.handle)

    if user_schema is None:
        return {"status": "error", "message": "user not added"}

    return {"status": "ok", "user": user_schema}


@router.patch("/{user_id}")
def patch_user(user_id: int, user: UserPatch):
    data = user.model_dump(exclude_unset=True)

    user_schema = update_user(id=user_id, **data)

    if user_schema is None:
        return {"status": "error"}

    return {"status": "ok", "result": user_schema}


@router.get("/update_codeforces/{handle}")
def update_user_from_codeforces(handle: str):
    user = services_update_user_info_from_codeforces(handle)
    if user is None:
        return {"status": "error"}

    return {"status": "ok", "user": user}


@router.get("/{handle}/contests")
def api_get_user_contests(handle: str) -> list[ContestSchema]:
    return get_user_contests(handle)


@router.delete("/{user_id}", deprecated=True)
def api_delete_user(user_id: int) -> UserSchema:
    """
    Удаляет пользователя из базы данных.

    Не рекомендуется к использованию т.к. пользователь может быть частью команды и при удалении команда будет не полной.

    Рекомендуется изменить поле watch у пользователя, используя **PATCH** метод.
    """
    user = services_delete_user(user_id)
    return user


@router.get("/{user_id}/problems")
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
    params = {"id": user_id, "verdict": verdict.value}
    params = {
        key: value for key, value in params.items() if value is not None and value
    }
    problems = services_get_solved_problems(**params)
    return problems
