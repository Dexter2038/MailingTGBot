from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    change_email = State()
    ask_question = State()
    register_email = State()
