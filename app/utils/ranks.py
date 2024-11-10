from datetime import UTC, datetime, timedelta
from typing import List, Tuple

import aiofiles
from aiogram import Bot


def init_rank_files(admin) -> None:
    """
    Инициализирует файлы рангов, если они не существуют.

    :return: None
    Инициализирует файлы рангов, если они не существуют.
    --admin <ID> - ID администратора, который будет добавлен в файл admin.txt.
    Если параметр --admin не указан, то файл admin.txt будет создан,
    но ничего в него не будет записано.
    """
    if admin:
        with open("app/data/admin.txt", mode="w") as f:
            f.write(str(admin))
    else:
        with open("app/data/admin.txt", mode="a") as f:
            pass
    with open("app/data/moders.txt", mode="a") as f:
        pass
    with open("app/data/chat.txt", mode="a") as f:
        pass
    with open("app/data/subadmins.txt", mode="a") as f:
        pass


async def get_moders() -> List[Tuple[str, str]]:
    """
    Эта функция получает список модераторов из текстового файла.

    Она открывает файл 'moders.txt' в асинхронном режиме чтения, читает все строки
    и возвращает их в виде списка кортежей, где каждый кортеж содержит ID и имя модератора.

    :return: Список кортежей, где каждый кортеж состоит из ID и имени модератора (str, str).

    Внутренний процесс:
    1. Открываем файл 'moders.txt' в режиме чтения через aiofiles.
    2. Читаем все строки из файла.
    3. Разделяем каждую строку по пробелам и преобразуем в кортеж (ID, имя).
    4. Если возникает ошибка, возвращаем пустой список.
    """
    try:
        async with aiofiles.open("app/data/moders.txt", mode="r") as f:
            lines = await f.readlines()
            return list(map(lambda line: line.split(" "), lines))
    except Exception as e:
        print(e)
        return []


async def get_moder(id: int | str) -> str:
    """
    Эта функция получает информацию о модераторе из текстового файла.

    Она открывает файл 'moders.txt' в асинхронном режиме чтения, читает все строки,
    находит строку, содержащую переданный ID, преобразует ее в кортеж (ID, имя)
    и возвращает его.

    :param id: ID модератора, который будет найден.
    :return: Кортеж, содержащий ID и имя модератора (str, str).

    Внутренний процесс:
    1. Открываем файл 'moders.txt' в режиме чтения через aiofiles.
    2. Читаем все строки из файла.
    3. Ищем строку, содержащую переданный ID, и преобразуем ее в кортеж.
    4. Если модератор не найден, возвращаем пустой кортеж.
    """
    async with aiofiles.open("app/data/moders.txt", mode="r") as f:
        lines = await f.readlines()
        moders = list(map(lambda line: line.split(" "), lines))
        moder = next(filter(lambda moder: moder[0] == str(id), moders), None)
        return moder


async def reset_chat() -> bool:
    """
    Эта функция сбрасывает содержимое файла чата, очищая его.

    :return: Возвращает True, если файл успешно очищен, иначе False.

    Внутренний процесс:
    1. Открываем файл 'chat.txt' в режиме записи, чтобы очистить его содержимое.
    2. Записываем пустую строку в файл, чтобы удалить все данные.
    3. Если операция проходит успешно, возвращаем True.
    4. Если возникает ошибка, возвращаем False.
    """
    try:
        async with aiofiles.open("app/data/chat.txt", mode="w") as f:
            await f.write("")
        return True
    except Exception:
        return False


async def get_chat_id() -> int:
    """
    Эта функция получает ID чата из текстового файла.

    Она открывает файл 'chat.txt' в асинхронном режиме чтения, читает строку,
    преобразует ее в целое число и возвращает его.

    :return: ID чата (int).

    Внутренний процесс:
    1. Открываем файл 'chat.txt' в режиме чтения через aiofiles.
    2. Читаем строку из файла.
    3. Преобразуем строку в целое число.
    4. Если файл пуст, возвращаем 0.
    """
    async with aiofiles.open("app/data/chat.txt", mode="r") as f:
        chat_id = await f.read()
        return int(chat_id) if chat_id else 0


