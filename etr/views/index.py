"""index views"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="etr/templates")
router = APIRouter()


@router.get("/")
def index(request: Request):
    """index page"""
    return templates.TemplateResponse("index.html", context={"request": request})


@router.get("/about")
def about(request: Request):
    """about page"""
    return templates.TemplateResponse("about.html", context={"request": request})


@router.get("/api")
def api(request: Request):
    """api page"""
    return templates.TemplateResponse("api.html", context={"request": request})
