from typing import List
from aiogram.filters import Filter
from aiogram.types import Message


class IsModer(Filter):

    async def __call__(self, message: Message) -> bool:
        with open("moders.txt", "r") as f:
            moders: str = f.read()
            res: List[str] = [sublist[0] for sublist in moders]
        return message.chat.id in res
