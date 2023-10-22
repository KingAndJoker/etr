from etr.utils.factory import (
    create_contest_model,
    create_problem_model,
    create_submission_model
)
from etr.models.problem import Problem
from etr.schemas.problem import ProblemSchema


def test_factory_contest_1():
    contest = create_contest_model(
        id=1,
        name="Test Contest #1",
        type="special",
        frozen=False,
        duration_seconds=111111,
        start_time_seconds=222222,
        relative_time_seconds=333333,
        prepared_by="Test User",
        website_url="https://test.com",
        description="Test contest description",
        difficulty=1000,
        kind="virtual",
        icpc_region="Europe",
        country="Russia",
        city="Moscow",
        season="Summer",
        duration_time="1 day 5 hours 18 minutes 31 seconds",
        start_datatime="01 01 2021 00:00:00"
    )

    assert contest is not None, "contest is None. Check create_contest_model function."
    assert contest.id == 1, "id is not equal 1. Check create_contest_model function."
    assert contest.name == "Test Contest #1", "name is not equal 'Test Contest #1'. Check create_contest_model function."
    assert contest.type == "special", "type is not equal 'special'. Check create_contest_model function."
    assert contest.frozen == False, "frozen is not equal False. Check create_contest_model function."
    assert contest.duration_seconds == 111111, "duration_seconds is not equal 111111. Check create_contest_model function."
    assert contest.start_time_seconds == 222222, "start_time_seconds is not equal 222222. Check create_contest_model function."
    assert contest.relative_time_seconds == 333333, "relative_time_seconds is not equal 333333. Check create_contest_model function."
    assert contest.prepared_by == "Test User", "prepared_by is not equal 'Test User'. Check create_contest_model function."
    assert contest.website_url == "https://test.com", "website_url is not equal 'https://test.com'. Check create_contest_model function."
    assert contest.description == "Test contest description", "description is not equal 'Test contest description'. Check create_contest_model function."
    assert contest.difficulty == 1000, "difficulty is not equal 1000. Check create_contest_model function."
    assert contest.kind == "virtual", "kind is not equal 'virtual'. Check create_contest_model function."
    assert contest.icpc_region == "Europe", "icpc_region is not equal 'Europe'. Check create_contest_model function."
    assert contest.country == "Russia", "country is not equal 'Russia'. Check create_contest_model function."
    assert contest.city == "Moscow", "city is not equal 'Moscow'. Check create_contest_model function."
    assert contest.season == "Summer", "season is not equal 'Summer'. Check create_contest_model function."


def test_factory_contest_2():
    contest = create_contest_model(
        id=2,
        name="Test Contest #2",
        type="cf",
        frozen=True,
        duration_seconds=222222,
        start_time_seconds=333333,
        relative_time_seconds=444444
    )

    assert contest is not None, "contest is None. Check create_contest_model function."
    assert contest.id == 2, "id is not equal 2. Check create_contest_model function."
    assert contest.name == "Test Contest #2", "name is not equal 'Test Contest #2'. Check create_contest_model function."
    assert contest.type == "cf", "type is not equal 'cf'. Check create_contest_model function."
    assert contest.frozen == True, "frozen is not equal True. Check create_contest_model function."
    assert contest.duration_seconds == 222222, "duration_seconds is not equal 222222. Check create_contest_model function."
    assert contest.start_time_seconds == 333333, "start_time_seconds is not equal 333333. Check create_contest_model function."
    assert contest.relative_time_seconds == 444444, "relative_time_seconds is not equal 444444. Check create_contest_model function."
    assert contest.prepared_by is None, "prepared_by is not equal None. Check create_contest_model function."
    assert contest.website_url is None, "website_url is not equal None. Check create_contest_model function."
    assert contest.description is None, "description is not equal None. Check create_contest_model function."
    assert contest.difficulty is None, "difficulty is not equal None. Check create_contest_model function."
    assert contest.kind is None, "kind is not equal None. Check create_contest_model function."
    assert contest.icpc_region is None, "icpc_region is not equal None. Check create_contest_model function."
    assert contest.country is None, "country is not equal None. Check create_contest_model function."
    assert contest.city is None, "city is not equal None. Check create_contest_model function."
    assert contest.season is None, "season is not equal None. Check create_contest_model function."


