from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import get_admin


class IsAdminMessage(Filter):

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != "private":
            return False
        return (await get_admin()) == message.chat.id


class IsAdminCallback(Filter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.message.chat.type != "private":
            return False
        return (await get_admin()) == callback.message.chat.id
