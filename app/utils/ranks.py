from datetime import UTC, datetime, timedelta
from typing import List, Tuple

import aiofiles
from aiogram import Bot

from app.utils.client import get_id_by_username, get_usernames_by_ids


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


async def get_moders() -> List[str]:
    """
    Эта функция получает список модераторов из текстового файла.

    Она открывает файл 'moders.txt' в асинхронном режиме чтения, читает все строки
    и возвращает их в виде списка кортежей, где каждый кортеж содержит ID и имя модератора.

    :return: Список id модераторов (str).

    Внутренний процесс:
    1. Открываем файл 'moders.txt' в режиме чтения через aiofiles.
    2. Читаем все строки из файла.
    3. Возвращаем список id модераторов.
    """
    try:
        async with aiofiles.open("app/data/moders.txt", mode="r") as f:
            return (id.strip() for id in await f.readlines())
    except Exception as e:
        print(e)
        return []


async def get_full_moders() -> List[Tuple[str, str]]:
    """
    Эта функция получает список модераторов из текстового файла.

    Она открывает файл 'moders.txt' в асинхронном режиме чтения, читает все строки
    и возвращает их в виде списка кортежей, где каждый кортеж содержит ID и имя модератора.

    :return: Список кортежей, где каждый кортеж состоит из ID и имени модератора (str, str).

    Внутренний процесс:
    1. Получаем список модераторов через функцию get_moders.
    2. Получаем имена модераторов через функцию get_usernames_by_ids.
    3. Возвращаем список кортежей, где каждый кортеж состоит из ID и имени модератора.
    """
    ids = await get_moders()
    usernames = await get_usernames_by_ids(ids)
    return list(zip(ids, usernames))


async def get_moder_username(id: int | str) -> str:
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
        ids = await f.readlines()
        if str(id) in ids:
            usernames = await get_usernames_by_ids([str(id)])
            if usernames:
                return usernames[0]
            else:
                return ""


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
    return user_id in moders


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
    except Exception as e:
        print(e)
        print("Не удалось создать ссылку на чат")
        return ""


