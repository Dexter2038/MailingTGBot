from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import get_admin


class IsAdminMessage(Filter):
    """
    Фильтр, который проверяет, является ли автор сообщения субадминистратором.
    """

    async def __call__(self, message: Message) -> bool:
        """
        :param message: Объект Message, представляющий сообщение.
        :return: True, если автор сообщения является администратором, False в противном случае.
        """
        if message.chat.type != "private":
            return False
        return (await get_admin()) == message.chat.id


class IsAdminCallback(Filter):
    """
    Фильтр, который проверяет, является ли автор callback-queries субадминистратором.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        :param callback: Объект CallbackQuery, представляющий callback-запрос.
        :return: True, если автор callback-запроса является администратором, False в противном случае.
        """
        if callback.message.chat.type != "private":
            return False
        return (await get_admin()) == callback.from_user.id
