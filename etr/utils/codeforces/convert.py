""" def of converting Codeforces schemas to etr schemas """
from etr.library.codeforces.schemas.user import CodeforcesUserSchema
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema
from etr.library.codeforces.schemas.submission import CodeforcesSubmissionSchema
from etr.library.codeforces.schemas.problem import CodeforcesProblemSchema
from etr.library.codeforces.schemas.problem import CodeforcesProblemStatistics
from etr.library.codeforces.schemas.contest import CodeforcesContestSchema
from etr.schemas.user import UserSchema
from etr.schemas.team import TeamSchema
from etr.schemas.submission import SubmissionSchema
from etr.schemas.problem import ProblemSchema
from etr.schemas.problem import ProblemStatistics
from etr.schemas.contest import ContestSchema


def convert_codeforces_user_schema(codeforces_user: CodeforcesUserSchema | None) -> UserSchema | None:
    """func converting user schema"""

    if codeforces_user is None:
        return None
    
    user = UserSchema(
        id=codeforces_user.id,
        handle=codeforces_user.handle,
        email=codeforces_user.email,
        vk_id=codeforces_user.vkId,
        open_id=codeforces_user.openId,
        first_name=codeforces_user.firstName,
        last_name=codeforces_user.lastName,
        country=codeforces_user.country,
        city=codeforces_user.city,
        organization=codeforces_user.organization,
        contribution=codeforces_user.contribution,
        rank=codeforces_user.rank,
        rating=codeforces_user.rating,
        max_rank=codeforces_user.maxRank,
        max_rating=codeforces_user.maxRating,
        last_online_time_seconds=codeforces_user.lastOnlineTimeSeconds,
        registration_time_seconds=codeforces_user.registrationTimeSeconds,
        friend_of_count=codeforces_user.friendOfCount,
        avatar=codeforces_user.avatar,
        title_photo=codeforces_user.titlePhoto,
    )

    return user


def convert_codeforces_team_schema(codeforces_team: CodeforcesTeamSchema | None) -> TeamSchema | None:
    """func converting team schema"""

    if codeforces_team is None:
        return None

    team = TeamSchema(
        id=codeforces_team.teamId,
        team_name=codeforces_team.teamName,
        users=codeforces_team.users,
    )

    return team


def convert_codeforces_submission_schema(codeforces_submission: CodeforcesSubmissionSchema | None) -> SubmissionSchema | None:
    """func converting submission schema"""

    if codeforces_submission is None:
        return None

    codeforces_sub = codeforces_submission.model_copy()
    if isinstance(codeforces_sub.author, CodeforcesUserSchema):
        codeforces_sub.author = convert_codeforces_user_schema(codeforces_sub.author)
    else:
        codeforces_sub.author = convert_codeforces_team_schema(codeforces_sub.author)
        

    submission = SubmissionSchema(
        id=codeforces_sub.id,
        contest_id=codeforces_sub.contestId,
        creation_time_seconds=codeforces_sub.creationTimeSeconds,
        relative_time_seconds=codeforces_sub.relativeTimeSeconds,
        problem=codeforces_sub.problem,
        author=codeforces_sub.author,
        programming_language=codeforces_sub.programmingLanguage,
        verdict=codeforces_sub.verdict,
        testset=codeforces_sub.testset,
        passed_test_count=codeforces_sub.passedTestCount,
        time_consumed_millis=codeforces_sub.timeConsumedMillis,
        memory_consumed_bytes=codeforces_sub.memoryConsumedBytes,
        points=codeforces_sub.points,
        type_of_member=codeforces_sub.participantType,
    )

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

    problem = ProblemSchema(
        id=codeforces_problem.id,
        contest_id=codeforces_problem.contestId,
        problemset_name=codeforces_problem.problemsetName,
        index=codeforces_problem.index,
        name=codeforces_problem.name,
        type=codeforces_problem.type,
        points=codeforces_problem.points,
        rating=codeforces_problem.rating,
        tags=codeforces_problem.tags,
    )

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

    contest = ContestSchema(
        id=codeforces_contest.id,
        name=codeforces_contest.name,
        type=codeforces_contest.type,
        phase=codeforces_contest.phase,
        frozen=codeforces_contest.frozen,
        duration_seconds=codeforces_contest.durationSeconds,
        start_time_seconds=codeforces_contest.startTimeSeconds,
        relative_time_seconds=codeforces_contest.relativeTimeSeconds,
        prepared_by=codeforces_contest.preparedBy,
        website_url=codeforces_contest.websiteUrl,
        description=codeforces_contest.description,
        difficulty=codeforces_contest.difficulty,
        kind=codeforces_contest.kind,
        icpc_region=codeforces_contest.icpcRegion,
        country=codeforces_contest.country,
        city=codeforces_contest.city,
        season=codeforces_contest.season,
    )
    contest.problems = convert_codeforces_problems_schema(codeforces_contest.problems)

    return contest


def convert_codeforces_problems_statistics(codeforces_problems_statistics: list[CodeforcesProblemStatistics]):
    problems_statistics: list[ProblemStatistics] = []
    for codeforces_problem_stat in codeforces_problems_statistics:
        problems_statistics.append(ProblemStatistics(
            contest_id=codeforces_problem_stat.contestId,
            index=codeforces_problem_stat.index,
            solved_count=codeforces_problem_stat.solvedCount
        ))
    return problems_statistics
