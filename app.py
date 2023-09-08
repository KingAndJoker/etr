"""app file"""
from flask import Flask
from flask import render_template, redirect, request
from flask.views import MethodView
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from models.base import Base
from models.User import User
from schemas.user import UserSchema


class Config:
    """App config file"""
    app: Flask
    engine: Engine

    def __init__(self, app: Flask, engine: Engine = None) -> None:
        self.app = app
        self.engine = engine


def setup_database(config: Config, **kwargs):
    """setup database"""
    DATABASE_URL = "sqlite:///users.db"
    echo = True
    config.engine = create_engine(DATABASE_URL, echo=echo)
    Base.metadata.create_all(config.engine)


def setup(config: Config, **kwargs) -> None:
    """setup app"""
    setup_database(config=config, **kwargs)


app = Flask(__name__)
config = Config(app)

setup(config)


@app.get("/")
def index():
    return render_template("index.html")


class NewUser(MethodView):
    def get(self):
        return render_template("new.html")

    def post(self):
        handler = request.form.get("handler")
        session = Session(config.engine)
        session.add(User(handler=handler))
        session.commit()
        return redirect("/")


class UserView(MethodView):
    def get(self):
        session = Session(config.engine)
        users = session.query(User).all()
        users = [UserSchema.model_validate(user) for user in users]
        return render_template("users.html", users=users)


app.add_url_rule("/user/new", view_func=NewUser.as_view("new-user"))
app.add_url_rule("/user", view_func=UserView.as_view("user"))
