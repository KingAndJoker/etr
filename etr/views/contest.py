"""contest views"""
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from etr import db
from etr.models.contest import ContestOrm
from etr.schemas.contest import ContestSchema
from etr.events.contest import ParseContestBeforeUpdate
from etr.handlers import handler
from etr.utils.services.contest import parse_url


templates = Jinja2Templates(directory="etr/templates")
router = APIRouter(prefix="/contest")


@router.get("/")
def get_contests(request: Request):
    return templates.TemplateResponse("contests.html", context={"request": request})


@router.get("/new")
def new_contest(request: Request):
    return templates.TemplateResponse("new_contest.html", context={"request": request})


@router.post("/new")
def new_contest(contest_url: Annotated[str, Form()], request: Request):
    url = parse_url(contest_url)
    event = ParseContestBeforeUpdate(url)
    results = handler(event)

    return RedirectResponse("/etr/", status_code=303)


@router.get("/{contest_id}")
def get_contest(contest_id: int, request: Request):
    with db.SessionLocal() as session:
        contest_db: ContestOrm = (
            session.query(ContestOrm).filter(ContestOrm.id == contest_id).one_or_none()
        )

        contest = ContestSchema.model_validate(contest_db)

    return templates.TemplateResponse(
        "contest.html", context={"request": request, "contest": contest}
    )
