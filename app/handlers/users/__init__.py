from aiogram import Router

from app.filters.user import IsUserCallback, IsUserMessage

from .callbacks import router as callbacks_router
from .messages import router as messages_router


def get_user_router() -> Router:
    """
    Функция, которая создает и возвращает роутер для обработки сообщений и callback-запросов от пользователей.

    :return: Router - Конфигурированный роутер для пользователя.

    Внутренний процесс:
    1. Создаем экземпляр класса Router с именем "user".
    2. Включаем в роутер маршрутизаторы для обработки callback-запросов и сообщений.
    3. Устанавливаем фильтр для сообщений, чтобы обрабатывать только те, которые проходят проверку IsUserMessage.
    4. Устанавливаем фильтр для callback-запросов, чтобы обрабатывать только те, которые проходят проверку IsUserCallback.
    5. Возвращаем сконфигурированный роутер.
    """
    router = Router(name="user")
    router.include_router(callbacks_router)
    router.include_router(messages_router)
    router.message.filter(IsUserMessage())
    router.callback_query.filter(IsUserCallback())
    return router
