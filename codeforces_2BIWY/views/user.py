"""views file"""
import requests
from sqlalchemy.orm import Session
from flask import render_template, redirect, request, Blueprint

from codeforces_2BIWY.models.user import User
from codeforces_2BIWY.schemas.user import UserSchema
from codeforces_2BIWY.db import get_db


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/new", methods=["GET", "POST"])
def new_user():
    if request.method == "GET":
        return render_template("new.html")
    elif request.method == "POST":
        handler = request.form.get("handler")
        response = requests.get(
            f"https://codeforces.com/api/user.info?handles={handler}"
        )
        response_json = response.json()
        if response_json['status'] == "OK":
            with get_db() as session:
                session.add(User(handler=handler))
                session.commit()
        return redirect("/")


@bp.route("/")
def get_users():
    with get_db() as session:
        users = session.query(User).all()
        users = [UserSchema.model_validate(user) for user in users]
        for i, user in enumerate(users):
            response = requests.get(
                f"https://codeforces.com/api/user.info?handles={user.handler}"
            )
            response_json = response.json()
            if response_json["status"] == "OK":
                users[i] = user.model_copy(update=response_json["result"][0])
    return render_template("users.html", users=users)
