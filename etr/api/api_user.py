"""API problem"""
from flask import Blueprint, request

from etr.services.user import get_users
from etr.utils.api.api_user import generate_kwargs_for_get_users


bp = Blueprint("api_user", __name__)


@bp.get("/user/")
def get_all_users():
    handles = request.args.get("handles", None)
    country = request.args.get("country", None)
    city = request.args.get("city", None)
    organization = request.args.get("organization", None)
    rank = request.args.get("rank", None)
    max_rank = request.args.get("max_rank", None)
    watch = request.args.get("watch", True)
    lang = request.args.get("lang", "en")

    kwargs = generate_kwargs_for_get_users(
        handles=handles,
        country=country,
        city=city,
        organization=organization,
        rank=rank,
        max_rank=max_rank,
        watch=watch,
        lang=lang
    )

    users_schema = get_users(**kwargs)

    if users_schema is None:
        return {"status": "error"}
    
    users = [
        user_schema.model_dump()
        for user_schema in users_schema
    ]

    return users
