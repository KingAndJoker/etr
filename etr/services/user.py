from etr.db import get_db
from etr.models.user import User
from etr.schemas.user import UserSchema

def get_users() -> list[dict]:
    with get_db() as session:
        users = session.query(User).filter(User.watch).all()

    users = [
        UserSchema.model_validate(user).model_dump()
        for user in users
    ]

    return users
