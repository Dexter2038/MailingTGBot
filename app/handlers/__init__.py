from aiogram import Router
from .admins import get_admin_router
from .users import get_user_router
from .moders import get_moder_router
from .chat import get_chat_router


def get_router() -> Router:
    """
    Функция, которая создает и возвращает основной роутер, включающий в себя
    маршрутизаторы администраторов, пользователей, модераторов и чатов.

    :return: Router - Конфигурированный основной роутер.

    Внутренний процесс:
    1. Создаем экземпляр класса Router.
    2. Включаем в роутер маршрутизатор администраторов с помощью функции get_admin_router().
    3. Включаем в роутер маршрутизатор пользователей с помощью функции get_user_router().
    4. Включаем в роутер маршрутизатор модераторов с помощью функции get_moder_router().
    5. Включаем в роутер маршрутизатор чатов с помощью функции get_chat_router().
    6. Возвращаем сконфигурированный роутер.
    """
    router = Router()
    router.include_router(get_chat_router())
    router.include_router(get_admin_router())
    router.include_router(get_moder_router())
    router.include_router(get_user_router())
    return router
