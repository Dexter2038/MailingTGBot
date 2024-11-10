from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    ask_question = State()
