from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery
from app.filters.moder import IsModerCallback
from app.keyboards.moder import get_chat_kb, get_moder_kb
from app.utils.ranks import get_chat_link


router = Router(name="moder_callbacks")




@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Пока что у тебя есть возможность только отвечать на вопросы в чате",
        reply_markup=get_moder_kb(),
    )


@router.callback_query(F.data == "show_chat")
async def show_chat_callback(callback: CallbackQuery, bot: Bot) -> None:
    chat_link = await get_chat_link(bot)

    if not chat_link:
        await callback.message.answer(
            "Чат ещё не инициализирован админом", get_chat_kb()
        )

    await callback.message.answer(f"Ссылка на чат: {chat_link}", get_chat_kb(chat_link))
