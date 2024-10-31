import os
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


class IsChatCallback(Filter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        with open("chat.txt", "r") as f:
            chat: str = f.read()
        return callback.message.chat.id == int(chat)


class IsChatMessage(Filter):

    async def __call__(self, message: Message) -> bool:
        with open("chat.txt", "r") as f:
            chat: str = f.read()
        return message.chat.id == int(chat)
