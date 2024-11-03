from aiogram import Bot

from app.keyboards.moder import get_question_kb
from app.utils.ranks import get_chat_id


async def ask_question(
    chat_id: int, msg_id: int, username: str, bot: Bot, text: str
) -> bool:
    """
    Отправляет сообщение в чат поддержки.

    :param chat_id: int - ID чата пользователя, отправляющего вопрос.
    :param msg_id: int - ID сообщения пользователя, отправляющего вопрос.
    :param username: str - имя пользователя.
    :param bot: Bot - объект бота, который отправляет сообщение.
    :param text: str - текст сообщения.
    :return: bool - флаг успешности отправки.

    Внутренний процесс:
    1. Получаем ID чата поддержки с помощью функции get_chat_id().
    2. Если ID чата поддержки не найден, возвращаем False.
    3. Отправляем сообщение в чат поддержки, используя объект бота.
       - Форматируем текст сообщения, включая ID чата, ID сообщения и имя пользователя.
       - Добавляем клавиатуру с возможными действиями с помощью функции get_question_kb().
    4. Возвращаем True, если сообщение отправлено успешно.
    """
    chat = await get_chat_id()
    if not chat:
        return False

    await bot.send_message(
        chat,
        f"Вопрос[{chat_id}, {msg_id}]:\nВопрос от {username}:\n{text}",
        reply_markup=get_question_kb(),
    )
    return True
