# app/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Uuid, Boolean, Table
from sqlalchemy.orm import mapped_column, MappedColumn, Mapped, relationship
from database import Base
from sqlalchemy.sql import func
import uuid
import datetime
from typing import Literal, List

ModelName = ["User", "Advert", "Role", "Right"]

user_role_relation = Table(
    "user_role_relation",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True)
)

role_right_relation = Table(
    "role_right_relation",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("right_id", ForeignKey("right.id"), primary_key=True)
)

class Right(Base):
    __tablename__ = "right"

    id: Mapped[int] = mapped_column(primary_key=True)
    write: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    only_own: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    model: Mapped[ModelName] = mapped_column(String(50), nullable=False)

class Role(Base):

    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    rights: Mapped[List[Right]] = relationship(
        secondary=role_right_relation,
        lazy="joined"
    )


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(70), nullable=False)

    tokens: Mapped[List['Token']] = relationship(
        "Token", back_populates="user", cascade="all, delete-orphan", lazy="joined"
    )

    adverts: Mapped[List['Advert']] = relationship(
        "Advert", back_populates="author", cascade="all, delete-orphan", lazy="joined"
    )

    roles: Mapped[List[Role]] = relationship(
        secondary=user_role_relation,
        lazy="joined"
    )
    @property
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "tokens": self.tokens,
            "roles": self.roles,
            "adverts": self.adverts
        }

class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        server_default=func.gen_random_uuid(),
        unique=True,
        nullable=False
    )
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(User, back_populates="tokens", lazy="joined")

    @property
    def to_dict(self):
        return {"id": self.id, "token": self.token, "creation_time": self.creation_time.isoformat(), "user_id": self.user_id}

class Advert(Base):
    __tablename__ = "adverts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    author_id: Mapped[[int]] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    author: Mapped[User] =  relationship(User, back_populates="adverts", lazy="joined")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat(),
            "author": self.author
        }


