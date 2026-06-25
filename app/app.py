# app/app.py
from multiprocessing.managers import Token

from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, AsyncSessionLocal
import models, schemas
from models import User, Token, Advert
from lifespan import lifespan
from dependencies import get_db_session
from services import add_item, get_item, update_item, delete_item, search_item, update_user_serv, get_user_serv, delete_user_serv
from auth import check_password, hash_password, check_token, check_object_access
from sqlalchemy import select

app = FastAPI(
    title="Neto FastAPI2",
    description="Advert App on FastApi for Netology, part 2",
    version="0.0.1",
    lifespan=lifespan
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

@app.get("/")
async def root():
    return {"Message": "Hello From FastAPI"}


# Login
@app.post("/login", response_model=schemas.LoginResponse)
async def login(
        login_data: schemas.LoginRequest,
        session: SessionDep
):
    query = select(User).where(User.username == login_data.username)
    user = await session.scalar(query)

    hashed_password = hash_password(login_data.password)

    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not check_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect  password")


    new_token = Token(user=user)
    stmt = select(Token).where(Token.user_id == user.id)
    result = await session.execute(stmt)
    tokens = result.unique().scalars().all()
    if tokens is not None:
        for token in tokens:
            await session.delete(token)
    session.add(new_token)
    await session.commit()
    await session.refresh(new_token)

    return new_token


# User routes
# Unauthorized
@app.post("/user", response_model=schemas.IdResponse, summary="Create new user")
async def create_user(
        user_data: schemas.CreateUserRequest,
        session: SessionDep
):
    hashed_password = hash_password(user_data.password)

    new_user = User(username=user_data.username, password=hashed_password, roles="user")
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"id": new_user.id}

# Unauthorized
@app.get("/user/{user_id}", response_model=schemas.GetUserResponse, summary="Get user by ID")
async def get_user(
        user_id: int,
        session: SessionDep
):
    query = select(User).where(User.id == user_id)
    user = await session.scalar(query)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

#Admin only
@app.get("/user", response_model=list[schemas.GetUserResponse], summary="Get all users")
async def get_all_users(
        session: SessionDep,
        token_obj: Token = Depends(check_token) 
):

    if token_obj.user.roles.name != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    query = select(User)
    result = await session.execute(query)
    users = result.scalars().unique().all()
    return users

@app.patch("/user/{user_id}", response_model=schemas.UpdateUserResponse, summary="Update User")
async def update_user(
        user_id: int,
        session: SessionDep,
        update_data: schemas.UpdateUserRequest,
        token_obj: Token = Depends(check_token)
):
    query = select(User).where(User.id == user_id)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    has_access = await check_object_access(
        user=token_obj.user,
        orm_object=user,
        session=session,
        need_read=True,
        need_write=True
    )

    if not has_access:
        raise HTTPException(status_code=403, detail="Access denied")

    if has_access:
        updated_user = await update_user_serv(session, models.User, user_id, update_data)


        user_dict = schemas.UpdateUserResponse(**updated_user.to_dict)
    return user_dict


@app.delete("/user/{user_id}", response_model=schemas.OkResponse, summary="Delete User")
async def delete_user(
        user_id: int,
        session: SessionDep,
        token_obj: Token = Depends(check_token)
):
    query = select(User).where(User.id == user_id)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    has_access = await check_object_access(
        user=token_obj.user,
        orm_object=user,
        session=session,
        need_read=True,
        need_write=True
    )

    if not has_access:
        raise HTTPException(status_code=403, detail="Access denied")

    if has_access:
        await delete_user_serv(session, models.User, user_id)
    return schemas.OkResponse()



# Advert routes
@app.post("/advertisement", response_model=schemas.CreateAdResponse, summary="Create new Ad")
async def create_ad(
        ad_data: schemas.CreateAdRequest,
        session: SessionDep,
        token_obj: Token = Depends(check_token)
):

    has_access = await check_object_access(
        user=token_obj.user,
        orm_object=models.Advert,
        session=session,
        need_write=True
    )
    if not has_access:
        raise HTTPException(status_code=403, detail="Access denied")
    if has_access:
        new_ad = await add_item(session, models.Advert, ad_data)
        return schemas.CreateAdResponse(id=new_ad.id)

# Unauthorized
@app.get("/advertisement/{ad_id}",  summary="Get Ad by ID")
async def get_ad(
        ad_id: int,
        session: SessionDep
):
    query = select(Advert).where(Advert.id == ad_id)
    advert = await session.scalar(query)

    if advert is None:
        raise HTTPException(status_code=404, detail="Advert not found")

    return advert

@app.patch("/advertisement/{ad_id}", response_model=schemas.UpdateAdResponse, summary="Update Ad")
async def update_ad(
        ad_id: int,
        update_data: schemas.UpdateAdRequest,
        session: SessionDep,
        token_obj: Token = Depends(check_token)
):

    query = select(Advert).where(Advert.id == ad_id)
    advert = await session.scalar(query)
    if advert is None:
        raise HTTPException(status_code=404, detail="Advert not found")

    has_access = await check_object_access(
        user=token_obj.user,
        orm_object=advert,
        session=session,
        need_read=True,
        need_write=True
    )

    if not has_access:
        raise HTTPException(status_code=403, detail="Access denied")

    if has_access:
        updated_ad = await update_item(session, models.Advert, ad_id, update_data)
        ad_dict = schemas.UpdateAdResponse(**updated_ad.dict)

    return ad_dict

@app.delete("/advertisement/{ad_id}", response_model=schemas.OkResponse, summary="Delete Ad")
async def delete_ad(
        ad_id: int,
        session: SessionDep,
        token_obj: Token = Depends(check_token)
):

    query = select(Advert).where(Advert.id == ad_id)
    advert = await session.scalar(query)
    if advert is None:
        raise HTTPException(status_code=404, detail="Advert not found")

    has_access = await check_object_access(
        user=token_obj.user,
        orm_object=advert,
        session=session,
        need_read=True,
        need_write=True
    )

    if not has_access:
        raise HTTPException(status_code=403, detail="Access denied")

    if has_access:
        await delete_item(session, models.Advert, ad_id)
    return schemas.OkResponse()


# Unauthorized
@app.get("/advertisement", summary="Get Ad by fields")
async def get_ad(
        session: SessionDep,
        search_data: str
):
    ads = await search_item(session, models.Advert, search_data)
    result=[]
    for ad in ads:
        result.append(schemas.SearchAdResponse(**ad.dict))
    return result

