from sqlalchemy import Engine
from sqlalchemy.orm import Session

from etr.models.submission import Submission
from etr.models.contest import Contest
from etr.models.problem import Problem
from etr.models.user import User
from etr.models.team import Team


def test_create_submission_user(in_memory_db_empty: Engine):
    """Test creating a user submission."""

    with Session(in_memory_db_empty) as session:
        contest = Contest(
            id=1,
            name="Codeforces Round #123",
            type="CF",
            phase="FINISHED",
            frozen=True,
            duration_seconds=7200,
            start_time_seconds=1610628000,
            relative_time_seconds=1610628000,
            prepared_by="MikeMirzayanov",
            website_url="https://codeforces.com/contest/123",
            description="",
            difficulty=3400,
            kind="official",
            icpc_region="Europe",
            country="Belarus",
            city="Gomel",
            season="Winter"
        )
        session.add(contest)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=1,
            index="A",
            name="Two Sum"
        )
        session.add(problem)
        session.commit()

    with Session(in_memory_db_empty) as session:
        user = User(
            handle="cool_proger"
        )
        session.add(user)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one()
        user = session.query(User).one()

        assert problem is not None, "problem is None."
        assert user is not None, "user is None."

        submission = Submission(
            id=1,
            contest_id=1,
            creation_time_seconds=1000,
            relative_time_seconds=2000,
            problem_id=problem.id,
            verdict="OK",
            programming_language="Python",
            author_id=user.id,
            testset="TESTS",
            passed_test_count=12,
            time_consumed_millis=1000,
            memory_consumed_bytes=1000,
            points=545
        )
        session.add(submission)
        session.commit()

    with Session(in_memory_db_empty) as session:
        submission = session.query(Submission).one()
        assert submission is not None, "submission is None."
        assert submission.id == 1, "submission.id != 1."
        assert submission.contest_id == 1, "submission.contest_id != 1."
        assert submission.creation_time_seconds == 1000, "submission.creation_time_seconds != 1000."
        assert submission.relative_time_seconds == 2000, "submission.relative_time_seconds != 2000."
        assert submission.problem_id == 1, "submission.problem_id != 1."
        assert submission.verdict == "OK", "submission.verdict != OK."
        assert submission.programming_language == "Python", "submission.programming_language != Python."
        assert submission.author_id == 1, "submission.author_id != 1."
        assert submission.testset == "TESTS", "submission.testset != TESTS."
        assert submission.passed_test_count == 12, "submission.passed_test_count != 12."
        assert submission.time_consumed_millis == 1000, "submission.time_consumed_millis != 1000."
        assert submission.memory_consumed_bytes == 1000, "submission.memory_consumed_bytes != 1000."
        assert submission.points == 545, "submission.points != 545."

        assert submission.author is not None, "submission.author is None."
        assert submission.author.handle == "cool_proger", "submission.author.handle != cool_proger."
        
        assert submission.problem is not None, "submission.problem is None."
        assert submission.problem.index == "A", "submission.problem.index != A."
        assert submission.problem.name == "Two Sum", "submission.problem.name != Two Sum."


def test_problem_create_team(in_memory_db_empty: Engine):
    """Test creating a team submission."""

    with Session(in_memory_db_empty) as session:
        contest = Contest(
            id=1,
            name="Codeforces Round #123",
            type="CF",
            phase="FINISHED",
            frozen=True,
            duration_seconds=7200,
            start_time_seconds=1610628000,
            relative_time_seconds=1610628000,
            prepared_by="MikeMirzayanov",
            website_url="https://codeforces.com/contest/123",
            description="",
            difficulty=3400,
            kind="official",
            icpc_region="Europe",
            country="Belarus",
            city="Gomel",
            season="Winter"
        )
        session.add(contest)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=1,
            index="A",
            name="Two Sum"
        )
        session.add(problem)
        session.commit()
    
    with Session(in_memory_db_empty) as session:
        users = [
            User(
                handle="cool_proger"
            ),
            User(
                handle="cool_proger2"
            )
        ]
        session.add_all(users)
        session.commit()

    with Session(in_memory_db_empty) as session:
        users = session.query(User).all()
        team = Team(
            id=1,
            team_name="Cool Team",
            users=users
        )
        session.add(team)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one()
        team = session.query(Team).one()

        assert problem is not None, "problem is None."
        assert team is not None, "team is None."

        submission = Submission(
            id=1,
            contest_id=1,
            creation_time_seconds=1000,
            relative_time_seconds=2000,
            problem_id=problem.id,
            verdict="OK",
            programming_language="Python",
            team_id=team.id,
            testset="TESTS",
            passed_test_count=12,
            time_consumed_millis=1000,
            memory_consumed_bytes=1000,
            points=545
        )
        session.add(submission)
        session.commit()

    with Session(in_memory_db_empty) as session:
        submission = session.query(Submission).one()
        assert submission is not None, "submission is None."
        assert submission.id == 1, "submission.id != 1."
        assert submission.contest_id == 1, "submission.contest_id != 1."
        assert submission.creation_time_seconds == 1000, "submission.creation_time_seconds != 1000."
        assert submission.relative_time_seconds == 2000, "submission.relative_time_seconds != 2000."
        assert submission.problem_id == 1, "submission.problem_id != 1."
        assert submission.verdict == "OK", "submission.verdict != OK."
        assert submission.programming_language == "Python", "submission.programming_language != Python."
        assert submission.team_id == 1, "submission.team_id != 1."
        assert submission.testset == "TESTS", "submission.testset != TESTS."
        assert submission.passed_test_count == 12, "submission.passed_test_count != 12."
        assert submission.time_consumed_millis == 1000, "submission.time_consumed_millis != 1000."
        assert submission.memory_consumed_bytes == 1000, "submission.memory_consumed_bytes != 1000."
        assert submission.points == 545, "submission.points != 545."

        assert submission.team is not None, "submission.team is None."
        assert submission.team.team_name == "Cool Team", "submission.team.team_name != Cool Team."
        assert len(submission.team.users) == 2, "len(submission.team.users) != 2."
        assert submission.team.users[0].handle == "cool_proger", "submission.team.users[0].handle != cool_proger."
        assert submission.team.users[1].handle == "cool_proger2", "submission.team.users[1].handle != cool_proger2."

        assert submission.problem is not None, "submission.problem is None."
        assert submission.problem.index == "A", "submission.problem.index != A."
        assert submission.problem.name == "Two Sum", "submission.problem.name != Two Sum."


