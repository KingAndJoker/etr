from etr.library.codeforces.codeforces_utils import get_user, get_users
# from etr.library.codeforces.schemas.user import CodeforcesUserSchema
# from etr.schemas.user import UserSchema
from etr.utils.codeforces.convert import convert_codeforces_user_schema


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
