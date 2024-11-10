from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import is_subadmin


class IsSubAdminMessage(Filter):
    """
    Фильтр, который проверяет, является ли автор сообщения модератором.
    """

    async def __call__(self, message: Message) -> bool:
        """
        :param message: Объект Message, представляющий сообщение.
        :return: True, если автор сообщения является модератором, False в противном случае.
        """
        if message.chat.type != "private":
            return False
        return await is_subadmin(message.chat.id)


class IsSubAdminCallback(Filter):
    """
    Фильтр, который проверяет, является ли автор callback-запроса модератором.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        :param callback: Объект CallbackQuery, представляющий callback-запрос.
        :return: True, если автор callback-запроса является модератором, False в противном случае.
        """
        if callback.message.chat.type != "private":
            return False
        return await is_subadmin(callback.from_user.id)
