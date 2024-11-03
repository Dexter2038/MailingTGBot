from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


class IsUserMessage(Filter):
    """
    Фильтр, который проверяет, является ли сообщение private-сообщением.
    """

    async def __call__(self, message: Message) -> bool:
        """
        :param message: Объект Message, представляющий сообщение.
        :return: True, если сообщение является private-сообщением, False в противном случае.
        """
        return message.chat.type == "private"


class IsUserCallback(Filter):
    """
    Фильтр, который проверяет, является ли callback-запрос private-callback-запросом.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        :param callback: Объект CallbackQuery, представляющий callback-запрос.
        :return: True, если callback-запрос является private-callback-запросом, False в противном случае.
        """
        return callback.message.chat.type == "private"
