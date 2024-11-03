from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.actions import modify_email
from app.states.user import User
from app.keyboards.user import get_back_kb
from app.utils.ask import ask_question
from app.utils.email import validate_email


router = Router(name="user_states")




@router.message(User.change_email)
async def change_email_state(message: Message, state: FSMContext) -> None:
    if not validate_email(message.text):
        await message.answer(
            "Некорректная почта. Попробуйте еще раз.", reply_markup=get_back_kb()
        )
        await state.set_state(User.change_email)
        return

    modify_email(message.from_user.id, message.text)
    await message.answer("Ваша почта изменена", reply_markup=get_back_kb())
    await state.clear()


@router.message(User.ask_question)
async def ask_question_state(message: Message, state: FSMContext, bot: Bot) -> None:
    result = await ask_question(
        message.from_user.id,
        message.message_id,
        message.from_user.username,
        bot,
        message.text,
    )

    if result:
        await message.answer("Ваш вопрос отправлен", reply_markup=get_back_kb())
    else:
        await message.answer(
            "Ваш вопрос не отправлен. Попробуйте позже", reply_markup=get_back_kb()
        )
    await state.clear()
