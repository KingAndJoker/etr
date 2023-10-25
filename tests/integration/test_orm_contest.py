from sqlalchemy import Engine
from sqlalchemy.orm import Session

from etr.models.contest import Contest


def test_contest_create(in_memory_db_empty: Engine):
    """ Test create contest """

    engine = in_memory_db_empty

    with Session(engine) as session:
        contest = Contest(id=1, name="Test Contest #1")
        session.add(contest)
        session.commit()

    with Session(engine) as session:
        contest = session.query(Contest).filter(
            Contest.id == 1
        ).one_or_none()
        assert contest.id == 1, "The contest was created incorrectly."

        contest = session.query(Contest).filter(
            Contest.id == 2
        ).one_or_none()
        assert contest is None, "ORM found a non-existent contest."


def test_create_contest_all_fields(in_memory_db_empty: Engine):
    """ Test create contest with all fields """

    engine = in_memory_db_empty

    with Session(engine) as session:
        contest = Contest(
            id=1,
            name="Test Contest #2",
            type="CF",
            phase="FINISHED",
            frozen=True,
            duration_seconds=100,
            start_time_seconds=200,
            relative_time_seconds=300,
            prepared_by="Test",
            website_url="https://test.com",
            description="Test description",
            difficulty=100,
            kind="ICPC",
            icpc_region="Europe",
            country="Belarus",
            city="Gomel",
            season="Summer"
        )

        session.add(contest)
        session.commit()

    with Session(engine) as session:
        contest = session.query(Contest).filter(
            Contest.id == 1
        ).one_or_none()

        assert contest is not None, "The contest was not created."
        assert contest.id == 1, "The contest was created incorrectly."
        assert contest.name == "Test Contest #2", "The contest was created incorrectly."
        assert contest.type == "CF", "The contest was created incorrectly."
        assert contest.phase == "FINISHED", "The contest was created incorrectly."
        assert contest.frozen is True, "The contest was created incorrectly."
        assert contest.duration_seconds == 100, "The contest was created incorrectly."
        assert contest.start_time_seconds == 200, "The contest was created incorrectly."
        assert contest.relative_time_seconds == 300, "The contest was created incorrectly."
        assert contest.prepared_by == "Test", "The contest was created incorrectly."
        assert contest.website_url == "https://test.com", "The contest was created incorrectly."
        assert contest.description == "Test description", "The contest was created incorrectly."
        assert contest.difficulty == 100, "The contest was created incorrectly."
        assert contest.kind == "ICPC", "The contest was created incorrectly."
        assert contest.icpc_region == "Europe", "The contest was created incorrectly."
        assert contest.country == "Belarus", "The contest was created incorrectly."
        assert contest.city == "Gomel", "The contest was created incorrectly."
        assert contest.season == "Summer", "The contest was created incorrectly."


def test_contest_update(in_memory_db_empty: Engine):
    """ Test update value field contest """

    engine = in_memory_db_empty

    with Session(engine) as session:
        contest = Contest(id=1, name="Test Contest #1")
        session.add(contest)
        session.commit()

    with Session(engine) as session:
        contest = session.query(Contest).filter(
            Contest.id == 1
        ).one_or_none()
        assert contest is not None, "The contest was not created."

        contest.name = "Test Contest #2"
        session.add(contest)
        session.commit()

    with Session(engine) as session:
        contest = session.query(Contest).filter(
            Contest.id == 1
        ).one_or_none()
        assert contest.name == "Test Contest #2", "Incorrectly updated name"


def test_contest_delete(in_memory_db_empty: Engine):
    """ Test delete contest """

    engine = in_memory_db_empty

    with Session(engine) as session:
        contest = Contest(id=1, name="Test Contest #1")
        session.add(contest)
        session.commit()

    with Session(engine) as session:
        contest = session.query(Contest).filter(
            Contest.id == 1
        ).one_or_none()
        assert contest is not None, "The contest was not created."

        session.delete(contest)
        session.commit()

    with Session(engine) as session:
        contest = session.query(Contest).filter(
            Contest.id == 1
        ).one_or_none()
        assert contest is None, "The contest was not deleted."
