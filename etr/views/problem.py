from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="etr/templates")
router = APIRouter(prefix="/problem")


@router.get("/")
def problems(request: Request):
    """return problems.html template"""
    return templates.TemplateResponse("problems.html", context={"request": request})
