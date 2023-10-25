from sqlalchemy import Engine
from sqlalchemy.orm import Session

from etr.models.user import User
from etr.models.team import Team


def test_user_create(in_memory_db_empty: Engine):
    """ Test create user """

    engine = in_memory_db_empty

    with Session(engine) as session:
        user = User(handle="tourist")
        session.add(user)
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(
            User.handle == "tourist"
        ).one_or_none()
        assert user.handle == "tourist", "The user was created incorrectly"
        assert user.watch, "The user was created incorrectly"

        user = session.query(User).filter(User.handle == "zxc").one_or_none()
        assert user is None, "ORM found a non-existent user"


def test_user_update(in_memory_db_empty: Engine):
    """ Test update value field user """

    engine = in_memory_db_empty

    with Session(engine) as session:
        user = User(handle="tourist")
        session.add(user)
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(
            User.handle == "tourist"
        ).one_or_none()
        user.city = "Gomel"
        user.watch = False
        session.add(user)
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(
            User.handle == "tourist"
        ).one_or_none()
        assert user.city == "Gomel", "Incorrectly updated city"
        assert not user.watch, "Incorrectly updated a watch field"


def test_user_delete(in_memory_db_empty: Engine):
    """ Test delete user """

    engine = in_memory_db_empty

    with Session(engine) as session:
        user = User(handle="tourist")
        session.add(user)
        user = User(handle="zxc")
        session.add(user)
        session.commit()

    with Session(engine) as session:
        session.query(User).filter(User.handle == "tourist").delete()
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(
            User.handle == "tourist"
        ).one_or_none()
        assert user is None, "ORM does not delete user"

        user = session.query(User).filter(User.handle == "zxc").one_or_none()
        assert user is not None, "ORM deletes the wrong user"


def test_user_team(in_memory_db_empty: Engine):
    """ Test user team """

    engine = in_memory_db_empty

    with Session(engine) as session:
        user = User(handle="tourist")
        session.add(user)
        user = User(handle="zxc")
        session.add(user)
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(
            User.handle == "tourist"
        ).one_or_none()
        user2 = session.query(User).filter(User.handle == "zxc").one_or_none()
        team = Team(teamName="team")
        team.users.append(user)
        team.users.append(user2)
        session.add(team)
        session.commit()

    with Session(engine) as session:
        team = session.query(Team).filter(
            Team.teamName == "team"
        ).one_or_none()
        assert len(team.users) == 2, "Incorrectly added users to the team."

        user = session.query(User).filter(
            User.handle == "tourist"
        ).one_or_none()
        user2 = session.query(User).filter(User.handle == "zxc").one_or_none()
        team.users.remove(user)
        team.users.remove(user2)
        session.add(team)
        session.commit()

    with Session(engine) as session:
        team = session.query(Team).filter(
            Team.teamName == "team"
        ).one_or_none()
        assert len(team.users) == 0, "Incorrectly deleted users from the team."
