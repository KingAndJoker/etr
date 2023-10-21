""" def of converting Codeforces schemas to etr schemas """
from etr.library.codeforces.schemas.user import CodeforcesUserSchema
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema
from etr.library.codeforces.schemas.submission import CodeforcesSubmissionSchema
from etr.library.codeforces.schemas.problem import CodeforcesProblemSchema
from etr.library.codeforces.schemas.contest import CodeforcesContestSchema
from etr.schemas.user import UserSchema
from etr.schemas.team import TeamSchema
from etr.schemas.submission import SubmissionSchema
from etr.schemas.problem import ProblemSchema
from etr.schemas.contest import ContestSchema


def convert_codeforces_user_schema(codeforces_user: CodeforcesUserSchema | None) -> UserSchema | None:
    """func converting user schema"""

    if codeforces_user is None:
        return None
    
    user = UserSchema(**codeforces_user.model_dump())

    return user


def convert_codeforces_team_schema(codeforces_team: CodeforcesTeamSchema | None) -> TeamSchema | None:
    """func converting team schema"""

    if codeforces_team is None:
        return None

    team = TeamSchema(**codeforces_team.model_dump())

    return team


def convert_codeforces_submission_schema(codeforces_submission: CodeforcesSubmissionSchema | None) -> SubmissionSchema | None:
    """func converting submission schema"""

    if codeforces_submission is None:
        return None

    submission = SubmissionSchema(**codeforces_submission.model_dump())

    return submission


def convert_codeforces_submissions_schema(codeforces_submissions: list[CodeforcesSubmissionSchema] | None) -> list[SubmissionSchema] | None:
    """func converting submissions schema"""

    if codeforces_submissions is None:
        return None

    submissions = [
        convert_codeforces_submission_schema(codeforces_submission)
        for codeforces_submission in codeforces_submissions
    ]

    return submissions


def convert_codeforces_problem_schema(codeforces_problem: CodeforcesProblemSchema | None) -> ProblemSchema | None:
    """func converting problem schema"""

    if codeforces_problem is None:
        return None

    problem = ProblemSchema(**codeforces_problem.model_dump())

    return problem


def convert_codeforces_problems_schema(codeforces_problems: list[CodeforcesProblemSchema] | None) -> list[ProblemSchema] | None:
    """func converting problems schema"""

    if codeforces_problems is None:
        return None

    problems = [
        convert_codeforces_problem_schema(codeforces_problem)
        for codeforces_problem in codeforces_problems
    ]

    return problems


def convert_codeforces_contest_schema(codeforces_contest: CodeforcesContestSchema | None) -> ContestSchema | None:
    """func converting contest schema"""

    if codeforces_contest is None:
        return None

    contest = ContestSchema(**codeforces_contest.model_dump())

    return contest
