from aiogram.fsm.state import State, StatesGroup


class Start(StatesGroup):
    reg = State()
