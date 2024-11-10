from aiogram import Router
from .root import get_root_router
from .users import get_user_router
from .moders import get_moder_router
from .chat import get_chat_router
from .subadmins import get_subadmin_router


def get_router() -> Router:
    """
    Функция, которая создает и возвращает основной роутер, включающий в себя
    маршрутизаторы администраторов, пользователей, модераторов и чатов.

    :return: Router - Конфигурированный основной роутер.

    Внутренний процесс:
    1. Создаем экземпляр роутера.
    2. Включаем в роутер маршрутизатор главного админа с помощью функции get_root_router().
    3. Включаем в роутер маршрутизатор субадминистратора с помощью функции get_subadmin_router().
    4. Включаем в роутер маршрутизатор пользователей с помощью функции get_user_router().
    5. Включаем в роутер маршрутизатор модераторов с помощью функции get_moder_router().
    6. Включаем в роутер маршрутизатор чатов с помощью функции get_chat_router().
    7. Возвращаем сконфигурированный роутер.
    """
    router = Router()
    router.include_router(get_chat_router())
    router.include_router(get_root_router())
    router.include_router(get_subadmin_router())
    router.include_router(get_moder_router())
    router.include_router(get_user_router())
    return router
