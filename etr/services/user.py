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


def _get_users_filter_by(watch: bool = True, **kwargs) -> list[User]:
    with get_db() as session:
        users = session.query(User).filter_by(
            watch=watch,
            **kwargs
        ).all()

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


def get_users(watch: bool = True, lang: str = "en", **kwargs) -> list[UserSchema] | None:
    users_db = _get_users_filter_by(watch, **kwargs)

    if users_db is None:
        return None

    users = [
        UserSchema.model_validate(user_db)
        for user_db in users_db
    ]

    return users
