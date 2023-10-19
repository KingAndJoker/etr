from sqlalchemy import Engine
from sqlalchemy.orm import Session

from etr.models.user import User
from etr.models.team import Team, teams_users


def test_user_create(in_memory_db: Engine):
    """ Test create user """

    engine = in_memory_db

    with Session(engine) as session:
        user = User(handle="tourist")
        session.add(user)
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(User.handle == "tourist").one_or_none()
        assert user.handle == "tourist", "The user was created incorrectly"
        assert user.watch == True, "The user was created incorrectly"

        user = session.query(User).filter(User.handle == "zxc").one_or_none()
        assert user is None, "ORM found a non-existent user"


def test_user_update(in_memory_db: Engine):
    """ Test update value field user """

    engine = in_memory_db
    
    with Session(engine) as session:
        user = User(handle="tourist")
        session.add(user)
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(User.handle == "tourist").one_or_none()
        user.city = "Gomel"
        user.watch = False
        session.add(user)
        session.commit()

    with Session(engine) as session:
        user = session.query(User).filter(User.handle == "tourist").one_or_none()
        assert user.city == "Gomel", "Incorrectly updated city"
        assert user.watch == False, "Incorrectly updated a watch field"


def test_user_delete(in_memory_db: Engine):
    """ Test delete user """

    engine = in_memory_db

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
        user = session.query(User).filter(User.handle == "tourist").one_or_none()
        assert user is None, "ORM does not delete user"

        user = session.query(User).filter(User.handle == "zxc").one_or_none()
        assert user is not None, "ORM deletes the wrong user"
