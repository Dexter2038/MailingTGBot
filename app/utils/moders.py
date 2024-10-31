import os
from typing import List, Tuple

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from app.keyboards.help import get_question_kb


def get_moders() -> List[Tuple[str, str]]:
    """
    Возвращает id и username модераторов из файла moders.txt
    """
    with open(file="moders.txt", mode="r") as f:
        res: List[str] = f.read().splitlines()
        return list(map(lambda x: x.split(" "), res))


def add_moder(id: str, username: str) -> bool:
    """
    Добавляет модератора в файл moders.txt

    Args:
        id: str - id модератора
        username: str - имя модератора

    Returns:
        bool: - True, если модератор успешно добавлен, False - в противном случае
    """
    if id in get_moders():
        return False
    with open(file="moders.txt", mode="a") as f:
        f.write(f"{id} {username}\n")
    return True


def del_moder(moder: str) -> bool:
    """
    Удаляет модератора из файла moders.txt

    Args:
        moder: str - id/username модератора

    Returns:
        bool: - True, если модератор успешно удален, False - в противном случае
    """
    try:
        with open(file="moders.txt", mode="w") as f:
            res: List[str] = f.read().splitlines()
            res = list(map(lambda x: x.split(" "), res))
            res = [sublist for sublist in res if moder not in sublist]
            result = "\n".join(" ".join(sublist) for sublist in res)
        return True
    except ValueError:
        return False


async def ask_question(
    chat_id: int, username: str, msg_id: int, bot: Bot, text: str
) -> bool:
    """
    Отправляет сообщение всем модераторам в ччат

    Args:
        text (str): текст сообщения.
        bot (Bot): объект бота, который отправляет сообщение.
        chat_id (int): id чата пользователя, который отправляет вопрос
        msg_id (int): id сообщения пользователя, который отправляет вопрос
        username (str): имя пользователя

    Returns:
        bool: флаг успешности отправки.
    """
    with open("chat.txt", "r") as f:
        chat: str = f.read()
    if not chat:
        return False

    kb: InlineKeyboardMarkup = get_question_kb(chat_id, msg_id)

    await bot.send_message(chat, f"Вопрос от {username}:\n{text}", reply_markup=kb)
    return True
