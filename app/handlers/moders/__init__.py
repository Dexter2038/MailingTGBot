from aiogram import Router

from app.filters.moder import IsModerCallback, IsModerMessage

from .callbacks import router as callbacks_router
from .messages import router as messages_router


def get_moder_router() -> Router:
    router = Router(name="moders")
    router.include_router(callbacks_router)
    router.include_router(messages_router)
    router.message.filter(IsModerMessage())
    router.callback_query.filter(IsModerCallback())
    return router
