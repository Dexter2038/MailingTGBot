from os import environ
from typing import Iterable, List
from pyrogram import Client
from pyrogram.raw.functions.contacts import ResolveUsername
from pyrogram.raw.base.contacts import ResolvedPeer


def init_client():
    try:
        with Client(
            name="bot_distributor",
            api_id=environ["API_ID"],
            api_hash=environ["API_HASH"],
            bot_token=environ["BOT_TOKEN"],
            app_version="1.2.3",
            device_model="PC",
            system_version="Linux",
        ):
            pass
    except KeyError as e:
        print(e)
        print("Невозможно инициализировать MTProto API, не нашли переменную окружения")
        exit(code=403)


async def get_usernames_by_ids(ids: List[int | str]):
    async with Client("bot_distributor") as client:
        users = await client.get_users(ids)
        return (
            [user.username for user in users]
            if isinstance(ids, Iterable)
            else users.username
        )


async def get_id_by_username(username: str) -> str | None:
    async with Client("bot_distributor") as client:
        result: ResolvedPeer = await client.invoke(ResolveUsername(username=username))
        if result.users:
            return result.users[0].id
        return None
