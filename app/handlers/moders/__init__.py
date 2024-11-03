from aiogram import Router

from app.filters.moder import IsModerCallback, IsModerMessage

from .callbacks import router as callbacks_router
from .messages import router as messages_router


def get_moder_router() -> Router:
    """
    Функция, которая возвращает роутер для обработки сообщений и callback-запросов
    от модераторов.

    :return: Router

    Внутренний процесс:
    1. Создаем экземпляр класса Router.
    2. Добавляем в роутер callback-запросы из модуля callbacks_router.
    3. Добавляем в роутер сообщения из модуля messages_router.
    4. Устанавливаем фильтры для callback-запросов и сообщений.
    """
    router = Router(name="moders")
    router.include_router(callbacks_router)
    router.include_router(messages_router)
    router.message.filter(IsModerMessage())
    router.callback_query.filter(IsModerCallback())
    return router
