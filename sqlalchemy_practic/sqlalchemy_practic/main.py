import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from sqlalchemy_practic.models import Group, User, UserGroup
from sqlalchemy_practic.schemas import BaseUser, BaseUserPLUS, GroupName

from .settings import async_session_maker

app = FastAPI()


@app.post("/user/{user_id}", response_model=BaseUser)
async def get_user(user_id: int):
    try:
        async with async_session_maker() as session:
            query = (
                select(User).options(
                    # selectinload(User.group),
                    # .options(joinedload(UserGroup.group)), # .options(joinedload(UserGroup.group)
                    # .options(joinedload(Group.user)),
                    # selectinload(User.addresses),
                    # selectinload(User.profile),
                )
            ).where(User.id == user_id)
            result = await session.execute(query)
            res = result.scalars().one()
            return res
    except Exception as err:
        logging.warning(str(err))
        raise HTTPException(status_code=401, detail=err)


@app.post("/users", response_model=list[BaseUser])
async def get_users():
    try:
        async with async_session_maker() as session:
            query = select(User)
            result = await session.execute(query)
            result.unique()  # этот подход помог избежать трех selectinload,
            # походу оно как раз помогает избежать дублирование запросы из за того как подтягиваются
            # модели, там могут быть дубликат, типикал как в сырых запросах.
            # при том скипается вот такая ошибка:
            """
                raise TypeError(f'Object of type {o.__class__.__name__} '
                TypeError: Object of type InvalidRequestError is not JSON serializable
            """
            res = result.scalars().all()
            return res
    except Exception as err:
        logging.warning(str(err))
        raise HTTPException(status_code=401, detail=err)


@app.post("/users_1", response_model=list[BaseUser])
async def get_users1():
    try:
        async with async_session_maker() as session:
            query = select(User).options(
                selectinload(User.group),  # походу не нужно из за unique()
                selectinload(User.addresses),  # походу не нужно из за unique()
                selectinload(User.profile),  # походу не нужно из за unique()
            )
            result = await session.execute(query)
            result = result.unique()
            res = [u[0].__dict__ for u in result]
            return res
    except Exception as err:
        logging.warning(str(err))
        raise HTTPException(status_code=401, detail=err)


@app.post("/users_plus_group_name", response_model=list[BaseUserPLUS])
async def get_users_plus_dop():
    try:
        async with async_session_maker() as session:
            query = (
                select(User)
                .join(User.group)
                .join(Group)
                .options(
                    selectinload(User.addresses),
                    selectinload(User.profile),
                )
            )
            result = await session.execute(query)
            result = result.unique()
            users_data = []
            for user in result.scalars():
                user_dict = user.__dict__
                user_dict["group"] = [
                    {"name": group.group.name} for group in user.group
                ]
                users_data.append(user_dict)
            return users_data
    except Exception as err:
        logging.warning(str(err))
        raise HTTPException(status_code=401, detail=err)


@app.post("/group_for_users/{user_id}", response_model=list[GroupName])
async def group_for_users(user_id: int):
    try:
        async with async_session_maker() as session:
            query = (
                select(Group)
                .join(UserGroup)
                .join(User)
                .where(User.id == user_id)
                # or
                # select(Group)
                # .join(UserGroup)
                # .join(User)
                # .where(UserGroup.user.has(User.id == user_id))
            )
            result = await session.execute(query)
            res = result.scalars().all()
            return res
    except Exception as err:
        logging.warning(str(err))
        raise HTTPException(status_code=401, detail=err)