async def set_chat_id(chat_id: int) -> None:
    """
    Эта функция записывает ID чата в файл 'chat.txt'.
    Она принимает ID чата (int) и ничего не возвращает.

    :param chat_id: ID чата, который будет записан в файл.
    :return: None

    Внутренний процесс:
    1. Открываем файл 'chat.txt' в режиме записи.
    2. Записываем ID чата в файл.
    """
    async with aiofiles.open("app/data/chat.txt", mode="w") as f:
        await f.write(str(chat_id))


async def is_moder(user_id: int) -> bool:
    """
    Эта функция проверяет, является ли пользователь модератором.

    :param user_id: Целое число, представляющее ID пользователя.
    :return: Возвращает True, если пользователь является модератором, иначе False.

    Внутренний процесс:
    1. Получаем список модераторов с помощью функции get_moders().
    2. Преобразуем каждый ID модератора в целое число.
    3. Проверяем, содержится ли переданный ID пользователя в списке ID модераторов.
    4. Если ID пользователя найден, возвращаем True; в противном случае — False.
    """
    moders = await get_moders()
    return user_id in [int(moder[0]) for moder in moders]


async def is_admin(user_id: int) -> bool:
    """
    Функция, которая проверяет, является ли пользователь администратором.

    Она принимает ID пользователя (int) и ничего не возвращает.

    :param user_id: ID пользователя, который будет проверяться.
    :return: Возвращает True, если пользователь является администратором, иначе False.

    Внутренний процесс:
    1. Получаем ID администратора с помощью функции get_admin().
    2. Сравниваем ID пользователя с ID администратора.
    3. Если они совпадают, возвращаем True; в противном случае — False.
    """
    admin = await get_admin()
    return user_id == admin


async def get_chat_link(bot: Bot) -> str:
    """
    Функция, которая получает ссылку на чат вопросов.

    Она принимает объект Bot, представляющий бота, и ничего не возвращает.

    :param bot: Объект Bot, представляющий бота.
    :return: Возвращает ссылку на чат вопросов (str).

    Внутренний процесс:
    1. Получаем ID чата вопросов с помощью функции get_chat_id().
    2. Если ID чата пуст, возвращаем пустую строку.
    3. Получаем ссылку на чат вопросов с помощью функции create_chat_invite_link().
    4. Если операция проходит успешно, возвращаем ссылку на чат.
    5. Если возникает ошибка, возвращаем пустую строку.
    """
    chat_id = await get_chat_id()

    if chat_id == 0:
        return ""

    try:
        cur_time = datetime.now(UTC)
        final_time = cur_time + timedelta(days=1)
        chat_link = await bot.create_chat_invite_link(chat_id, expire_date=final_time)
        chat_link = chat_link.invite_link
        return chat_link
    except Exception:
        return ""


async def add_moder(id: str, username: str) -> bool:
    """
    Функция для добавления модератора в список.

    Она принимает ID и имя пользователя модератора, проверяет, существует ли
    он уже в списке модераторов, и добавляет его, если не существует.

    :param id: ID пользователя, который будет добавлен в список модераторов.
    :param username: Имя пользователя, который будет добавлен в список модераторов.
    :return: Возвращает True, если модератор был успешно добавлен, иначе False.

    Внутренний процесс:
    1. Открываем файл 'moders.txt' в режиме добавления и чтения.
    2. Читаем текущий список модераторов из файла.
    3. Преобразуем каждую строку в список, содержащий ID и имя пользователя.
    4. Проверяем, существует ли модератор в текущем списке.
    5. Если модератор найден, возвращаем False.
    6. Если модератор не найден, добавляем его в файл и возвращаем True.
    """
    async with aiofiles.open("app/data/moders.txt", mode="a+") as f:
        lines = await f.readlines()
        moders = list(map(lambda line: line.split(" "), lines))
        ismoder = any(id in moder for moder in moders)
        if ismoder in moders:
            return False
        else:
            await f.write(f"{id} {username}\n")
            return True


