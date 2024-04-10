from etr.utils.request import Request
from .utils.generate_url import generate_url
from .schemas.problem import CodeforcesProblemSchema, CodeforcesProblemStatistics


def problems(
    tags: str | None = None,
    problemsetName: str | None = None,
    lang: str = "ru"
) -> tuple[list[CodeforcesProblemSchema], list[CodeforcesProblemSchema]]:
    """метод для получения задач и статистики по этим задачам

    Args:
        tags (str, optional): Список тегов, разделенных точкой с запятой. По умолчанию не надо.
        problemsetName (str, optional): Короткое имя дополнительного архива, например 'acmsguru', по умолчанию не надо.
        lang: str = "ru": язык ответа, по умолчанию русский.

    Returns:
        _type_: tuple(list[CodeforcesProblemSchema], list[CodeforcesProblemSchema])
    """
    kwargs = {
        "tags": tags,
        "problemsetName": problemsetName,
        "lang": lang
    }
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    problemset_problems = generate_url(
        "problemset.problems",
        **kwargs
    )
    request = Request()
    response = request.handle(problemset_problems, "GET")
    
    if not response.ok:
        return ([], [])
    
    data = response.json()
    
    if data["status"] != "OK":
        return ([], [])
    
    problems: list[CodeforcesProblemSchema] = []
    problems_statistics: list[CodeforcesProblemStatistics] = []
    
    for problem in data["result"]["problems"]:
        problems.append(CodeforcesProblemSchema(**problem))

    for problem_statistics in data["result"]["problemStatistics"]:
        problems_statistics.append(CodeforcesProblemStatistics(**problem_statistics))
    
    return (problems, problems_statistics)