def test_factory_contest_none():
    contest = create_contest_model()

    assert contest is None, "contest is None. Check create_contest_model function."


def test_factory_problem_1():
    problem: Problem | None = create_problem_model(
        id=1,
        contest_id=1,
        index="A",
        name="Test Problem #1",
        type="PROGRAMMING",
        points=1500,
        rating=1000,
        tags=["implementation", "math", "number theory"],
        zxc="123"
    )

    assert problem is not None, "problem is None. Check create_problem_model function."
    assert problem.id == 1, "id is not equal 1. Check create_problem_model function."
    assert problem.contest_id == 1, "contest_id is not equal 1. Check create_problem_model function."
    assert problem.index == "A", "index is not equal 'A'. Check create_problem_model function."
    assert problem.name == "Test Problem #1", "name is not equal 'Test Problem #1'. Check create_problem_model function."
    assert problem.type == "PROGRAMMING", "type is not equal 'PROGRAMMING'. Check create_problem_model function."
    assert problem.points == 1500, "points is not equal 1500. Check create_problem_model function."
    assert problem.rating == 1000, "rating is not equal 1000. Check create_problem_model function."


def test_factory_problem_2():
    problem: Problem | None = create_problem_model(
        id=2,
        index="B",
        name="Test Problem #2",
    )

    assert problem is not None, "problem is None. Check create_problem_model function."
    assert problem.id == 2, "id is not equal 2. Check create_problem_model function."
    assert problem.contest_id is None, "contest_id is not equal None. Check create_problem_model function."
    assert problem.index == "B", "index is not equal 'B'. Check create_problem_model function."
    assert problem.name == "Test Problem #2", "name is not equal 'Test Problem #2'. Check create_problem_model function."
    assert problem.type is None, "type is not equal None. Check create_problem_model function."
    assert problem.points is None, "points is not equal None. Check create_problem_model function."


def test_factory_problem_none():
    problem: Problem | None = create_problem_model()

    assert problem is None, "problem is None. Check create_problem_model function."


def test_factory_problem_with_missing_necessary_field():
    problem: Problem | None = create_problem_model(
        id=1
    )

    assert problem is None, "problem is not None. Check create_problem_model function."


def test_factory_submission_user():
    submission = create_submission_model(
        id=1,
        contest_id=1,
        problem_id=1,
        author_id=1,
        programming_language="Python",
        verdict="OK",
        testset="TESTS",
        passed_test_count=10,
        time_consumed_millis=1000,
        memory_consumed_bytes=1000000,
        points=1000,
        creation_time_seconds=111111,
        relative_time_seconds=222222,
        zxc="123"
    )

    assert submission is not None, "submission is None. Check create_submission_model function."
    assert submission.id == 1, "id is not equal 1. Check create_submission_model function."
    assert submission.contest_id == 1, "contest_id is not equal 1. Check create_submission_model function."
    assert submission.problem_id == 1, "problem_id is not equal 1. Check create_submission_model function."
    assert submission.author_id == 1, "author_id is not equal 1. Check create_submission_model function."
    assert submission.team_id is None, "team_id is not equal None. Check create_submission_model function."
    assert submission.programming_language == "Python", "programming_language is not equal 'Python'. Check create_submission_model function."
    assert submission.verdict == "OK", "verdict is not equal 'OK'. Check create_submission_model function."
    assert submission.testset == "TESTS", "testset is not equal 'TESTS'. Check create_submission_model function."
    assert submission.passed_test_count == 10, "passed_test_count is not equal 10. Check create_submission_model function."
    assert submission.time_consumed_millis == 1000, "time_consumed_millis is not equal 1000. Check create_submission_model function."
    assert submission.memory_consumed_bytes == 1000000, "memory_consumed_bytes is not equal 1000000. Check create_submission_model function."
    assert submission.points == 1000, "points is not equal 1000. Check create_submission_model function."
    assert submission.creation_time_seconds == 111111, "creation_time_seconds is not equal 111111. Check create_submission_model function."
    assert submission.relative_time_seconds == 222222, "relative_time_seconds is not equal 222222. Check create_submission_model function."


