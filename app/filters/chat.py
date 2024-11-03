from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import get_chat_id


class IsChatMessage(Filter):

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != "group":
            return False
        return (await get_chat_id()) == message.chat.id


class IsChatCallback(Filter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.message.chat.type != "group":
            return False
        return (await get_chat_id()) == callback.message.chat.id
