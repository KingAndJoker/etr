"""API problem"""
from flask import Blueprint

from etr.services.user import get_users


bp = Blueprint("api_user", __name__)


@bp.get("/user/")
def get_all_users():
    users_schema = get_users()

    if users_schema is None:
        return {"status": "error"}
    
    users = [
        user_schema.model_dump()
        for user_schema in users_schema
    ]

    return users
