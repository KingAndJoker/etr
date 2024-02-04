import copy

from sqlalchemy.orm import Session

from etr import db
from etr.models.user import UserOrm
from etr.schemas.user import UserSchema
from etr.utils.factory import create_user_model


def __get_users_filter_by(session: Session, **kwargs) -> list[UserOrm]:
    users = session.query(UserOrm).filter_by(**kwargs).all()
    return users


def _get_user_db_with_kwargs(**kwargs) -> UserSchema | None:
    with db.SessionLocal() as session:
        users_db = __get_users_filter_by(session, **kwargs)
        if users_db != []:
            return UserSchema.model_validate(users_db[0])
    return None


def _get_users_db_with_kwargs(**kwargs) -> list[UserSchema]:
    with db.SessionLocal() as session:
        users_db = __get_users_filter_by(session, **kwargs)
        users_schema = list()
        for user_db in users_db:
            try:
                users_schema.append(UserSchema.model_validate(user_db))
            except:
                pass
    return users_schema


def _get_users_db_with_handles(handles: list[str], **kwargs) -> list[UserSchema]:
    users_schema = [
        _get_user_db_with_kwargs(handle=handle, **kwargs) for handle in handles
    ]
    users_schema = [x for x in users_schema if x is not None]
    return users_schema


def get_user(handle: str, **kwargs) -> UserSchema | None:
    users = get_users(**kwargs)
    for user in users:
        if handle.lower() == user.handle.lower():
            return user
    return None


def get_users(lang: str = "ru", **kwargs) -> list[UserSchema] | None:
    if "handles" in kwargs:
        users_schema = _get_users_db_with_handles(**kwargs)
    else:
        users_schema = _get_users_db_with_kwargs(**kwargs)
    return users_schema


def add_user(user_schema: UserSchema) -> UserSchema | None:
    user_db = _get_user_db_with_kwargs(handle=user_schema.handle)

    if user_db is not None:
        return None

    return _add_new_user_with_schema(user_schema)


def __add_user_with_kwargs(session: Session, **kwargs) -> UserOrm | None:
    try:
        user = create_user_model(**kwargs)
        session.add(user)
        session.commit()
        return user
    except:
        session.rollback()
        return None


def _add_new_user_with_schema(user_schema: UserSchema) -> UserSchema | None:
    with db.SessionLocal() as session:
        user_db = __add_user_with_kwargs(session, **user_schema.model_dump())
        users_db = __get_users_filter_by(session, handle=user_schema.handle)
        if users_db == []:
            return None
        else:
            user_db = users_db[0]
        user_schema = UserSchema.model_validate(user_db)
    return user_schema


def update_user(id: int, **kwargs) -> UserSchema | None:
    user_schema = _get_user_db_with_kwargs(id=id)
    if user_schema is None:
        return None

    if _check_patch_with_kwargs(user_schema, **kwargs):
        user_schema_update = _update_user_with_kwargs(user_schema, **kwargs)

    return UserSchema.model_validate(_get_user_db_with_kwargs(id=id))


def _check_patch_with_kwargs(user_schema: UserSchema, **kwargs) -> bool:
    try:
        user_copy_schema = copy.deepcopy(user_schema)
        for key, value in kwargs.items():
            setattr(user_copy_schema, key, value)

        check_user_schema = UserSchema(**user_copy_schema.model_dump())
    except:
        return False
    return True


def __update_user_with_id(session: Session, user_id: int, **kwargs) -> UserOrm | None:
    user_db = session.query(UserOrm).filter_by(id=user_id).one_or_none()
    if user_db is None:
        return None
    for key, value in kwargs.items():
        if key != "id":
            setattr(user_db, key, value)
    session.add(user_db)
    session.commit()
    return user_db


def _update_user_with_kwargs(user_schema: UserSchema, **kwargs) -> UserSchema:
    with db.SessionLocal() as session:
        user_db = __update_user_with_id(
            session, user_id=user_schema.id, **kwargs)
        user_schema = (
            UserSchema.model_validate(user_db) if user_db is not None else None
        )
    return user_schema


def __delete_user_with_id(session: Session, user_id: int) -> int:
    return session.query(UserOrm).filter_by(id=user_id).delete()


def _delete_user(user_id: int) -> int:
    with db.SessionLocal() as session:
        cnt = __delete_user_with_id(session, user_id)
        session.commit()
        return cnt


def delete_user(user_id: int) -> int:
    return _delete_user(user_id)
