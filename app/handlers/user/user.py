from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.actions import is_user_registered
from app.states.start import Start

router = Router(name=__name__)


@router.message()
async def echo(message: Message, state: FSMContext) -> None:
    if is_user_registered(id=message.from_user.id):
        await message.answer(text="Добро пожаловать! Чтобы узнать команды введите /help")
        return
    
    await state.set_state(state=Start.reg)
    await message.answer(text="Для регистрации введите свой email")