from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from app.utils.ranks import get_chat_id


class IsChatMessage(Filter):
    """
    Фильтр, который проверяет, является ли сообщение сообщением из чата.
    """

    async def __call__(self, message: Message) -> bool:
        """
        :param message: Объект Message, представляющий сообщение.
        :return: True, если сообщение является сообщением из чата, False в противном случае.
        """
        if message.chat.type != "group" and message.chat.type != "supergroup":
            return False
        return (await get_chat_id()) == message.chat.id


class IsChatCallback(Filter):
    """
    Фильтр, который проверяет, является ли callback-запрос callback-запросом из чата.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        :param callback: Объект CallbackQuery, представляющий callback-запрос.
        :return: True, если callback-запрос является callback-запросом из чата, False в противном случае.
        """
        if (
            callback.message.chat.type != "group"
            and callback.message.chat.type != "supergroup"
        ):
            return False
        return (await get_chat_id()) == callback.message.chat.id