def test_factory_submission_team():
    submission = create_submission_model(
        id=2,
        contest_id=2,
        problem_id=2,
        team_id=2,
        programming_language="C++",
        verdict="WRONG_ANSWER",
        testset="PRETESTS",
        passed_test_count=5,
        time_consumed_millis=500,
        memory_consumed_bytes=500000,
        points=500,
        creation_time_seconds=222222,
        relative_time_seconds=333333,
    )

    assert submission is not None, "submission is None. Check create_submission_model function."
    assert submission.id == 2, "id is not equal 2. Check create_submission_model function."
    assert submission.contest_id == 2, "contest_id is not equal 2. Check create_submission_model function."
    assert submission.problem_id == 2, "problem_id is not equal 2. Check create_submission_model function."
    assert submission.author_id is None, "author_id is not equal None. Check create_submission_model function."
    assert submission.team_id == 2, "team_id is not equal 2. Check create_submission_model function."
    assert submission.programming_language == "C++", "programming_language is not equal 'C++'. Check create_submission_model function."
    assert submission.verdict == "WRONG_ANSWER", "verdict is not equal 'WRONG_ANSWER'. Check create_submission_model function."
    assert submission.testset == "PRETESTS", "testset is not equal 'PRETESTS'. Check create_submission_model function."
    assert submission.passed_test_count == 5, "passed_test_count is not equal 5. Check create_submission_model function."
    assert submission.time_consumed_millis == 500, "time_consumed_millis is not equal 500. Check create_submission_model function."
    assert submission.memory_consumed_bytes == 500000, "memory_consumed_bytes is not equal 500000. Check create_submission_model function."
    assert submission.points == 500, "points is not equal 500. Check create_submission_model function."
    assert submission.creation_time_seconds == 222222, "creation_time_seconds is not equal 222222. Check create_submission_model function."
    assert submission.relative_time_seconds == 333333, "relative_time_seconds is not equal 333333. Check create_submission_model function."


def test_factory_submission_with_problem_schema():
    submission = create_submission_model(
        id=3,
        contest_id=3,
        programming_language="Java",
        verdict="COMPILATION_ERROR",
        testset="TESTS",
        passed_test_count=0,
        time_consumed_millis=0,
        memory_consumed_bytes=0,
        points=0,
        creation_time_seconds=333333,
        relative_time_seconds=444444,
        problem=ProblemSchema(
            id=4,
            contest_id=3,
            index="C",
            name="Test Problem #3",
            type="PROGRAMMING",
            points=1500,
            rating=1000,
            tags=["implementation", "math", "number theory"]
        )
    )

    assert submission is not None, "submission is None. Check create_submission_model function."
    assert submission.id == 3, "id is not equal 3. Check create_submission_model function."
    assert submission.contest_id == 3, "contest_id is not equal 3. Check create_submission_model function."
    assert submission.problem_id == 4, "problem_id is not equal 4. Check create_submission_model function."
    assert submission.author_id is None, "author_id is not equal None. Check create_submission_model function."
    assert submission.team_id is None, "team_id is not equal None. Check create_submission_model function."
    assert submission.programming_language == "Java", "programming_language is not equal 'Java'. Check create_submission_model function."
    assert submission.verdict == "COMPILATION_ERROR", "verdict is not equal 'COMPILATION_ERROR'. Check create_submission_model function."
    assert submission.testset == "TESTS", "testset is not equal 'TESTS'. Check create_submission_model function."
    assert submission.passed_test_count == 0, "passed_test_count is not equal 0. Check create_submission_model function."
    assert submission.time_consumed_millis == 0, "time_consumed_millis is not equal 0. Check create_submission_model function."
    assert submission.memory_consumed_bytes == 0, "memory_consumed_bytes is not equal 0. Check create_submission_model function."
    assert submission.points == 0, "points is not equal 0. Check create_submission_model function."
    assert submission.creation_time_seconds == 333333, "creation_time_seconds is not equal 333333. Check create_submission_model function."
    assert submission.relative_time_seconds == 444444, "relative_time_seconds is not equal 444444. Check create_submission_model function."


def test_factory_submission_none():
    submission = create_submission_model()

    assert submission is None, "submission is not None. Check create_submission_model function."
