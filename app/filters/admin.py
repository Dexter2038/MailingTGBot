import os
from aiogram.filters import Filter
from aiogram.types import Message


class IsAdmin(Filter):

    async def __call__(self, message: Message) -> bool:
        with open("admin.txt", "r") as f:
            admin: str = f.read()
            if admin == "":
                return False
        return message.from_user.id == int(admin)
