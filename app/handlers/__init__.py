from aiogram import Router
from .admins import get_admin_router
from .users import get_user_router
from .moders import get_moder_router
from .chat import get_chat_router


def get_router() -> Router:
    router = Router()
    router.include_router(get_admin_router())
    router.include_router(get_user_router())
    router.include_router(get_moder_router())
    router.include_router(get_chat_router())
    return router
