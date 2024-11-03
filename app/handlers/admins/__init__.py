from aiogram import Router

from app.filters.admin import IsAdminMessage, IsAdminCallback

from .callbacks import router as callbacks_router
from .commands import router as commands_router
from .states import router as states_router


def get_admin_router() -> Router:
    router = Router(name="admin")
    router.include_router(states_router)
    router.include_router(callbacks_router)
    router.include_router(commands_router)
    router.message.filter(IsAdminMessage())
    router.callback_query.filter(IsAdminCallback())
    return router
