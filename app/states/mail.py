from aiogram.fsm.state import State, StatesGroup


class Mail(StatesGroup):
    change = State()
