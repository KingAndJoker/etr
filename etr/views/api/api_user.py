"""API problem"""
from flask import Blueprint

from etr.services.user import get_users


bp = Blueprint("api_user", __name__)


@bp.get("/user/")
def get_all_users():
    users = get_users()

    return users
