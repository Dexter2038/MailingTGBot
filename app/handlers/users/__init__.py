from aiogram import Router

from app.filters.user import IsUserCallback, IsUserMessage

from .callbacks import router as callbacks_router
from .messages import router as messages_router


def get_user_router() -> Router:
    router = Router(name="user")
    router.include_router(callbacks_router)
    router.include_router(messages_router)
    router.message.filter(IsUserMessage())
    router.callback_query.filter(IsUserCallback())
    return router
