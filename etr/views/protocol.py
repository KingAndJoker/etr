"""views file"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="etr/templates")
router = APIRouter(prefix="/protocol")


@router.get("/")
def get_protocol(request: Request):
    return templates.TemplateResponse("protocol.html", context={"request": request})
