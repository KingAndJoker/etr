from etr.utils.factory import create_contest_model


def test_factury_contest_1():
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


def test_factury_contest_2():
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


def test_factury_contest_none():
    contest = create_contest_model()

    assert contest is None, "contest is None. Check create_contest_model function."
