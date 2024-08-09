from loguru import logger

from etr import db
from etr.schemas.recommendation import RecommendationSchema
from etr.models.recommendation import RecommendationOrm


@logger.catch(reraise=True)
def get_recommendations():
    logger.info(f"получаю все рекомендации")
    with db.SessionLocal() as session:
        recommendations_orm = session.query(RecommendationOrm).all()
        recommendations = [
            RecommendationSchema.model_validate(recommendation_orm)
            for recommendation_orm in recommendations_orm
        ]
        logger.success(f"возвращаю {len(recommendations)=} посылок")
        return recommendations