def test_submission_update(in_memory_db_empty: Engine):
    """Test updating a submission."""

    with Session(in_memory_db_empty) as session:
        contest = Contest(
            id=1,
            name="Codeforces Round #123",
            type="CF",
            phase="FINISHED",
            frozen=True,
            duration_seconds=7200,
            start_time_seconds=1610628000,
            relative_time_seconds=1610628000,
            prepared_by="MikeMirzayanov",
            website_url="https://codeforces.com/contest/123",
            description="",
            difficulty=3400,
            kind="official",
            icpc_region="Europe",
            country="Belarus",
            city="Gomel",
            season="Winter"
        )
        session.add(contest)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=1,
            index="A",
            name="Two Sum"
        )
        session.add(problem)
        session.commit()

    with Session(in_memory_db_empty) as session:
        user = User(
            handle="cool_proger"
        )
        session.add(user)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one()
        user = session.query(User).one()

        assert problem is not None, "problem is None."
        assert user is not None, "user is None."

        submission = Submission(
            id=1,
            contest_id=1,
            creation_time_seconds=1000,
            relative_time_seconds=2000,
            problem_id=problem.id,
            verdict="OK",
            programming_language="Python",
            author_id=user.id,
            testset="TESTS",
            passed_test_count=12,
            time_consumed_millis=1000,
            memory_consumed_bytes=1000,
            points=545
        )
        session.add(submission)
        session.commit()

    with Session(in_memory_db_empty) as session:
        submission = session.query(Submission).one()
        submission.points = 1000
        session.add(submission)
        session.commit()

    with Session(in_memory_db_empty) as session:
        submission = session.query(Submission).one()
        assert submission is not None, "submission is None."
        assert submission.id == 1, "submission.id != 1."
        assert submission.points == 1000, "submission.points != 1000."


def test_submission_delete(in_memory_db_empty: Engine):
    """Test deleting a submission."""

    with Session(in_memory_db_empty) as session:
        contest = Contest(
            id=1,
            name="Codeforces Round #123",
            type="CF",
            phase="FINISHED",
            frozen=True,
            duration_seconds=7200,
            start_time_seconds=1610628000,
            relative_time_seconds=1610628000,
            prepared_by="MikeMirzayanov",
            website_url="https://codeforces.com/contest/123",
            description="",
            difficulty=3400,
            kind="official",
            icpc_region="Europe",
            country="Belarus",
            city="Gomel",
            season="Winter"
        )
        session.add(contest)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=1,
            index="A",
            name="Two Sum"
        )
        session.add(problem)
        session.commit()

    with Session(in_memory_db_empty) as session:
        user = User(
            handle="cool_proger"
        )
        session.add(user)
        session.commit()

    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one()
        user = session.query(User).one()

        assert problem is not None, "problem is None."
        assert user is not None, "user is None."

        submission = Submission(
            id=1,
            contest_id=1,
            creation_time_seconds=1000,
            relative_time_seconds=2000,
            problem_id=problem.id,
            verdict="OK",
            programming_language="Python",
            author_id=user.id,
            testset="TESTS",
            passed_test_count=12,
            time_consumed_millis=1000,
            memory_consumed_bytes=1000,
            points=545
        )
        session.add(submission)
        session.commit()

    with Session(in_memory_db_empty) as session:
        submission = session.query(Submission).one()
        session.delete(submission)
        session.commit()

    with Session(in_memory_db_empty) as session:
        submission = session.query(Submission).one_or_none()
        assert submission is None, "submission is not None."
