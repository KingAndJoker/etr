from etr.schemas.contest import ContestSchema
from etr.schemas.submission import SubmissionSchema
from etr.schemas.user import UserSchema
from etr.schemas.team import TeamSchema
from etr.utils.codeforces_utils import get_contest, get_submission, get_user, get_users


def test_get_contest():
    contest: ContestSchema | None = get_contest(566)

    assert contest is not None
    assert contest.name == "VK Cup 2015 - Finals, online mirror"
    assert contest.problems[4].name == "Restoring Map"


def test_get_not_exist_contest():
    contest: ContestSchema | None = get_contest(-1)

    assert contest is None


def test_get_user_submission():
    submissions: list[SubmissionSchema] | None = get_submission(
        566, from_=1, count=3)

    assert submissions is not None
    assert submissions[1].id == 227708730
    assert isinstance(submissions[0].author, UserSchema)
    assert submissions[2].id == 227705729
    assert submissions[0].problem.name == "Restructuring Company"


def test_get_team_submission():
    submissions: list[SubmissionSchema] | None = get_submission(
        566,
        handle="I_love_Hoang_Yen"
    )

    assert submissions is not None
    assert submissions[4].id == 12874103
    assert isinstance(submissions[15].author, TeamSchema)
    assert submissions[15].author.team_name == "Zenith"


def test_get_not_exist_submission():
    submissions: list[SubmissionSchema] | None = get_submission(
        -1,
        from_=1,
        count=3
    )

    assert submissions is None


def test_get_user():
    user: UserSchema | None = get_user("DmitriyH")

    assert user is not None
    assert user.registration_time_seconds == 1268570311


def test_get_users():
    handles = [
        "DmitriyH",
        "tourist"
    ]
    users: list[UserSchema | None] = get_users(handles=handles)

    assert len(users) == 2
    assert users[0] is not None
    assert users[1] is not None
    assert users[1].last_name == "Korotkevich"


def test_get_not_exist_user():
    user: UserSchema | None = get_user("jasdjaksdjaksdjkasjkdsajkadsjkasjksajkasjdaskjdksaj")

    assert user is None
