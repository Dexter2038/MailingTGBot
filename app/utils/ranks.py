from typing import List, Tuple

import aiofiles
from aiogram import Bot


async def get_moders() -> List[Tuple[str, str]]:
    try:
        async with aiofiles.open("app/data/moders.txt", mode="r") as f:
            lines = await f.readlines()
            return list(map(lambda line: line.split(" "), lines))
    except Exception:
        return []


async def get_moder(id: int | str) -> str:
    async with aiofiles.open("app/data/moders.txt", mode="r") as f:
        lines = await f.readlines()
        moders = list(map(lambda line: line.split(" "), lines))
        moder = next(filter(lambda moder: moder[0] == str(id), moders), None)
        return moder


async def reset_chat() -> bool:
    try:
        async with aiofiles.open("app/data/chat.txt", mode="w") as f:
            await f.write("")
        return True
    except Exception:
        return False


async def get_chat_id() -> int:
    async with aiofiles.open("app/data/chat.txt", mode="r") as f:
        chat_id = await f.read()
        return int(chat_id) if chat_id else 0


async def set_chat_id(chat_id: int) -> None:
    async with aiofiles.open("app/data/chat.txt", mode="r") as f:
        f.write(str(chat_id))


async def is_moder(user_id: int) -> bool:
    moders = await get_moders()
    return user_id in [int(moder[0]) for moder in moders]


async def is_admin(user_id: int) -> bool:
    admin = await get_admin()
    return user_id == admin


async def get_chat_link(bot: Bot) -> str:
    chat_id = await get_chat_id()

    if not chat_id:
        return ""

    chat_link = await bot.export_chat_invite_link(chat_id)
    return chat_link


async def add_moder(id: str, username: str) -> bool:
    async with aiofiles.open("app/data/moders.txt", mode="a+") as f:
        lines = await f.readlines()
        moders = list(map(lambda line: line.split(" "), lines))
        if [id, username] in moders:
            return False
        else:
            await f.write(f"{id} {username}\n")
            return True


async def del_moder(id_or_username: str) -> bool:
    async with aiofiles.open("app/data/moders.txt", mode="w+") as f:
        lines = await f.readlines()
        moders = list(map(lambda line: line.split(" "), lines))
        if [id_or_username] in moders:
            return False
        else:
            await f.write(
                "\n".join([moder for moder in moders if id_or_username not in moder])
            )
            return True


async def get_admin() -> int:
    async with aiofiles.open("app/data/admin.txt", mode="r") as f:
        admin = await f.read()
        return int(admin) if admin else 0
