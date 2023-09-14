"""Remote Procedure Call module"""
from flask import (
    Blueprint,
    request
)


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
bp = Blueprint("rpc", __name__, url_prefix="/rpc")
