import copy

from sqlalchemy.orm import Session

from etr.db import get_db
from etr.models.user import User
from etr.schemas.user import UserSchema
from etr.library.codeforces.codeforces_utils import get_user as get_codeforces_user
from etr.library.dl_gsu_by_codeforces.parse_students import get_students
from etr.utils.codeforces.convert import convert_codeforces_user_schema
from etr.utils.factory import create_user_model
from etr.utils.dl_gsu_by_codeforces.convert import convert_dl_to_etr


def __get_users_filter_by(session: Session, **kwargs) -> list[User]:
    users = session.query(User).filter_by(
        **kwargs
    ).all()

    return users


def _get_user_db_with_kwargs(**kwargs) -> UserSchema | None:
    with get_db() as session:
        users_db = __get_users_filter_by(session, **kwargs)

        if users_db != []:
            return UserSchema.model_validate(users_db[0])

    return None


def _get_users_db_with_kwargs(**kwargs) -> list[UserSchema]:
    with get_db() as session:
        users_db = __get_users_filter_by(session, **kwargs)

        users_schema = list()
        for user_db in users_db:
            users_schema.append(UserSchema.model_validate(user_db))

    return users_schema


def _get_users_db_with_handles(handles: list[str], **kwargs):
    users_schema = [
        _get_user_db_with_kwargs(handle=handle, **kwargs)
        for handle in handles
    ]
    users_schema = [
        x for x in users_schema if x is not None
    ]
    return users_schema


def get_user(handle: str, watch: bool = True) -> UserSchema | None:
    user_schema = _get_user_db_with_kwargs(
        handle=handle,
        watch=watch
    )

    return user_schema


def get_users(
    lang: str = "en",
    **kwargs
) -> list[UserSchema] | None:
    if "handles" in kwargs:
        users_schema = _get_users_db_with_handles(**kwargs)
    else:
        users_schema = _get_users_db_with_kwargs(**kwargs)

    return users_schema


def add_user(handle: str, lang: str = "en") -> UserSchema | None:
    user_db = _get_user_db_with_kwargs(handle=handle)

    if user_db is not None:
        return None

    # TODO: rewrite without send request to codeforces
    user_schema = convert_codeforces_user_schema(
        get_codeforces_user(handle, lang=lang)
    )

    if user_schema is None:
        return None

    user_schema = _add_new_user_with_schema(user_schema)
    if user_schema is None:
        return None

    return user_schema


def __add_user_with_kwargs(session, **kwargs) -> User | None:
    try:
        user = create_user_model(**kwargs)
        session.add(user)
        session.commit()
        return user
    except:
        session.rollback()
        return None


def _add_new_user_with_schema(user_schema: UserSchema) -> UserSchema | None:
    with get_db() as session:
        user_db = __add_user_with_kwargs(session, **user_schema.model_dump())
        users_db = __get_users_filter_by(session, handle=user_schema.handle)
        if users_db == []:
            user_db = None
        else:
            user_db = users_db[0]

        if user_db is None:
            return None
        
        user_schema = UserSchema.model_validate(user_db)

    return user_schema


def update_user(id: int, **kwargs) -> UserSchema | None:
    user_schema = _get_user_db_with_kwargs(id=id)

    if user_schema is None:
        return None

    if _check_patch_with_kwargs(user_schema, **kwargs):
        user_schema_update = _update_user_with_kwargs(user_schema, **kwargs)

    user_schema_result = UserSchema.model_validate(
        _get_user_db_with_kwargs(id=id)
    )
    return user_schema_result


def _check_patch_with_kwargs(user_schema: UserSchema, **kwargs) -> bool:
    try:
        user_copy_schema = copy.deepcopy(user_schema)
        for key, value in kwargs.items():
            setattr(user_copy_schema, key, value)

        check_user_schema = UserSchema(**user_copy_schema.model_dump())
    except:
        return False

    return True


def __update_user_with_id(session: Session, user_id: int, **kwargs) -> User | None:
    user_db = session.query(User).filter_by(id=user_id).one_or_none()
    if user_db is None:
        return None
    for key, value in kwargs.items():
        if key != "id":
            setattr(user_db, key, value)
    session.add(user_db)
    session.commit()
    return user_db


def _update_user_with_kwargs(user_schema: UserSchema, **kwargs) -> UserSchema:
    with get_db() as session:
        user_db = __update_user_with_id(session, user_id=user_schema.id, **kwargs)
        user_schema = UserSchema.model_validate(user_db) if user_db is not None else None
    return user_schema


def sync_user_with_dl():
    sync_users_schema = convert_dl_to_etr(get_students())

    users_schema = get_users()
    for dl_user in sync_users_schema:
        if dl_user.handle in (user_schema.handle for user_schema in users_schema):
            update_user_schema = _get_user_db_with_kwargs(handle=dl_user.handle)
            _update_user_with_kwargs(update_user_schema, **dl_user.model_dump())
        else:
            _add_new_user_with_schema(dl_user)
