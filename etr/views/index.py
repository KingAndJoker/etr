"""index views"""
from loguru import logger
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="etr/templates")
router = APIRouter()


@router.get("/")
@logger.catch(reraise=True)
def index(request: Request):
    """index page"""
    return templates.TemplateResponse("index.html", context={"request": request})


@router.get("/about")
@logger.catch(reraise=True)
def about(request: Request):
    """about page"""
    return templates.TemplateResponse("about.html", context={"request": request})


@router.get("/api")
@logger.catch(reraise=True)
def api(request: Request):
    """api page"""
    return templates.TemplateResponse("api.html", context={"request": request})
