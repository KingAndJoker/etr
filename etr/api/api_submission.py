from loguru import logger
from fastapi import APIRouter

from etr.crud.submission import get_submissions
from etr.crud.submission import delete_submissions
from etr.schemas.user import ContestantType
from etr.utils.api.generate import generate_kwargs


router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.get("/")
@logger.catch(reraise=True)
def api_get_submissions(
    handle: str | None = None,
    contest_id: int | None = None,
    problem_index: str | None = None,
    min_creation_time_seconds: int | None = None,
    max_creation_time_seconds: int | None = None
):
    """функция возвращает посылки пользователей

    Args:
        handle (str | None, optional): handle автора посылки. Defaults to None.
        contest_id (int | None, optional): id контеста. Defaults to None.
        problem_index (str | None, optional): индекс (номер) задачи. Defaults to None.
        min_creation_time_seconds (int | None, optional): минимальное время создания в UNIX. Defaults to None.
        max_creation_time_seconds (int | None, optional): максимлаьное время создания в UNIX. Defaults to None.

    Returns:
        _type_: список посылок, подходящих под заданные параметры
    """
    logger.info("API получаем посылки пользователей из базы данных")
    kwargs = generate_kwargs(
        handle=handle,
        contest_id=contest_id,
        problem_index=problem_index,
        min_creation_time_seconds=min_creation_time_seconds,
        max_creation_time_seconds=max_creation_time_seconds
    )
    submissions = get_submissions(**kwargs)

    logger.success("API посылки получили")
    return {"status": "ok", "submissions": submissions}


@router.delete("/")
@logger.catch(reraise=True)
def api_delete_submissions(
    id_: int | None = None,
    contest_id: int | None = None,
    author_id: int | None = None,
    team_id: int | None = None,
    problem_id: int | None = None,
    programming_language: str | None = None,
    type_of_member: ContestantType | None = None,
):
    """функция удаляет все посылки, подходящий под описание

    Args:
        id_ (int | None, optional): id посылки (если конкретная посылка). Defaults to None.
        contest_id (int | None, optional): id контеста. Defaults to None.
        author_id (int | None, optional): id автора. Defaults to None.
        team_id (int | None, optional): id команды. Defaults to None.
        problem_id (int | None, optional): id задачи. Defaults to None.
        programming_language (str | None, optional): язык программирования. Defaults to None.
        type_of_member (ContestantType | None, optional): тип участия в соревновании. Defaults to None.

    Returns:
        _type_: количество удаленных посылок
    """
    logger.info("API удаляем посылки")
    kwargs = generate_kwargs(
        id_=id_,
        contest_id=contest_id,
        author_id=author_id,
        team_id=team_id,
        problem_id=problem_id,
        programming_language=programming_language,
        type_of_member=type_of_member,
    )

    deleted_count = delete_submissions(**kwargs)

    logger.success(f"удалили {deleted_count=} посылок")
    return {"status": "ok", "count_submissions": deleted_count}
