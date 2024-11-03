from aiogram import Router

from .callbacks import router as callbacks_router
from .messages import router as messages_router


def get_chat_router() -> Router:
    router = Router(name="chat")
    router.include_router(callbacks_router)
    router.include_router(messages_router)
    return router
