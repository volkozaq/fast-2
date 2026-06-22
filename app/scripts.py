# app/scripts.py
import asyncio
from sqlalchemy import select
from models import User, Role, Right
from auth import hash_password
from database import AsyncSessionLocal

async def create_initial_roles(session):

    right_read_own_advert = Right(
        read=True, write=False, only_own=True, model="Advert"
    )
    right_read_write_own_advert = Right(
        read=True, write=True, only_own=True, model="Advert"
    )
    right_read_any_advert = Right(
        read=True, write=False, only_own=False, model="Advert"
    )
    right_full_advert = Right(
        read=True, write=True, only_own=False, model="Advert"
    )

    right_read_own_user = Right(
        read=True, write=False, only_own=True, model="User"
    )
    right_read_write_own_user = Right(
        read=True, write=True, only_own=True, model="User"
    )
    right_read_any_user = Right(
        read=True, write=False, only_own=False, model="User"
    )
    right_full_user = Right(
        read=True, write=True, only_own=False, model="User"
    )

    session.add_all([right_read_own_advert, right_read_write_own_advert, right_read_any_advert, right_full_advert,
                     right_read_write_own_user, right_read_own_user, right_read_any_user, right_full_user])
    await session.flush()

    role_user = Role(name="user")
    role_user.rights = [right_read_write_own_user, right_read_write_own_advert, right_read_any_user,
                        right_read_any_advert, right_read_own_user, right_read_own_advert]

    role_admin = Role(name="admin")
    role_admin.rights = [right_full_user, right_full_advert]

    session.add_all([role_user, role_admin])
    await session.flush()
    return role_user, role_admin

async def create_test_user(session, role_user):

    hashed_pw = hash_password("4567")
    test_user = User(username = "testuser1", password=hashed_pw, roles=[role_user])
    print(test_user)
    session.add(test_user)

    print(f'Test user created with id: {test_user.id}')
    print(test_user)
    print(test_user.roles)
    for role in test_user.roles:
        print(role.name)

    hashed_pw = hash_password("1234")
    test_user = User(username = "testuser2", password=hashed_pw, roles=[role_user])
    print(test_user)
    session.add(test_user)

    print(f'Test user created with id: {test_user.id}')
    print(test_user)
    print(test_user.roles)
    for role in test_user.roles:
        print(role.name)

    hashed_pw = hash_password("5463")
    test_user = User(username = "testuser3", password=hashed_pw, roles=[role_user])
    print(test_user)
    session.add(test_user)
    await session.commit()

    print(f'Test user created with id: {test_user.id}')
    print(test_user)
    print(test_user.roles)
    for role in test_user.roles:
        print(role.name)

async def create_test_admin(session, role_admin):

    hashed_pw = hash_password("admin")
    test_admin = User(username = "admin", password=hashed_pw, roles=[role_admin])
    print(test_admin)
    session.add(test_admin)
    await session.commit()
    print(f'Test admin created with id: {test_admin.id}')
    for role in test_admin.roles:
        print(role.name)

async def main():
    async with AsyncSessionLocal() as session:
        stmt = select(Role)
        result = await session.execute(stmt)
        existing_roles = result.scalars().unique().all()



        if not existing_roles:
            print("--- Creating initial roles ---")
            role_user, role_admin = await create_initial_roles(session)

            await create_test_user(session, role_user)
            await create_test_admin(session, role_admin)
            await session.commit()
            print("--- Initial data created ---")
        else:
            print("Roles already exists")
            print(existing_roles)

if __name__ == "__main__":
    asyncio.run(main())