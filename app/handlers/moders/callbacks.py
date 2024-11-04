from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery
from app.keyboards.moder import get_chat_kb, get_moder_kb
from app.utils.ranks import get_chat_link


router = Router(name="moder_callbacks")


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery) -> None:
    """
    Обработка callback-запроса на старт.
    Эта функция изменяет текст сообщения на инструкцию для модератора
    и отправляет сообщение с клавиатурой для выбора действия.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Изменяем текст сообщения на инструкцию.
    2. Отправляем сообщение с клавиатурой.
    """
    await callback.message.edit_text(
        "Пока что у тебя есть возможность только отвечать на вопросы в чате",
        reply_markup=get_moder_kb(),
    )


@router.callback_query(F.data == "show_chat")
async def show_chat_callback(callback: CallbackQuery, bot: Bot) -> None:
    """
    Обработка callback-запроса на получение ссылки на чат.
    Эта функция получает ссылку на чат, используя функцию get_chat_link(),
    и отправляет сообщение с этой ссылкой или информацией
    о том, что чат не инициализирован.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param bot: Объект Bot, представляющий бота.
    :return: None

    Внутренний процесс:
    1. Получаем ссылку на чат.
    2. Если ссылка не найдена, отправляем сообщение об этом.
    3. Если ссылка найдена, отправляем сообщение с этой ссылкой.
    """
    chat_link = await get_chat_link(bot)

    if not chat_link:
        await callback.message.answer(
            "Чат ещё не инициализирован админом", get_chat_kb()
        )
    else:
        await callback.message.answer(
            f"Ссылка на чат: {chat_link}", get_chat_kb(chat_link)
        )
