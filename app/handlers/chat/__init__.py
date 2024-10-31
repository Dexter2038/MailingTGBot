from aiogram import Router

from .chat import router as chat_router


def get_chat_router() -> Router:
    router = Router()

    router.include_router(chat_router)

    return router
