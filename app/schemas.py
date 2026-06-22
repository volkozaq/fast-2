# app/schemas.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List




# Advert schemas
# class CreateAdRequest(BaseModel):
#     title: str
#     description: str
#     price: int

class CreateAdRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    author_id: int

class CreateAdResponse(BaseModel):
    id: int

class GetAdResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: int
    author_id: int
    created_at: datetime | None = None

class UpdateAdRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author_id: int | None = None

class UpdateAdResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: int
    author_id: int
    created_at: datetime | None = None

class OkResponse(BaseModel):
    status: str = 'ok'

class SearchAdRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author_id: int | None = None

class SearchAdResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: int
    author_id: int
    created_at: datetime | None = None


# Login schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    id: int
    token: UUID
    user_id: int

    class Config():
        from_attributes = True

# User schemas
class CreateUserRequest(BaseModel):
    username: str
    password: str

class IdResponse(BaseModel):
    id: int

class GetUserResponse(BaseModel):
    id: int
    username: str
    password: str

class UpdateUserRequest(BaseModel):
    username: str | None = None
    password: str | None = None

class TokenResponse(BaseModel):
    user_id: int
    id: int
    token: UUID
    creation_time: datetime

    class Config():
        from_attributes = True

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config():
        from_attributes = True

class UpdateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    tokens: List[TokenResponse]
    roles: List[RoleResponse]

# class




