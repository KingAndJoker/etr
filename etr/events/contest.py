from dataclasses import dataclass

from . import Event
from etr.schemas.contest import ContestUrl


@dataclass
class UpdateContest(Event):
    pass


@dataclass
class ParseContestBeforeUpdate(Event):
    contest_url: ContestUrl


@dataclass
class ParseCodeforcesContest(Event):
    contest_url: ContestUrl
