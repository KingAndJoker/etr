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


def convert_codeforces_user_schema(codeforces_user: CodeforcesUserSchema) -> UserSchema:
    """func converting user schema"""

    user = UserSchema(**codeforces_user.model_dump())

    return user


def convert_codeforces_team_schema(codeforces_team: CodeforcesTeamSchema) -> TeamSchema:
    """func converting team schema"""

    team = TeamSchema(**codeforces_team.model_dump())

    return team


def convert_codeforces_submission_schema(codeforces_submission: CodeforcesSubmissionSchema) -> SubmissionSchema:
    """func converting submission schema"""

    submission = SubmissionSchema(**codeforces_submission.model_dump())

    return submission


def convert_codeforces_submissions_schema(codeforces_submissions: list[CodeforcesSubmissionSchema]) -> list[SubmissionSchema]:
    """func converting submissions schema"""

    submissions = [
        convert_codeforces_submission_schema(codeforces_submission)
        for codeforces_submission in codeforces_submissions
    ]

    return submissions


def convert_codeforces_problem_schema(codeforces_problem: CodeforcesProblemSchema) -> ProblemSchema:
    """func converting problem schema"""

    problem = ProblemSchema(**codeforces_problem.model_dump())

    return problem


def convert_codeforces_problems_schema(codeforces_problems: list[CodeforcesProblemSchema]) -> list[ProblemSchema]:
    """func converting problems schema"""

    problems = [
        convert_codeforces_problem_schema(codeforces_problem)
        for codeforces_problem in codeforces_problems
    ]

    return problems


def convert_codeforces_contest_schema(codeforces_contest: CodeforcesContestSchema) -> ContestSchema:
    """func converting contest schema"""

    contest = ContestSchema(**codeforces_contest.model_dump())

    return contest