async def add_moder(username: str) -> int:
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
    3. Получаем ID пользователя по его никнейму.
    4. Проверяем, есть ли ID пользователя в списке модераторов.
    5. Если ID пользователя нет в списке модераторов, добавляем его и возвращаем 1.
    6. Если ID пользователя уже есть в списке модераторов, возвращаем -1.
    7. Если возникает ошибка, возвращаем -2.
    """
    try:
        async with aiofiles.open("app/data/moders.txt", mode="a+") as f:
            moders = await f.readlines()
            id = await get_id_by_username(username)
            if str(id) in moders:
                return -1
            else:
                await f.write(f"{id}\n")
                return 1
    except Exception as e:
        print(e)
        print("Не удалось добавить модератора")
        return -2


async def del_moder(id_or_username: str) -> bool:
    """
    Функция для удаления модератора из списка модераторов.

    Она принимает ID или имя пользователя модератора, который будет удален,
    и ничего не возвращает.

    :param username: имя пользователя модератора, который будет удален.
    :return: Возвращает True, если модератор был успешно удален, иначе False.

    Внутренний процесс:
    1. Открываем файл 'moders.txt' в режиме записи.
    2. Читаем текущий список модераторов из файла.
    3. Получаем ID пользователя по его никнейму.
    4. Проверяем, есть ли ID пользователя в списке модераторов.
    5. Если ID пользователя есть в списке модераторов, удаляем его и возвращаем 1.
    6. Если ID пользователя нет в списке модераторов, возвращаем -1.
    7. Если возникает ошибка, возвращаем -2.
    """
    try:
        async with aiofiles.open("app/data/moders.txt", mode="r+") as f:
            if id_or_username.isdigit():
                id = id_or_username
            else:
                id = await get_id_by_username(id_or_username)
            ids = [id.strip() for id in await f.readlines()]
            if str(id) in ids:
                await f.seek(0)
                await f.truncate()
                await f.write("\n".join([_id for _id in ids if str(_id) != str(id)]))
                return 1
            else:
                return -1
    except:
        return -2


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
    """
    Функция для получения списка ID субадминистраторов.

    Она ничего не принимает и возвращает список ID субадминистраторов.

    :return: Список ID субадминистраторов.

    Внутренний процесс:
    1. Открываем файл 'subadmins.txt' в режиме чтения.
    2. Читаем список ID субадминистраторов из файла.
    3. Возвращаем список ID субадминистраторов.
    """
    async with aiofiles.open("app/data/subadmins.txt", mode="r") as f:
        return [id.strip() for id in await f.readlines()]


async def get_full_subadmins() -> list:
    """
    Функция для получения списка кортежей ID и имени субадминистраторов.

    Она ничего не принимает и возвращает список кортежей ID и имени субадминистраторов.

    :return: Список кортежей ID и имени субадминистраторов.

    Внутренний процесс:
    1. Получаем список ID субадминистраторов с помощью функции get_subadmins().
    2. Получаем список имён субадминистраторов с помощью функции get_usernames_by_ids().
    3. Возвращаем список кортежей ID и имени субадминистраторов.
    """
    ids = await get_subadmins()
    usernames = await get_usernames_by_ids(ids)
    return list(zip(ids, usernames))


async def del_subadmin(id_or_username: str) -> int:
    """
    Функция для удаления субадминистратора из списка субадминистраторов.

    Она принимает имя пользователя субадминистратора, который будет удален.

    :param username: Имя пользователя субадминистратора.
    :return: Возвращает 1, если субадминистратор был успешно удален, иначе -1 или -2.

    Внутренний процесс:
    1. Открываем файл 'subadmins.txt' в режиме добавления и чтения.
    2. Читаем текущий список субадминистраторов из файла.
    3. Получаем ID пользователя по его никнейму, если выдан никнейм.
    4. Проверяем, есть ли ID пользователя в списке субадминистраторов.
    5. Если ID пользователя есть в списке субадминистраторов, удаляем его и возвращаем 1.
    6. Если ID пользователя нет в списке субадминистраторов, возвращаем -1.
    7. Если возникает ошибка, возвращаем -2.
    """
    try:
        async with aiofiles.open("app/data/subadmins.txt", mode="r+") as f:
            if id_or_username.isdigit():
                id = id_or_username
            else:
                id = await get_id_by_username(id_or_username)
            ids = [id.strip() for id in await f.readlines()]
            if str(id) in ids:
                await f.seek(0)
                await f.truncate()
                await f.write("\n".join([_id for _id in ids if str(_id) != str(id)]))
                return 1
            else:
                return -1
    except:
        return -2


async def add_subadmin(username: str) -> int:
    """
    Функция для добавления субадминистратора в список субадминистраторов.

    Она принимает ID и имя пользователя субадминистратора, который будет добавлен.

    :param username: Имя пользователя субадминистратора.
    :return: Возвращает 1, если субадминистратор был успешно добавлен, иначе -1 или -2.

    Внутренний процесс:
    1. Открываем файл 'subadmins.txt' в режиме добавления и чтения.
    2. Читаем текущий список субадминистраторов из файла.
    3. Получаем ID пользователя по его никнейму.
    4. Проверяем, есть ли ID пользователя в списке субадминистраторов.
    5. Если ID пользователя нет в списке субадминистраторов, добавляем его и возвращаем 1.
    6. Если ID пользователя уже есть в списке субадминистраторов, возвращаем -1.
    7. Если возникает ошибка, возвращаем -2.
    """
    try:
        async with aiofiles.open("app/data/subadmins.txt", mode="a+") as f:
            moders = await f.readlines()
            id = await get_id_by_username(username)
            if str(id) in moders:
                return -1
            else:
                await f.write(f"{id}\n")
                return 1
    except Exception as e:
        print(e)
        print("Не удалось добавить модератора")
        return -2


async def is_subadmin(id: str) -> bool:
    """
    Функция для проверки, является ли пользователь субадминистратором.

    Она принимает ID пользователя.

    :param id: ID пользователя.
    :return: Возвращает True, если пользователь является субадминистратором, иначе False.

    Внутренний процесс:
    1. Получаем список ID субадминистраторов с помощью функции get_subadmins().
    2. Проверяем, есть ли переданный ID в списке субадминистраторов.
    3. Если ID пользователя есть в списке субадминистраторов, возвращаем True; в противном случае — False.
    """
    ids = await get_subadmins()
    return str(id) in ids


async def get_subadmin_username(id: str) -> str:
    async with aiofiles.open("app/data/subadmins.txt", mode="r") as f:
        ids = await f.readlines()
        if str(id) in ids:
            usernames = await get_usernames_by_ids([str(id)])
            if usernames:
                return usernames[0]
            else:
                return ""


async def is_able_to_answer(user_id: int) -> bool:
    return (
        (await is_moder(user_id))
        or (await is_admin(user_id))
        or (await is_subadmin(user_id))
    )
