from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import is_subadmin


class IsSubAdminMessage(Filter):
    """
    Фильтр, который проверяет, является ли автор сообщения субадминистратором.
    """

    async def __call__(self, message: Message) -> bool:
        """
        :param message: Объект Message, представляющий сообщение.
        :return: True, если автор сообщения является субадминистратором, False в противном случае.
        """
        if message.chat.type != "private":
            return False
        return await is_subadmin(message.chat.id)


class IsSubAdminCallback(Filter):
    """
    Фильтр, который проверяет, является ли автор callback-запроса субадминистратором.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        :param callback: Объект CallbackQuery, представляющий callback-запрос.
        :return: True, если автор callback-запроса является субадминистратором, False в противном случае.
        """
        if callback.message.chat.type != "private":
            return False
        return await is_subadmin(callback.from_user.id)
