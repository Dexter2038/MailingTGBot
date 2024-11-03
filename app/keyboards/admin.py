from typing import List, Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Показать модераторов", callback_data="show_moders"),
        InlineKeyboardButton(text="Добавить модератора", callback_data="add_moderator"),
        InlineKeyboardButton(text="Сделать рассылку", callback_data="make_mailing"),
        InlineKeyboardButton(text="Показать рассылки", callback_data="show_confirms"),
        InlineKeyboardButton(
            text="Сбросить чат вопросов", callback_data="ask_del_chat"
        ),
        InlineKeyboardButton(text="Показать викторины", callback_data="show_quizzes"),
        InlineKeyboardButton(text="Показать новости", callback_data="show_all_news"),
        InlineKeyboardButton(text="Показать чат", callback_data="show_chat"),
        InlineKeyboardButton(
            text="Редактировать о викторине", callback_data="edit_about_quiz"
        ),
        InlineKeyboardButton(
            text="Редактировать частые вопросы", callback_data="edit_faq"
        ),
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


def get_about_quiz_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_faq_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
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


def get_del_moder_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить другого модератора", callback_data="show_moders"
        )
    )
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
