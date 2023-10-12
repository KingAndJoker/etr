from etr.schemas.contest import ContestSchema
from etr.utils.codeforces_utils import get_contest


def test_get_contest():
    contest: ContestSchema | None = get_contest(566)

    assert contest is not None
    assert contest.name == "VK Cup 2015 - Finals, online mirror"
    assert contest.problems[4].name == "Restoring Map"


def test_get_not_exist_contest():
    contest: ContestSchema | None = get_contest(-1)

    assert contest is None
