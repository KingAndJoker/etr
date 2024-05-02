from etr import db
from etr.schemas.recommendation import RecommendationSchema
from etr.models.recommendation import RecommendationOrm


def get_recommendations():
    with db.SessionLocal() as session:
        recommendations_orm = session.query(RecommendationOrm).all()
        recommendations = [
            RecommendationSchema.model_validate(recommendation_orm)
            for recommendation_orm in recommendations_orm
        ]
        return recommendations
