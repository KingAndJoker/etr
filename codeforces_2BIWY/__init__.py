"""run file"""
from flask import Flask
from sqlalchemy import create_engine
from .models.base import Base


app = Flask(__name__)

DATABASE_URL = "sqlite:///users.db"
echo = True
engine = create_engine(DATABASE_URL, echo=echo)
Base.metadata.create_all(engine)

import codeforces_2BIWY.views
