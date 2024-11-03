from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    add_moderator = State()
    del_moderator = State()
    make_mailing = State()
    add_confirm = State()
    del_confirm = State()
    show_confirm_users = State()
    edit_about_quiz = State()
    edit_faq = State()
    edit_news = State()
    edit_quiz = State()
    add_news = State()
    add_quiz = State()
