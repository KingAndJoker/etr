"""API recommendation"""
from loguru import logger
from fastapi import APIRouter

from etr.crud.recommendation import get_recommendations
from etr.schemas.recommendation import RecommendationResponseSchema


router = APIRouter(prefix="/recommendation", tags=["recommendation"])


@router.get("/{handle}")
@logger.catch(reraise=True)
def get_all_recommendations(handle: str):
    """функция возвращает список пользователей и рекомендованные задачи для них

    Args:
        handle (str): handle интересующего пользователя

    Returns:
        _type_: список рекомендованных задач для пользователя
    """
    logger.info(f"API строим список для {handle=}")
    recommendations = [
        recommendation
        for recommendation in get_recommendations()
        if recommendation.user.handle.lower() == handle.lower()
    ]
    if recommendations == []:
        logger.warning(f"API для пользователя {handle=} нету рекомендаций")
        return []

    response_recommendations = {
        "user": recommendations[0].user,
        "recommendations": [
            RecommendationResponseSchema.model_validate(recommendation)
            for recommendation in recommendations
        ]
    }
    logger.success(f"API возвращаю список рекомендаций для {handle=}")
    return response_recommendations
