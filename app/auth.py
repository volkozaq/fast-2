# app/auth.py
import bcrypt
import uuid
import datetime
from fastapi import Header, HTTPException, Depends
from requests import session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Token, User, Advert, Right, Role, user_role_relation, role_right_relation
from dependencies import get_db_session
from config import config
from sqlalchemy.sql import func


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

async def check_token(
        session: AsyncSession = Depends(get_db_session),
        token: uuid.UUID = Header(..., alias="x-token")
)-> Token:
    expire_threshold = func.now() - datetime.timedelta(seconds=config.TOKEN_TIME)
    query = select(Token).where(
        Token.token == token,
        Token.creation_time >= expire_threshold
    )
    token_obj = await session.scalar(query)

    if token_obj is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return token_obj

async def check_object_access(
        user: User,
        orm_object,
        session: AsyncSession = Depends(get_db_session),
        need_read: bool = False,
        need_write: bool = False
) -> bool:

    model_class = orm_object if isinstance(orm_object, type) else orm_object.__class__
    model_name = model_class.__name__

    where_args = [
        User.id == user.id,
        Right.model == model_name
    ]

    if need_read:
        where_args.append(Right.read == True)
    if need_write:
        where_args.append(Right.write == True)
    if not isinstance(orm_object, type) and (hasattr(orm_object, 'id') or hasattr(orm_object, 'author_id')):
        if hasattr(orm_object, 'author_id'):
            if orm_object.author_id != user.id:
                where_args.append(Right.only_own == False)
        elif hasattr(orm_object, 'id'):
            if orm_object.id != user.id:
                where_args.append(Right.only_own == False)




    query = (
        select(func.count())
        .select_from(User)
        .join(user_role_relation, User.id == user_role_relation.c.user_id)
        .join(Role, user_role_relation.c.role_id == Role.id)
        .join(role_right_relation, Role.id == role_right_relation.c.role_id)
        .join(Right, role_right_relation.c.right_id == Right.id)
        .where(*where_args)
    )

    result = await session.execute(query)
    count = result.scalar()

    return count>0


