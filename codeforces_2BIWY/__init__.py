"""run file"""
import os

from flask import Flask
from sqlalchemy import create_engine
from .models.base import Base


def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",

    )
    # app.config.from_file("pyproject.toml")

    # register the database commands
    from codeforces_2BIWY import db

    # Base.metadata.create_all(app.config["DATABASE_ENGINE"])
    db.init_db(app)

    # apply the blueprints to the app
    from codeforces_2BIWY import views

    # app.register_blueprint(views.bp)
    app.add_url_rule("/user/new", view_func=views.NewUser.as_view("new-user"))
    app.add_url_rule("/user", view_func=views.UserView.as_view("user"))
    # app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index

    return app
