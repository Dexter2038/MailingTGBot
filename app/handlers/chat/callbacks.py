from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery

from app.filters.chat import IsChatCallback
from app.utils.ranks import is_admin, is_moder

router = Router(name="chat_callbacks")


router.callback_query.filter(IsChatCallback())


@router.callback_query(F.data == "decline_question")
async def decline_message(callback: CallbackQuery, bot: Bot):
    try:
        data = callback.message.text.split("]", maxsplit=1)[0]
        data = data.split("[", maxsplit=1)[1]
        chat_id, msg_id = data.split(", ")
        if not is_moder(callback.from_user.id) and not is_admin(callback.from_user.id):
            return  # ничего не делать

        answer_text = "Ваш вопрос отклонён!"

        await bot.send_message(chat_id, answer_text, reply_to_message_id=msg_id)

        await callback.message.delete()

    except Exception:
        return  # ничего не делать
