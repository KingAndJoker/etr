"""views file"""
from typing import Annotated

import requests
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from etr.models.user import User
from etr.db import get_db


templates = Jinja2Templates(directory="etr/templates")
router = APIRouter(prefix="/user")


@router.get("/new")
def new_user(request: Request):
    return templates.TemplateResponse("new_user.html", context={"request": request})


@router.post("/new")
def new_user(handle: Annotated[str, Form()]):
    if handle is None:
        return RedirectResponse("/etr")
    response = requests.get(f"https://codeforces.com/api/user.info?handles={handle}")
    response_json = response.json()
    if response_json["status"] == "OK":
        with get_db() as session:
            session.add(User(handle=handle))
            session.commit()
    return RedirectResponse("/etr")


@router.get("/")
def get_users(request: Request):
    return templates.TemplateResponse("users.html", context={"request": request})
