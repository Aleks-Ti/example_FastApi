import asyncio
import os
import sys

from sqlalchemy import text

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from sqlalchemy_practic.settings import async_session_maker


async def load_test_users() -> None:
    async with async_session_maker() as session:
        query = text(
            """
            INSERT INTO public.user (
                name,
                fullname
            )
            VALUES (
                :name,
                :fullname
            )
        """
        )
        values = [
            {
                "name": "admin",
                "fullname": "adminov",
            },
            {
                "name": "admin1",
                "fullname": "adminov1",
            },
        ]
        print("Run script. Loads Users")
        for value in values:
            await session.execute(query, value)
            await session.commit()

    print("Test user loaded!")


if __name__ == "__main__":
    asyncio.run(load_test_users())


"""
insert into public."group" (id, name) values(1, 'AUD');
insert into public."group" (id, name) values(2, 'FHG');
insert into public."group" (id, name) values(3, 'ATG');
insert into public."group" (id, name) values(3, 'DAB');

insert into public.user_group (group_id, user_id) values(1, 1);
insert into public.user_group (group_id, user_id) values(1, 2);
insert into public.user_group (group_id, user_id) values(2, 1);
insert into public.user_group (group_id, user_id) values(3, 2);
insert into public.user_group (group_id, user_id) values(4, 1);
insert into public.user_group (group_id, user_id) values(4, 2);

insert into public.profile (date, zodiac, user_id) values('2022.01.01', 'snake', 1);
insert into public.profile (date, zodiac, user_id) values('2022.01.01', 'snake', 2);
"""
