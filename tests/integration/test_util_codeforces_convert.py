from etr.library.codeforces.codeforces_utils import (
    get_user,
    get_users,
    get_submission
)
from etr.utils.codeforces.convert import (
    convert_codeforces_user_schema,
    convert_codeforces_submission_schema,
    convert_codeforces_submissions_schema
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
