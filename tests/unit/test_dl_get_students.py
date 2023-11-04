from etr.library.dl_gsu_by_codeforces.parse_students import get_students
from etr.library.dl_gsu_by_codeforces.schema import StudentSchema
from etr.utils.dl_gsu_by_codeforces.convert import convert_dl_to_etr
from etr.schemas.user import UserSchema


def test_get_students():
    students = get_students()
    assert isinstance(students, list)
    assert len(students) > 0
    assert isinstance(students[0], StudentSchema)


def test_convert_dl_to_etr():
    students = get_students()
    users = convert_dl_to_etr(students)
    assert isinstance(users, list)
    assert len(users) > 0
    assert isinstance(users[0], UserSchema)
