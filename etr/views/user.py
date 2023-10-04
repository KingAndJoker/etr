"""views file"""
import requests
from sqlalchemy.orm import Session
from flask import render_template, redirect, request, Blueprint

from etr.models.user import User
from etr.schemas.user import UserSchema
from etr.db import get_db


bp = Blueprint("user", __name__)


@bp.route("/new", methods=["GET", "POST"])
def new_user():
    if request.method == "GET":
        return render_template("new_user.html")

    elif request.method == "POST":
        handle = request.form.get("handle")
        response = requests.get(
            f"https://codeforces.com/api/user.info?handles={handle}"
        )
        response_json = response.json()
        if response_json['status'] == "OK":
            with get_db() as session:
                session.add(User(handle=handle))
                session.commit()
        return redirect("/etr")


@bp.route("/")
def get_users():
    with get_db() as session:
        users = session.query(User).all()
        users = [UserSchema.model_validate(user) for user in users]
        for i, user in enumerate(users):
            response = requests.get(
                f"https://codeforces.com/api/user.info?handles={user.handle}"
            )
            response_json = response.json()
            if response_json["status"] == "OK":
                users[i] = user.model_copy(update=response_json["result"][0])
    return render_template("users.html", users=users)