async def del_moder(id_or_username: str) -> bool:
    """
    Функция для удаления модератора из списка модераторов.

    Она принимает ID или имя пользователя модератора, который будет удален,
    и ничего не возвращает.

    :param id_or_username: ID или имя пользователя модератора, который будет удален.
    :return: Возвращает True, если модератор был успешно удален, иначе False.

    Внутренний процесс:
    1. Открываем файл 'moders.txt' в режиме записи.
    2. Читаем текущий список модераторов из файла.
    3. Преобразуем каждую строку в список, содержащий ID и имя пользователя.
    4. Проверяем, существует ли модератор в текущем списке.
    5. Если модератор найден, удаляем его из файла.
    6. Если модератор не найден, возвращаем False.
    """
    async with aiofiles.open("app/data/moders.txt", mode="r+") as f:
        lines = await f.readlines()
        moders = list(map(lambda line: line.split(" "), lines))
        ismoder = any(id_or_username in moder for moder in moders)
        if ismoder:
            await f.seek(0)
            await f.truncate()
            await f.write(
                "\n".join(
                    [" ".join(moder) for moder in moders if id_or_username not in moder]
                )
            )
            return True
        else:
            return False


async def get_admin() -> int:
    """
    Функция для получения ID администратора.

    Она ничего не принимает и возвращает ID администратора.
    Если администратор не существует, возвращает 0.

    :return: ID администратора.

    Внутренний процесс:
    1. Открываем файл 'admin.txt' в режиме чтения.
    2. Читаем ID администратора из файла.
    3. Если ID существует, преобразуем его в целое число и возвращаем.
    4. Если ID не существует, возвращаем 0.
    """

    async with aiofiles.open("app/data/admin.txt", mode="r") as f:
        admin = await f.read()
        return int(admin) if admin else 0


async def get_subadmins() -> list:
    async with aiofiles.open("app/data/subadmins.txt", mode="r") as f:
        lines = await f.readlines()
        return [line.strip().split(" ") for line in lines]


async def del_subadmin(id_or_username: str) -> bool:
    async with aiofiles.open("app/data/subadmins.txt", mode="r+") as f:
        lines = await f.readlines()
        subadmins = [line.strip().split(" ") for line in lines]
        if any(id_or_username in subadmin for subadmin in subadmins):
            await f.seek(0)
            await f.truncate()
            await f.write(
                "\n".join(
                    [
                        " ".join(subadmin)
                        for subadmin in subadmins
                        if id_or_username not in subadmin
                    ]
                )
            )
            return True
        else:
            return False


async def add_subadmin(id: str, username: str) -> bool:
    async with aiofiles.open("app/data/subadmins.txt", mode="a+") as f:
        lines = await f.readlines()
        subadmins = [line.strip().split(" ") for line in lines]
        if any(id in subadmin for subadmin in subadmins):
            return False
        else:
            await f.write(f"{id} {username}\n")
            return True


async def is_subadmin(id_or_username: str) -> bool:
    async with aiofiles.open("app/data/subadmins.txt", mode="r") as f:
        lines = await f.readlines()
        subadmins = [line.strip().split(" ") for line in lines]
        return any(str(id_or_username) in subadmin for subadmin in subadmins)


async def get_subadmin(id_or_username: str) -> str:
    async with aiofiles.open("app/data/subadmins.txt", mode="r") as f:
        lines = await f.readlines()
        subadmins = [line.strip().split(" ") for line in lines]
        for subadmin in subadmins:
            if id_or_username in subadmin:
                return subadmin
        return None


async def is_able_to_answer(user_id: int) -> bool:
    return (
        (await is_moder(user_id))
        or (await is_admin(user_id))
        or (await is_subadmin(user_id))
    )
