"""views file"""
import requests
from sqlalchemy.orm import Session
from flask import render_template, redirect, request
from flask.views import MethodView

from codeforces_2BIWY.models.User import User
from codeforces_2BIWY.schemas.user import UserSchema
from codeforces_2BIWY.db import get_db


def index():
    return render_template("index.html")


class NewUser(MethodView):
    def get(self):
        return render_template("new.html")

    def post(self):
        handler = request.form.get("handler")
        session: Session = get_db()
        session.add(User(handler=handler))
        session.commit()
        return redirect("/")


class UserView(MethodView):
    def get(self):
        session: Session = get_db()
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
