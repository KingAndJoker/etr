"""API recommendation"""
from fastapi import APIRouter

from etr.crud.recommendation import get_recommendations
from etr.schemas.recommendation import RecommendationResponseSchema


router = APIRouter(prefix="/recommendation", tags=["recommendation"])


@router.get("/{handle}")
def get_all_recommendations(handle: str):
    recommendations = [
        recommendation
        for recommendation in get_recommendations()
        if recommendation.user.handle.lower() == handle.lower()
    ]
    if recommendations == []:
        return []

    response_recommendations = {
        "user": recommendations[0].user,
        "recommendations": [
            RecommendationResponseSchema.model_validate(recommendation)
            for recommendation in recommendations
        ]
    }
    return response_recommendations
