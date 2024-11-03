from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import get_moders


class IsUserMessage(Filter):

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"


class IsUserCallback(Filter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.message.chat.type == "private"
