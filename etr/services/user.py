from etr.db import get_db
from etr.models.user import User
from etr.schemas.user import UserSchema
from etr.library.codeforces.codeforces_utils import get_user as get_codeforces_user
from etr.utils.codeforces.convert import convert_codeforces_user_schema
from etr.utils.factory import create_user_model


def _get_user_db_with_kwargs(**kwargs) -> User | None:
    with get_db() as session:
        user = session.query(User).filter_by(
            **kwargs
        ).one_or_none()

    return user


def _get_users_filter_by(**kwargs) -> list[User]:
    with get_db() as session:
        users = session.query(User).filter_by(
            **kwargs
        ).all()

    return users


def _get_users_db_with_handle(handles: list[str], watch: bool = True) -> list[User]:
    users = [
        user := _get_user_db_with_kwargs(
            handle=handle,
            watch=watch
        )
        for handle in handles if user
    ]

    return users


def get_user(handle: str, watch: bool = True) -> UserSchema | None:
    user_db = _get_user_db_with_kwargs(
        handle=handle,
        watch=watch
    )

    if user_db is None:
        return None

    user = UserSchema.model_validate(user_db)

    return user


def get_users(
    lang: str = "en",
    handles: list[str] | None = None,
    **kwargs
) -> list[UserSchema] | None:

    if handles:
        users_db = list()
        for handle in handles:
            users_db.extend(_get_users_filter_by(handle=handle, **kwargs))
    else:
        users_db = _get_users_filter_by(**kwargs)

    users_db = [user_db for user_db in users_db if user_db is not None]

    users = [
        UserSchema.model_validate(user_db)
        for user_db in users_db
    ]

    return users


def add_user(handle: str, lang: str = "en") -> UserSchema | None:
    user_db = _get_user_db_with_kwargs(handle=handle)

    if user_db is not None:
        return None

    user_schema = convert_codeforces_user_schema(
        get_codeforces_user(handle, lang=lang)
    )

    if user_schema is None:
        return None

    user_schema = _add_new_user_with_schema(user_schema)
    if user_db is None:
        return None

    return user_schema


def _add_new_user_with_schema(user_schema: UserSchema) -> UserSchema | None:
    user_db = create_user_model(**user_schema.model_dump())

    if user_db is None:
        return None

    with get_db() as session:
        session.add(user_db)
        session.commit()

    return user_schema


def update_user(id: int, **kwargs) -> UserSchema | None:
    user_db = _get_user_db_with_kwargs(id=id)

    if user_db is None:
        return None

    if _check_patch_with_kwargs(user_db, **kwargs):
        user_db = _update_user_with_kwargs(user_db, **kwargs)

    user_schema = UserSchema.model_validate(
        _get_user_db_with_kwargs(id=id)
    )
    return user_schema


def _check_patch_with_kwargs(user_db: User, **kwargs) -> bool:
    user_schema = UserSchema.model_validate(user_db)

    try:
        for key, value in kwargs.items():
            setattr(user_schema, key, value)
    except:
        return False

    try:
        check_user_schema = UserSchema(**user_schema.model_dump())
    except:
        return False

    return True


def _update_user_with_kwargs(user_db: User, **kwargs) -> User:
    for key, value in kwargs.items():
        setattr(user_db, key, value)

    with get_db() as session:
        session.add(user_db)
        session.commit()

    return user_db
