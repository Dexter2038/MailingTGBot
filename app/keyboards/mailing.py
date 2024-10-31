from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_mailing_kb(mailing_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text="Подтвердить", callback_data=f"ConfirmMailing_{mailing_id}"
        ),
        InlineKeyboardButton(text="Отказаться", callback_data="CancelMailing"),
    )

    # Регулирование расположения кнопок
    # kb.adjust()

    return kb.as_markup()
