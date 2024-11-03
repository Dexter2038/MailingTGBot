from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import get_moders


class IsModerMessage(Filter):

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != "private":
            return False
        return message.chat.id in [int(moder[0]) for moder in await get_moders()]


class IsModerCallback(Filter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.message.chat.type != "private":
            return False
        return callback.message.chat.id in [
            int(moder[0]) for moder in await get_moders()
        ]
