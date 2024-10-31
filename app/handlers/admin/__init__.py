from aiogram import Router

from .admin import router as admin_router


def get_admin_router() -> Router:
    router = Router()

    router.include_router(admin_router)

    return router
