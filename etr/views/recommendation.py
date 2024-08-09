"""recommendation file"""
from loguru import logger
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="etr/templates")
router = APIRouter(prefix="/recommendation")


@router.get("/")
@logger.catch(reraise=True)
def get_users(request: Request):
    return templates.TemplateResponse("recommendation.html", context={"request": request})
