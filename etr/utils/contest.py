from etr.schemas.submission import SubmissionSchema


def get_count_success_tasks(submissions: list[SubmissionSchema]):
    return sum([1 for submission in submissions if submission.verdict == "OK"])
