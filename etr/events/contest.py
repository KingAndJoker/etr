from dataclasses import dataclass

from . import Event
from etr.schemas.contest import ContestSchema
from etr.schemas.contest import ContestUrl


@dataclass
class ParseContestBeforeUpdate(Event):
    contest_url: ContestUrl


@dataclass
class ParseCodeforces(Event):
    contest_url: ContestUrl


@dataclass
class ParseCodeforcesContest(Event):
    contest_url: ContestUrl


@dataclass
class ParseCodeforcesGym(Event):
    contest_url: ContestUrl


@dataclass
class AddContest(Event):
    contest: ContestSchema
