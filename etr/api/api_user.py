"""API problem"""
from flask import Blueprint, request

from etr.services.user import get_users
from etr.utils.api.api_user import generate_kwargs_for_get_users
from etr.services.user import add_user
from etr.services.user import update_user
from etr.services.user import update_user_info_from_codeforces as services_update_user_info_from_codeforces


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

    return {
        "status": "ok",
        "users": users
    }


@bp.post("/user/")
def new_user():
    lang = request.accept_languages.best_match(["ru", "en"], "en")
    input_data = request.get_json()
    handle = input_data.get("handle", None)

    if input_data is None:
        return {"status": "error"}
    
    if handle is None:
        return {"status": "error"}

    user_schema = add_user(handle, lang)

    if user_schema is None:
        return {"status": "error"}
    
    return {
        "status": "ok",
        "user": user_schema.model_dump()
    }


@bp.patch("/user/<int:user_id>")
def patch_user(user_id: int):
    data = request.get_json()

    user_schema = update_user(id=user_id, **data)

    if user_schema is None:
        return {"status": "error"}

    return {
        "status": "ok",
        "result": user_schema.model_dump()
    }


@bp.get("/user/update_codeforces/<handle>")
def update_user_from_codeforces(handle: str):
    user = services_update_user_info_from_codeforces(handle)
    if user is None:
        return {"status": "error"}

    return {
        "status": "ok",
        "user": user.model_dump()
    }
