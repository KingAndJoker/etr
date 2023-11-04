from etr.library.dl_gsu_by_codeforces.schema import StudentSchema
from etr.schemas.user import UserSchema


def _contert(student: StudentSchema) -> UserSchema:
    user = UserSchema(
        **student.model_dump()
    )
    return user


def convert_dl_to_etr(students: list[StudentSchema]) -> list[UserSchema]:
    users = [
        _contert(student)
        for student in students
    ]
    return users
