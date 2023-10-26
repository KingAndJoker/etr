from etr.db import get_db
from etr.models.user import User
from etr.schemas.user import UserSchema


def _get_user_db_with_handle(handle: str, watch: bool = True) -> User | None:
    with get_db() as session:
        user = session.query(User).filter_by(
            handle=handle,
            watch=watch
        ).one_or_none()

    return user


def _get_all_users(watch: bool = True) -> list[User]:
    with get_db() as session:
        users = session.query(User).all()

    return users


def _get_users_db_with_handle(handles: list[str], watch: bool = True) -> list[User]:
    users = [
        user := _get_user_db_with_handle(handle, watch)
        for handle in handles if user
    ]

    return users


def get_user(handle: str, watch: bool = True) -> UserSchema | None:
    user_db = _get_user_db_with_handle(handle, watch)

    if user_db is None:
        return None

    user = UserSchema.model_validate(user_db)

    return user
