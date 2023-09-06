"""app file"""
from flask import Flask
from flask import render_template, redirect
from sqlalchemy import Engine, create_engine


class Config:
    """App config file"""
    app: Flask
    engine: Engine

    def __init__(self, app: Flask, engine: Engine = None) -> None:
        self.app = app
        self.engine = engine


def setup_database(config: Config, **kwargs):
    """setup database"""
    DATABASE_URL = "sqlite:///:memory:"
    echo = True
    config.engine = create_engine(DATABASE_URL, echo=echo)


def setup(config: Config, **kwargs) -> None:
    """setup app"""
    setup_database(config=config, **kwargs)


app = Flask(__name__)
config = Config(app)

setup(config)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/new")
def new():
    return render_template("new.html")


@app.post("/new")
def new():
    return redirect("/")
