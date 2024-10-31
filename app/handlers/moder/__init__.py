from aiogram import Router

from .moder import router as moder_router


def get_moder_router() -> Router:
    router = Router()

    router.include_router(moder_router)

    return router
