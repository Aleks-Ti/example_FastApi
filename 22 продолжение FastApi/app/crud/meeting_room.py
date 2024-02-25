from typing import Optional

# Добавляем импорт функции select.
from sqlalchemy import select

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession
) -> MeetingRoom:
    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)

    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room


# Добавляем новую асинхронную функцию.
async def get_room_id_by_name(
        room_name: str,
        session: AsyncSession,
) -> Optional[int]:

    # Получаем объект класса Result.
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    # Извлекаем из него конкретное значение.
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def get_meeting_room_by_id(
        room_id: int,
        session: AsyncSession,
) -> Optional[MeetingRoom]:
    db_room = await session.execute(
        select(MeetingRoom).where(MeetingRoom.id == room_id)
    )
    db_room = db_room.scalar().first()
    # db_room = await session.get(MeetingRoom, room_id)
    return db_room


async def read_all_rooms_from_db(
        session: AsyncSession,
) -> list[MeetingRoom]:
    # Получаем объект класса Result.
    db_room_id: AsyncSession = await session.execute(
        select(MeetingRoom)
    )
    # Извлекаем из него конкретное значение.
    db_room_id = db_room_id.scalars().all()
    return db_room_id


async def update_meeting_room(
        # Объект из БД для обновления.
        db_room: MeetingRoom,
        # Объект из запроса.
        room_in: MeetingRoomUpdate,
        session: AsyncSession,
) -> MeetingRoom:
    # Представляем объект из БД в виде словаря.
    obj_data = jsonable_encoder(db_room)
    # Конвертируем объект с данными из запроса в словарь,
    # исключаем неустановленные пользователем поля.
    update_data = room_in.dict(exclude_unset=True)

    # Перебираем все ключи словаря, сформированного из БД-объекта.
    for field in obj_data:
        # Если конкретное поле есть в словаре с данными из запроса, то...
        if field in update_data:
            # ...устанавливаем объекту БД новое значение атрибута.
            setattr(db_room, field, update_data[field])
    # Добавляем обновленный объект в сессию.
    session.add(db_room)
    # Фиксируем изменения.
    await session.commit()
    # Обновляем объект из БД.
    await session.refresh(db_room)
    return db_room
