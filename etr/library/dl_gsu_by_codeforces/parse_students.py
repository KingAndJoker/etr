import requests

from etr.library.dl_gsu_by_codeforces.schema import StudentSchema


def _get_request() -> list[dict]:
    url = "http://dl.gsu.by/codeforces/api/students"
    response = requests.get(url)
    return response.json()


def get_students() -> list[StudentSchema]:
    students_response = _get_request()
    students = [
        StudentSchema(**student_response)
        for student_response in students_response
    ]
    return students
