from etr.library.codeforces.schemas.contest import CodeforcesContestSchema
from etr.library.codeforces.schemas.submission import CodeforcesSubmissionSchema
from etr.library.codeforces.schemas.user import CodeforcesUserSchema
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema
from etr.library.codeforces.codeforces_utils import get_contest, get_submission, get_user, get_users, get_problem_with_contest


def test_get_contest():
    contest: CodeforcesContestSchema | None = get_contest(566)

    assert contest is not None, "Contest is None. check get_contest def or network connection."
    assert contest.contestName == "VK Cup 2015 - Finals, online mirror", "Incorrect name of the contest."


def test_get_not_exist_contest():
    contest: CodeforcesContestSchema | None = get_contest(-1)

    assert contest is None, "get_contest returns non-existing contest."


def test_get_user_submission():
    submissions: list[CodeforcesSubmissionSchema] | None = get_submission(566)

    assert submissions is not None, "Submissions is None. Check get_submission def or network connection."
    assert submissions[-1].id == 12277300, "Submission id is incorrect. Check first submission of contest."
    assert isinstance(
        submissions[-1].author,
        CodeforcesUserSchema
    ), "Author class is incorrect. Check author's parser in get_submission."
    assert submissions[-2].id == 12277309, "Submission id is incorrect. Check second submission of contest."
    assert submissions[-2].problem.name == "Clique in the Divisibility Graph", "Name of contest problem is incorrect. Check problem's parser in get_submission."


def test_get_team_submission():
    submissions: list[CodeforcesSubmissionSchema] | None = get_submission(
        566,
        handle="I_love_Hoang_Yen"
    )

    assert submissions is not None, "Submission is None. Check get_submission def or network connection."
    assert submissions[4].id == 12874103, "Submission id is incorrect. Check all submission of \"I_love_Hoang_Yen\" on contest."
    assert isinstance(
        submissions[15].author,
        CodeforcesTeamSchema
    ), "Author class is incorrect. Check author's parser in get_submission."
    assert submissions[15].author.teamName == "Zenith", "team_name is incorrect. Check team parser in get_submission."


def test_get_not_exist_submission():
    submissions: list[CodeforcesSubmissionSchema] | None = get_submission(
        -1,
        from_=1,
        count=3
    )

    assert submissions is None, "get_submission retunrs is non-exists submission."


def test_get_user():
    user: CodeforcesUserSchema | None = get_user("DmitriyH")

    assert user is not None
    assert user.registrationTimeSeconds == 1268570311


def test_get_users():
    handles = [
        "DmitriyH",
        "tourist"
    ]
    users: list[CodeforcesUserSchema | None] = get_users(handles=handles)

    assert len(users) == 2, "get_users return the wrong number of users."
    assert users[0] is not None, "get_users return null for an existing user."
    assert users[1] is not None, "get_users return null for an existing user."
    assert users[1].lastName == "Korotkevich", "last_name is incorrect."


def test_get_not_exist_user():
    user: CodeforcesUserSchema | None = get_user(
        "jasdjaksdjaksdjkasjkdsajkadsjkasjksajkasjdaskjdksaj"
    )

    assert user is None, "get_user return is non-exist user."


def test_get_problems():
    problems = get_problem_with_contest(993)

    assert problems is not None, "get_problem_with_contest return null for an existsing problems."
    assert problems[1].index == "B", "Wrong index in problem."
    assert problems[4].points == 2250, "Wrong points in problem."
    assert problems[3].tags[1] == "dp", "Wrong tag in problem."


def test_get_not_exist_problems():
    problems = get_problem_with_contest(-1)

    assert problems is None, "get_problem_with_contest returns non-existing problems."
