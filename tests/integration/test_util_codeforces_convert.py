from etr.library.codeforces.codeforces_utils import (
    get_user,
    get_users,
    get_submission,
    get_problem_with_contest
)
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema
from etr.utils.codeforces.convert import (
    convert_codeforces_user_schema,
    convert_codeforces_submission_schema,
    convert_codeforces_submissions_schema,
    convert_codeforces_problems_schema,
    convert_codeforces_team_schema
)
from etr.schemas.user import UserSchema
from etr.schemas.team import TeamSchema


def test_convert_user():
    codeforces_user = get_user(handle="tourist")
    assert codeforces_user is not None, "Existing user is None. Check get_user or network connection."
    assert codeforces_user.lastName == "Korotkevich", "lastName is incorrect. Check cf profile info and get_users func."

    user = convert_codeforces_user_schema(codeforces_user)

    assert user.last_name == "Korotkevich", "last_name is incorrect. Check cf profile info and convert_codeforces_user_schema func."
    assert user.first_name == "Gennady", "first_name is incorrect. Check cf profile info and convert_codeforces_user_schema func."
    assert user.city == "Gomel", "city is incorrect. Check cf profile info and convert_codeforces_user_schema func."


def test_convert_users():
    handles = [
        "tourist",
        "DmitriyH"
    ]
    codeforces_users = get_users(handles)
    assert codeforces_users is not None, "Existing users is None. Check get_users or network connection."
    assert codeforces_users[0].lastName == "Korotkevich", "lastName is incorrect. Check cf profile info and get_users func."
    assert codeforces_users[1].lastName == "Khodyrev", "lastName is incorrect. Check cf profile info and get_users func."

    users = [
        convert_codeforces_user_schema(codeforces_user)
        for codeforces_user in codeforces_users
    ]

    assert users[0].last_name == "Korotkevich", "last_name is incorrect. Check cf profile info and convert_codeforces_user_schema func."
    assert users[0].first_name == "Gennady", "first_name is incorrect. Check cf profile info and convert_codeforces_user_schema func."
    assert users[0].city == "Gomel", "city is incorrect. Check cf profile info and convert_codeforces_user_schema func."

    assert users[1].last_name == "Khodyrev", "last_name is incorrect. Check cf profile info and convert_codeforces_user_schema func."


def test_convert_submission_user():
    codeforces_submissions = get_submission(566)
    assert codeforces_submissions is not None, "Existing submissions is None. Check get_submission or network connection."
    assert codeforces_submissions[-1].id == 12277300, "id is incorrect. Check get_submission func."

    submission = convert_codeforces_submission_schema(codeforces_submissions[-1])

    assert submission.id == 12277300, "id is incorrect. Check convert_codeforces_submission_schema func."
    assert submission.programming_language == "GNU C++11", "programming language is incorrect. Check convert_codeforces_submission_schema."
    assert isinstance(submission.author, UserSchema), "submission author is not user. Check convert_codeforces_submission_schema."
    assert submission.author.handle == "truckski", "handle of author incorrect. Check convert_cdoeforces_submission_schema."



def test_convert_submission_team():
    codeforces_submissions = get_submission(566)
    assert codeforces_submissions is not None, "Existing submissions is None. Check get_submission or network connection."
    assert codeforces_submissions[-1].id == 12277300, "id is incorrect. Check get_submission func."

    submission = convert_codeforces_submission_schema(codeforces_submissions[-3])

    assert isinstance(submission.author, TeamSchema), "submission author is not team. Check convert_codeforces_submission_schema."
    assert submission.author.team_name == "USA1", "team name is incorrect. Check convert_codeforces_submission_schema."


def test_convert_submissions():
    codeforces_submissions = get_submission(566)
    assert codeforces_submissions is not None, "Existing submissions is None. Check get_submission or network connection."
    assert codeforces_submissions[-1].id == 12277300, "id is incorrect. Check get_submission func."

    submissions = convert_codeforces_submissions_schema(codeforces_submissions)

    assert submissions[-100].programming_language == "GNU C++"


def test_convert_problems():
    codeforces_problems = get_problem_with_contest(566)

    assert codeforces_problems is not None, "Existing problems is None. Check get_problem_with_contest func or network connection."
    assert len(codeforces_problems) == 7, "Number of problems is incorrect. Check contest info and get_problem_with_contest func."
    assert codeforces_problems[3].contestId == 566, "contestId is incorrect. Check get_problem_with_contest."

    problems = convert_codeforces_problems_schema(codeforces_problems)

    assert len(problems) == 7, "Number of problems is incorrect. Check contest info and get_problem_with_contest func."
    assert problems[3].contest_id == 566, "problem.contest_id is incorrect. Check convert_codeforces_problems_schema."
    assert problems[6].index == "G", "problem index is incorrect. Check convert_codeforces_problems_schema."


def test_team():
    codeforces_users = get_users(["DmitriyH", "Fefer_Ivan"])
    codeforces_team = CodeforcesTeamSchema(teamId=123, teamName="BBIWY", users=codeforces_users)

    assert codeforces_users is not None, "Existing users is None. Check get_users or network connection."
    assert codeforces_team.teamId == 123, "teamId is incorrect. Check CodeforcesTeamSchema."
    assert codeforces_team.teamName == "BBIWY", "teamName is incorrect. Check CodeforcesTeamSchema."

    team = convert_codeforces_team_schema(codeforces_team)

    assert team.id == 123, "team_id is incorrect. Check convert_codeforces_team_schema."
    assert team.team_name == "BBIWY", "team_name is incorrect. Check convert_codeforces_team_schema."
    assert len(team.users) == 2, "Number of users is incorrect. Check convert_codeforces_team_schema."
