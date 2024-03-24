"""API problem"""
from enum import Enum
from fastapi import APIRouter

from etr.services.problem import get_problems_with_contest_id, get_problems


router = APIRouter(prefix="/problem", tags=["problems"])


class NONES(Enum):
    NONE = None
    NULL = None


@router.get("/")
def api_get_problems(
    id_: int | None = None,
    contest_id: int | None = None,
    problemset_name: str | None = None,
    index: str | None = None,
    rating: str | None = None,
    points: str | None = None,
):
    """метод для получения списка задач

    Args:
    
        id_ (int | None, optional): Id задачи. Defaults to None.
        
        contest_id (int | None, optional): получить задачи с определенным contest_id. Defaults to None.
        
        problemset_name (str | None, optional): получить задачи из определенного архива. Defaults to None.
        
        index (str | None, optional): индекс задачи. Defaults to None.
        
        rating (str | None, optional): рейтинг задачи. Принимает целое число или строку 'none', 'null'. Defaults to None.
        
        points (str | None, optional): баллы за задачу. Принимает число с плавающей запятой или строку 'none', 'null'. Defaults to None.

    Returns:
        _type_: список задач с заданными параметрами
    """
    params = {
        "id": id_,
        "contest_id": contest_id,
        "problemset_name": problemset_name,
        "index": index,
    }
    params = {key: value for key, value in params.items() if value is not None}
    try:
        if rating.lower() == "null" or rating.lower() == "none":
            params["rating"] = None
        else:
            params["rating"] = int(rating)
    except:
        pass
    try:
        if points.lower() == "null" or points.lower() == "none":
            params["points"] = None
        else:
            params["points"] = float(rating)
    except:
        pass

    problems = get_problems(**params)

    return {
        "status": "ok",
        "problems": [problem.model_dump() for problem in problems]
    }


@router.get("/{contest_id}")
def get_problem_with_contest(contest_id: int):
    """Get problem with contest"""

    problems_schema = get_problems_with_contest_id(contest_id)
    return {"status": "ok", "problems": problems_schema}
