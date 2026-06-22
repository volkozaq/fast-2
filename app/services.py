# app/services.py
from fastapi import  HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError

import models, schemas

async def add_item(
        session: AsyncSession,
        orm_model: type(models.Advert),
        item_data: schemas.CreateAdRequest
) -> models.Advert:

    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    try:
        await session.commit()
        await session.refresh(new_item)
        return new_item
    except IntegrityError as e:
        await session.rollback()
        raise e

async def get_item(
        session: AsyncSession,
        orm_model: type[models.Advert],
        item_id: int
) -> models.Advert:

    q = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(q)
    item = result.unique().scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} with id {item_id} not found"
        )
    return item

async def update_item(
        session: AsyncSession,
        orm_model: type[models.Advert],
        item_id: int,
        update_data: schemas.UpdateAdRequest
) -> models.Advert:

    item = await get_item(session, orm_model, item_id)
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item

async def delete_item(
    session: AsyncSession,
    orm_model: type[models.Advert],
    item_id: int
) -> None:

    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()

async def search_item(
        session: AsyncSession,
        orm_model: type[models.Advert],
        search_data: schemas.SearchAdRequest
) -> models.Advert:
    print(search_data)
    q = select(orm_model).where(or_(orm_model.title.contains(search_data),
                                    orm_model.description.contains(search_data)))
    result = await session.execute(q)
    item = result.unique().scalars().all()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} containing query string '{search_data}' is not found"
        )
    return item

async def get_user_serv(
        session: AsyncSession,
        orm_model: type[models.User],
        item_id: int
) -> models.User:

    q = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(q)
    item = result.unique().scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} with id {item_id} not found"
        )
    return item

async def update_user_serv(
        session: AsyncSession,
        orm_model: type[models.User],
        item_id: int,
        update_data: schemas.UpdateUserRequest
) -> models.User:

    item = await get_user_serv(session, orm_model, item_id)
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item

async def delete_user_serv(
    session: AsyncSession,
    orm_model: type[models.User],
    item_id: int
) -> None:

    item = await get_user_serv(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()