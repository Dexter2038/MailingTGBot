from aiogram import Router

from .user import get_user_router
from .admin import get_admin_router
from .chat import get_chat_router
from .moder import get_moder_router


def get_router() -> Router:
    router = Router()

    router.include_router(get_chat_router())
    router.include_router(get_admin_router())
    router.include_router(get_moder_router())
    router.include_router(get_user_router())

    return router
