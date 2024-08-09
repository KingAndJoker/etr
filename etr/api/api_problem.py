"""API problem"""
from enum import Enum

from loguru import logger
from fastapi import APIRouter

from etr.services.problem import get_problems_with_contest_id, get_problems


router = APIRouter(prefix="/problem", tags=["problems"])


class NONES(Enum):
    NONE = None
    NULL = None


@router.get("/")
@logger.catch(reraise=True)
def api_get_problems(
    id_: int | None = None,
    contest_id: int | None = None,
    problemset_name: str | None = None,
    index: str | None = None,
    rating: str | None = None,
    points: str | None = None,
    tags: str | None = None
):
    """метод для получения списка задач

    Args:

        id_ (int | None, optional): Id задачи. Defaults to None.

        contest_id (int | None, optional): получить задачи с определенным contest_id. Defaults to None.

        problemset_name (str | None, optional): получить задачи из определенного архива. Defaults to None.

        index (str | None, optional): индекс задачи. Defaults to None.

        rating (str | None, optional): рейтинг задачи. Принимает целое число или строку 'none', 'null'. Defaults to None.

        points (str | None, optional): баллы за задачу. Принимает число с плавающей запятой или строку 'none', 'null'. Defaults to None.

        tags (str | None, optional): теги, перечисленные через ';'. Вернуться задачи с заданными тегами. Defaults to None.

    Returns:
        _type_: список задач с заданными параметрами
    """
    logger.info(f"API получаем задачи")
    params = {
        "id": id_,
        "contest_id": contest_id,
        "problemset_name": problemset_name,
        "index": index,
        "tags": [tag for tag in tags.split(";") if tag] if tags else None,
    }
    params = {key: value for key, value in params.items() if value is not None}
    try:
        if rating.lower() == "null" or rating.lower() == "none":
            params["rating"] = None
        else:
            params["rating"] = int(rating)
    except:
        logger.exception(f"{rating=} либо отсутсвует, либо не приводим к числу")
    try:
        if points.lower() == "null" or points.lower() == "none":
            params["points"] = None
        else:
            params["points"] = float(points)
    except:
        logger.exception(f"{points=} либо отсутсвует, либо не приводим к числу")

    problems = get_problems(**params)

    logger.success(f"API возвращаю {len(problems)=} задач")
    return {
        "status": "ok",
        "problems": problems
    }


@router.get("/{contest_id}")
@logger.catch(reraise=True)
def get_problem_with_contest(contest_id: int):
    """Get problem with contest"""
    logger.info(f"API получаю список задач для контеста {contest_id=}")
    problems_schema = get_problems_with_contest_id(contest_id)
    logger.success(f"API для контеста {contest_id=} возвращаю {len(problems_schema)=} задач")
    return {"status": "ok", "problems": problems_schema}
