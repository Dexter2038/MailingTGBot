from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    add_moderator = State()
    add_subadmin = State()
    make_mailing = State()
    add_confirm = State()
    edit_about_quiz = State()
    edit_faq = State()
    edit_news = State()
    edit_quiz = State()
    edit_rules = State()
    add_news = State()
    add_quiz = State()
