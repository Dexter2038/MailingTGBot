from aiogram import Router
from .callbacks import router as callbacks_router
from .commands import router as commands_router
from .states import router as states_router
from .user import router as user_router


def get_user_router() -> Router:
    router = Router()

    router.include_router(router=callbacks_router)
    router.include_router(router=states_router)
    router.include_router(router=commands_router)
    router.include_router(router=user_router)

    return router
