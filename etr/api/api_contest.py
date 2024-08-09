from typing import Any

from loguru import logger
from fastapi import APIRouter
from fastapi import HTTPException

from etr.services.contest import get_contests
from etr.services.contest import get_contest_table_rows
from etr.services.contest import update_contest
from etr.services.contest import delete_contest_and_deps
from etr.schemas.contest import ContestSchema


router = APIRouter(prefix="/contest", tags=["contests"])


@router.get("/")
@logger.catch(reraise=True)
def api_get_contests(index: int | None = None, count: int | None = None):
    """get contests"""
    logger.info(f"API хочу получить контесты с {index=} {count=} штук")
    params = {
        key: value
        for key, value in dict(
            contest_index=index,
            contest_count=count,
        ).items()
        if value is not None
    }
    
    logger.debug(f"получаю контесты из базы данных")
    contests = get_contests(**params)
    if index is not None:
        logger.debug(f"API обрезаю по {index=}")
        contests = contests[index:]
    if count is not None:
        logger.debug(f"API обрезаю по {count=}")
        contests = contests[:count]
    
    logger.success(f"API возвращаю {len(contests)=} соревнований")
    return {"status": "ok", "contests": contests}


@router.get("/{contest_id}/table")
@logger.catch(reraise=True)
def api_get_table_contest(contest_id: int):
    """функция возвращает таблицу результатов для соревнования

    Args:
        contest_id (int): id контеста

    Returns:
        _type_: возвращает данные о соревновании, и о посылках пользователей/команд
    """
    logger.info(f"API хочу получить данные о результатах {contest_id}")
    contest = get_contests(id=contest_id)[0]
    rows = get_contest_table_rows(contest_id)

    logger.debug(f"API готовлю данные по результатам соревнования {contest_id=}")
    response = {"status": "ok", "contest": contest, "rows": []}

    for row in rows:
        if "user" in row:
            response["rows"].append(
                {"user": row["user"], "submissions": row["submissions"]}
            )
        else:
            response["rows"].append(
                {"team": row["team"], "submissions": row["submissions"]}
            )

    logger.success(f"API возвращаю таблицу результатов для {contest_id=}")
    return response


@router.patch("/contest/{contest_id}")
@logger.catch(reraise=True)
def api_update_contest(contest_id: int, contest_update_fields: dict[str, Any]):
    """функция обновляет данные о контесте

    Args:
        contest_id (int): id соревнования
        contest_update_fields (dict[str, Any]): новые значение полей о соревновании

    Returns:
        _type_: новая информация
    """
    logger.info(f"API пытаемся обновить данные о {contest_id=}")
    contest = update_contest(contest_id, **contest_update_fields)
    if contest is None:
        logger.error(f"API {contest_id=} при попытке обновления вернуло None")
        return {"status": "error"}

    logger.success(f"для соревнования {contest_id} обновление данных прошло успешно")
    return {"status": "ok", "contest": contest}


@router.delete("/contest/{contest_id}")
@logger.catch(reraise=True)
def api_delete_contest(contest_id: int) -> ContestSchema:
    """удаляет контест с заданным contest_id

    Args:

        contest_id (int): id контеста

    Raises:

        HTTPException: вызывается с статус кодом 404 если контест не найден.

    Returns:
        ContestSchema: схема контеста
    """
    logger.info(f"API удаляем контест {contest_id=}")
    contest = delete_contest_and_deps(contest_id)
    if contest is None:
        logger.exception(f"не получилось удалить соревнование {contest_id=}")
        raise HTTPException(status_code=404, detail="Contest not found")
    
    logger.success(f"удалили соревнование {contest_id}")
    return contest
