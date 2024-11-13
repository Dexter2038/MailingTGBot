from typing import List, Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(text="Новости", callback_data="news_user"),
        InlineKeyboardButton(text="Правила", callback_data="rules_user"),
        InlineKeyboardButton(text="О викторине", callback_data="about_quiz_user"),
        InlineKeyboardButton(text="Частые вопросы", callback_data="faq_user"),
        InlineKeyboardButton(
            text="Предстоящие викторины", callback_data="quizzes_user"
        ),
        InlineKeyboardButton(text="Задать вопрос", callback_data="ask_question_user"),
        InlineKeyboardButton(text="Режим администратора", callback_data="start"),
    )

    kb.adjust(1)

    return kb.as_markup()


def get_back_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="Назад", callback_data="user_mode"))

    return kb.as_markup()


def get_admin_kb(is_subadmin: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Сделать рассылку", callback_data="make_mailing"),
        InlineKeyboardButton(
            text="Рассылки с подтверждением", callback_data="show_confirms"
        ),
        InlineKeyboardButton(
            text="Предстоящие викторины", callback_data="show_quizzes"
        ),
        InlineKeyboardButton(text="О викторине", callback_data="edit_about_quiz"),
        InlineKeyboardButton(text="Частые вопросы", callback_data="edit_faq"),
        InlineKeyboardButton(text="Новости", callback_data="show_all_news"),
        InlineKeyboardButton(text="Правила", callback_data="edit_rules"),
        InlineKeyboardButton(text="Войти в чат вопросов", callback_data="show_chat"),
        InlineKeyboardButton(
            text="Сбросить чат вопросов", callback_data="ask_del_chat"
        ),
        InlineKeyboardButton(text="Модераторы", callback_data="show_moders"),
        InlineKeyboardButton(text="Режим пользователя", callback_data="user_mode"),
    )
    if not is_subadmin:
        builder.add(
            InlineKeyboardButton(
                text="Субадминистраторы", callback_data="show_subadmins"
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def get_moders_kb(active_ids: Optional[List[str]] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if active_ids:
        for moder_id in active_ids:
            builder.row(
                InlineKeyboardButton(
                    text=f"Модератор {moder_id}", callback_data=f"moder_{moder_id}"
                )
            )
    builder.row(
        InlineKeyboardButton(text="Добавить модератора", callback_data="add_moderator")
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_moder_kb(moder_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить модератора", callback_data=f"del_moder_{moder_id}"
        )
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="show_moders"))
    return builder.as_markup()


def get_add_moder_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="start"))
    return builder.as_markup()


def get_del_moder_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить другого модератора", callback_data="show_moders"
        )
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_subadmin_kb(subadmin_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить субадминистратора",
            callback_data=f"del_subadmin_{subadmin_id}",
        )
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="show_subadmins"))
    return builder.as_markup()


def get_subadmins_kb(active_ids: Optional[List[str]] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if active_ids:
        for subadmin_id in active_ids:
            builder.row(
                InlineKeyboardButton(
                    text=f"Субадминистратор {subadmin_id}",
                    callback_data=f"subadmin_{subadmin_id}",
                )
            )
    builder.row(
        InlineKeyboardButton(
            text="Добавить субадминистратора", callback_data="add_subadmin"
        )
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_del_subadmin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить другого субадмина", callback_data="show_subadmins"
        )
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_add_subadmin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="start"))
    return builder.as_markup()


def get_del_chat_kb(confirm: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if confirm:
        builder.row(
            InlineKeyboardButton(text="Да", callback_data="del_chat"),
            InlineKeyboardButton(text="Нет", callback_data="start"),
        )
    else:
        builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_confirms_kb(active_ids: Optional[List[str]] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Добавить рассылку", callback_data="add_confirm")
    )
    if active_ids:
        for confirm_id in active_ids:
            builder.row(
                InlineKeyboardButton(
                    text=f"Рассылка {confirm_id}",
                    callback_data=f"show_confirm_{confirm_id}",
                )
            )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_quizzes_kb(active_ids: Optional[List[str]] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if active_ids:
        for quiz_id in active_ids:
            builder.row(
                InlineKeyboardButton(
                    text=f"Викторина {quiz_id}", callback_data=f"show_quiz_{quiz_id}"
                )
            )
    builder.row(
        InlineKeyboardButton(text="Добавить викторину", callback_data="add_quiz"),
        InlineKeyboardButton(text="Назад", callback_data="start"),
    )
    return builder.as_markup()


def get_news_kb(active_ids: Optional[List[str]] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Добавить новость", callback_data="add_news"))
    if active_ids:
        for news_id in active_ids:
            builder.row(
                InlineKeyboardButton(
                    text=f"Новость {news_id}", callback_data=f"show_one_news_{news_id}"
                )
            )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_add_quiz_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="show_quizzes"))
    return builder.as_markup()


def get_add_news_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="show_news"))
    return builder.as_markup()


def get_edit_quiz_kb(quiz_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отмена", callback_data=f"show_quiz_{quiz_id}")
    )
    return builder.as_markup()


def get_edit_news_kb(news_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отмена", callback_data=f"show_one_news_{news_id}")
    )
    return builder.as_markup()


def get_del_quiz_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад", callback_data="show_quizzes"))
    return builder.as_markup()


def get_del_news_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад", callback_data="show_all_news"))
    return builder.as_markup()


def get_end_confirm_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад", callback_data="show_confirms"))
    return builder.as_markup()


def get_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))

    return builder.as_markup()


def get_chat_kb(chat_link: Optional[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if chat_link:
        builder.row(InlineKeyboardButton(text="Ссылка на чат", url=chat_link))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_mailing_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отмена рассылки", callback_data="start"))
    return builder.as_markup()


def get_confirm_kb(active_id: Optional[str] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if active_id:
        builder.row(
            InlineKeyboardButton(
                text="Удалить рассылку", callback_data=f"end_confirm_{active_id}"
            )
        )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="show_confirms"))
    return builder.as_markup()


def get_add_confirm_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отмена", callback_data="show_confirms"))
    return builder.as_markup()


def get_quiz_kb(id: str | int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Редактировать викторину", callback_data=f"edit_quiz_{id}"
        )
    )
    builder.row(
        InlineKeyboardButton(text="Удалить викторину", callback_data=f"del_quiz_{id}")
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="show_quizzes"))
    return builder.as_markup()


def get_news_one_kb(news_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить новость", callback_data=f"del_news_{news_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Редактировать новость", callback_data=f"edit_news_{news_id}"
        )
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data=f"show_news"))
    return builder.as_markup()
