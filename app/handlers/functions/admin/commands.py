from typing import List, Tuple
from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message


from app.keyboards.admin import get_admin_kb
from app.utils.ranks import (
    add_subadmin,
    del_subadmin,
    get_full_moders,
    get_full_subadmins,
    reset_chat,
    get_chat_link,
    add_moder,
    del_moder,
)
from app.utils.mailing import make_confirm_mailing, make_mailing
from app.utils.info import (
    add_news,
    add_quiz,
    edit_about_quiz,
    edit_rules,
    get_about_quiz,
    edit_faq,
    get_faq,
    edit_news,
    get_news_admin,
    del_news,
    get_quizzes_admin,
    get_quiz,
    edit_quiz,
    del_quiz,
    get_rules,
)

from app.database.actions import end_confirm, get_all_confirms, get_confirm


async def start_command(message: Message, is_subadmin: bool) -> None:
    """
    Эта функция обрабатывает команду /start,
    отправляя приветственное сообщение администратору
    и предлагая ему просмотреть список доступных команд.

    :param message: Объект Message, представляющий сообщение.
    :return: None

    Внутренний процесс:
    1. Отправляем приветственное сообщение администратору.
    2. Предлагаем администратору просмотреть список доступных команд.
    """
    if is_subadmin:
        role = "субадминистратор"
    else:
        role = "администратор"
    await message.answer(
        f"Привет, {role}! Команды доступны по команде /commands",
        reply_markup=get_admin_kb(is_subadmin),
    )


async def commands_command(message: Message, is_subadmin: bool) -> None:
    """
    Эта функция обрабатывает команду /commands, отправляя пользователю
    список всех доступных команд и их описание.

    :param message: Объект Message, представляющий сообщение.
    :return: None

    Внутренний процесс:
    1. Формируем текст, содержащий описание всех доступных команд для пользователя.
    2. Отправляем этот текст в ответ на сообщение пользователя.
    """
    text = (
        "Доступные команды:\n\n"
        "/start - начать работу с ботом\n"
        "/addmoder <username> - назначить пользователя модератором\n"
        "/delmoder <id/username> - убрать пользователя из списка модераторов\n"
        "/moders - посмотреть список модераторов\n"
        "/mailing <текст> - сделать рассылку всем пользователям\n"
        "/confirms - посмотреть список рассылки с подтверждением\n"
        "/confirm <id> - посмотреть участников конкретной рассылки с подтверждением\n"
        "/addconfirm <текст> - начать рассылку с подтверждением\n"
        "/endconfirm <id> - завершить конкретную рассылку с подтверждением\n"
        "/initchat (только в групповом чате) - инициализировать чат с вопросами\n"
        "/askchat - получить ссылку на чат с вопросами\n"
        "/delchat - сбросить чат с вопросами\n"
        "/editaboutquiz <текст> - редактировать информацию о викторине\n"
        "/aboutquiz - посмотреть информацию о викторине\n"
        "/editfaq <текст> - редактировать информацию о частых вопросах\n"
        "/faq - посмотреть информацию о частых вопросах\n"
        "/editrules <текст> - редактировать правила\n"
        "/rules - посмотреть правила\n"
        "/news - посмотреть новости\n"
        "/editnews <id> <текст> - редактировать новость\n"
        "/delnews <id> - удалить новость\n"
        "/quizzes - посмотреть предстоящие викторины\n"
        "/quiz <id> - посмотреть текст предстоящей викторины\n"
        "/editquiz <id> <текст> - редактировать текст предстоящей викторины\n"
        "/delquiz <id> - удалить информацию о предстоящей викторине\n"
        "/commands - посмотреть доступные команды\n"
    )
    if not is_subadmin:
        text += (
            "/addsubadmin <username> - назначить пользователя субадминистратором\n"
            "/delsubadmin <id/username> - убрать пользователя из списка субадминистраторов\n"
            "/subadmins - посмотреть список субадминистраторов\n"
        )

    await message.answer(text)


async def show_moderators_command(message: Message) -> None:
    """
    Команда для администратора, которая показывает список модераторов.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем список модераторов с помощью функции get_full_moders().
    2. Если список модераторов пуст, отправляем сообщение о том, что модераторов нет.
    3. Если модераторы найдены, формируем текст сообщения с их ID, именами.
    4. Отправляем сообщение с данными модераторов.
    """
    moders = await get_full_moders()
    if not moders:
        await message.answer("Нет модераторов")
        return

    text = "Модераторы:\n\n"
    text += "\n".join([f"ID: {moder[0]} - @{moder[1]}" for moder in moders])
    await message.answer(text)


async def add_moderator_command(message: Message, command: CommandObject) -> None:
    """
    Команда для администратора, которая назначает модератором пользователя.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем аргументы команды.
    2. Если аргументов меньше 1, выводим ошибку.
    3. Если пользователь уже является модератором, выводим ошибку.
    4. Если ID или никнейм пользователя правильный, то добавляем его в список модераторов.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /addmoder <username>. Пример: @username или username"
        )
        return

    if len(args) != 1:
        await message.answer(
            "Неверный формат команды. Используйте /addmoder <username>. Пример: @username или username"
        )
        return

    username = args[0]

    username = username.replace("@", "")

    try:
        result = await add_moder(username)

        if result:
            await message.answer("Пользователь назначен модератором")
        else:
            if result == -2:
                await message.answer("Пользователь с таким никнеймом не найден")
            elif result == -1:
                await message.answer("Пользователь уже является модератором")

    except Exception:
        await message.answer("Пользователь не назначен модератором. Произошла ошибка")


async def del_moderator_command(message: Message, command: CommandObject) -> None:
    """
    Команда для удаления модератора из списка модераторов.

    :param message: Объект Message, представляющий сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем аргументы команды.
    2. Если аргументов меньше 1, выводим ошибку.
    3. Если ID пользователя правильный, то удаляем его из списка модераторов.
    4. Если ID пользователя не правильный, выводим ошибку.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /delmoder <id/username>"
        )
        return

    if len(args) != 1:
        await message.answer(
            "Неверный формат команды. Используйте /delmoder <id/username>"
        )
        return

    id = args[0]

    try:
        result = await del_moder(id)

        if result:
            await message.answer("Пользователь удален из списка модераторов")
        else:
            if result == -2:
                await message.answer("Пользователь с таким никнеймом не найден")
            elif result == -1:
                await message.answer("Пользователь не является модератором")

    except Exception as e:
        await message.answer(
            "Пользователь не удален из списка модераторов. Произошла ошибка"
        )


async def show_subadmins_command(message: Message) -> None:
    """
    Команда для администратора, которая показывает список субадминистраторов.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем список субадминистраторов с помощью функции get_subadmins().
    2. Если список субадминистраторов пуст, отправляем сообщение о том, что субадминистраторов нет.
    3. Если модераторы найдены, формируем текст сообщения с их ID, именами.
    4. Отправляем сообщение с данными субадминистраторов.
    """
    subadmins = await get_full_subadmins()
    if not subadmins:
        await message.answer("Нет субадминистраторов")
        return

    text = "Субадминистраторы:\n\n"
    text += "\n".join([f"ID: {subadmin[0]} - @{subadmin[1]}" for subadmin in subadmins])
    await message.answer(text)


async def add_subadmin_command(message: Message, command: CommandObject) -> None:
    """
    Команда для администратора, которая назначает субадминистратором пользователя.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем аргументы команды.
    2. Если аргументов меньше 1, выводим ошибку.
    3. Если пользователь уже является субадминистратором, выводим ошибку.
    4. Если ID или никнейм пользователя правильный, то добавляем его в список модераторов.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /addsubadmin <username>. Пример: @username или username"
        )
        return

    if len(args) != 1:
        await message.answer(
            "Неверный формат команды. Используйте /addsubadmin <username>. Пример: @username или username"
        )
        return

    username = args[0]

    username = username.replace("@", "")

    try:
        result = await add_subadmin(username)

        if result:
            await message.answer("Пользователь назначен субадминистратором")
        else:
            if result == -2:
                await message.answer("Пользователь с таким никнеймом не найден")
            elif result == -1:
                await message.answer("Пользователь уже является субадминистратором")

    except Exception:
        await message.answer(
            "Пользователь не назначен субадминистратором. Произошла ошибка"
        )


async def del_subadmin_command(message: Message, command: CommandObject) -> None:
    """
    Команда для удаления модератора из списка субадминистраторов.

    :param message: Объект Message, представляющий сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем аргументы команды.
    2. Если аргументов меньше 1, выводим ошибку.
    3. Если ID пользователя правильный, то удаляем его из списка субадминистраторов.
    4. Если ID пользователя не правильный, выводим ошибку.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /delsubadmin <id/username>"
        )
        return

    if len(args) != 1:
        await message.answer(
            "Неверный формат команды. Используйте /delsubadmin <id/username>"
        )
        return

    id = args[0]

    try:
        result = await del_subadmin(id)

        if result:
            await message.answer("Пользователь удален из списка субадминистраторов")
        else:
            if result == -2:
                await message.answer("Пользователь с таким никнеймом не найден")
            elif result == -1:
                await message.answer("Пользователь не является субадминистратором")

    except Exception as e:
        await message.answer(
            "Пользователь не удален из списка субадминистраторов. Произошла ошибка"
        )


async def send_mailing_command(
    message: Message, command: CommandObject, bot: Bot
) -> None:
    """
    Команда для администратора, которая отправляет рассылку всем зарегистрированным пользователям.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :param bot: Объект Bot, представляющий бота, который отправляет сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем аргументы команды.
    2. Если аргументов меньше 1, выводим ошибку.
    3. Если аргументы правильные, то отправляем рассылку.
    """
    text = command.args
    if not text:
        await message.answer("Неверный формат команды. Используйте /mailing <текст>")
        return

    result = await make_mailing(text, bot)

    if result:
        await message.answer("Рассылка выполнена")
    else:
        await message.answer("Рассылка не выполнена. Произошла ошибка")


async def del_chat_command(message: Message) -> None:
    """
    Команда для сброса чата вопросов.
    Она не имеет параметров, а возвращает None.

    Внутренний процесс:
    1. Очищаем файл с вопросами.
    2. Отправляем сообщение, подтверждающее сброс чата.
    """
    result = await reset_chat()

    if result:
        await message.answer("Чат сброшен")
    else:
        await message.answer("Чат не сброшен. Произошла ошибка")


async def show_confirms_command(message: Message) -> None:
    """
    Команда для администратора, которая показывает список рассылок с подтверждением.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Проверяем, есть ли рассылки с подтверждением.
    2. Если рассылки с подтверждением нет, выводим сообщение об этом.
    3. Если рассылки с подтверждением есть, выводим список рассылок с подтверждением.
    """
    confirms = get_all_confirms()
    if not confirms:
        await message.answer("Нет рассылок с подтверждением")
        return

    text = "Рассылки с подтверждением:\n\n"
    text += "\n".join(f"ID: {id} - {text}" for id, text in confirms)

    await message.answer(text)


async def show_confirm_command(message: Message, command: CommandObject) -> None:
    """
    Команда для администратора, которая показывает рассылку с подтверждением.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Проверяем, есть ли рассылка с подтверждением.
    2. Если рассылка с подтверждением нет, выводим сообщение об этом.
    3. Если рассылка с подтверждением есть, выводим рассылку с подтверждением.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /confirm <id>")
        return

    if len(args) != 1 or not args[0].isdigit():
        await message.answer("Неверный формат команды. Используйте /confirm <id>")
        return

    id = args[0]

    confirm = get_confirm(id)

    if not confirm:
        await message.answer("Рассылка с подтверждением не найдена")
        return
    description, users = confirm

    description: str
    users: List[Tuple[int, str]]

    text = (
        f"Рассылка с подтверждением:\n\n"
        f"ID: {id}\n"
        f"Текст: {description}\nУчастники:\n"
    )
    text += "\n".join(f"ID: {id} - @{username}" for id, username in users)

    await message.answer(text)


async def add_confirm_command(
    message: Message, command: CommandObject, bot: Bot
) -> None:
    """
    Команда для администратора, которая начинает рассылку с подтверждением.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :param bot: Объект Bot, представляющий бота, который отправляет сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем текст рассылки.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст непустой, начинаем рассылку с подтверждением.
    """
    text = command.args

    if not text:
        await message.answer("Неверный формат команды. Используйте /addconfirm <текст>")
        return

    result = await make_confirm_mailing(text, bot)

    if result:
        await message.answer("Рассылка с подтверждением выполнена")
    else:
        await message.answer("Рассылка с подтверждением не выполнена. Произошла ошибка")


async def del_confirm_command(message: Message, command: CommandObject) -> None:
    """
    Команда для завершения рассылки с подтверждением.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем ID рассылки.
    2. Если ID не предоставлен или неверный, выводим сообщение об ошибке.
    3. Если ID правильный, завершаем рассылку с подтверждением.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /endconfirm <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /endconfirm <id>")
        return

    id = args[0]

    result = end_confirm(id)

    if result:
        await message.answer("Рассылка с подтверждением закончена")
    else:
        await message.answer("Рассылка с подтверждением не закончена. Произошла ошибка")


async def show_chat_command(message: Message, bot: Bot) -> None:
    """
    Команда для получения ссылки на чат с вопросами.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param bot: Объект Bot, представляющий бота, который отправляет сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем ссылку на чат с вопросами с помощью функции get_chat_link().
    2. Если ссылка не найдена, выводим сообщение об этом.
    3. Если ссылка найдена, отправляем её в ответе на сообщение пользователя.
    """
    chat_link = await get_chat_link(bot)

    if not chat_link:
        await message.answer("Чат не инициализирован")
        return

    await message.answer(f"Ссылка на чат: {chat_link}")


async def edit_about_quiz_command(message: Message, command: CommandObject) -> None:
    """
    Команда для редактирования информации о викторине.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем текст для редактирования информации о викторине.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст непустой, обновляем информацию о викторине.
    """
    args = command.args

    if not args:
        await message.answer(
            "Неверный формат команды. Используйте /editaboutquiz <текст>"
        )
        return

    result = await edit_about_quiz(args)

    if result:
        await message.answer("Информация о викторине обновлена")
    else:
        await message.answer("Информация о викторине не обновлена. Произошла ошибка")


async def show_about_quiz_command(message: Message) -> None:
    """
    Команда для просмотра информации о викторине.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем информацию о викторине с помощью функции get_about_quiz().
    2. Если информация не найдена, выводим сообщение об этом.
    3. Если информация найдена, отправляем её в ответе на сообщение пользователя.
    """
    quiz_info = await get_about_quiz()

    if not quiz_info:
        await message.answer("Информация о викторине не найдена")
        return

    await message.answer(quiz_info)


async def edit_faq_command(message: Message, command: CommandObject) -> None:
    """
    Команда для редактирования информации о частых вопросах.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем текст для редактирования информации о частых вопросах.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст непустой, обновляем информацию о частых вопросах.
    """
    args = command.args

    if not args:
        await message.answer("Неверный формат команды. Используйте /editfaq <текст>")
        return

    result = await edit_faq(args)

    if result:
        await message.answer("Информация о частых вопросах обновлена")
    else:
        await message.answer(
            "Информация о частых вопросах не обновлена. Произошла ошибка"
        )


async def show_faq_command(message: Message) -> None:
    """
    Команда для просмотра информации о частых вопросах.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем информацию о частых вопросах с помощью функции get_faq().
    2. Если информация не найдена, выводим сообщение об этом.
    3. Если информация найдена, отправляем её в ответе на сообщение пользователя.
    """
    faq = await get_faq()

    if not faq:
        await message.answer("Информация о частых вопросах не найдена")
        return

    await message.answer(faq)


async def edit_rules_command(message: Message, command: CommandObject) -> None:
    """
    Команда для редактирования правил.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем текст для редактирования правил.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст непустой, обновляем правила.
    """
    args = command.args

    if not args:
        await message.answer("Неверный формат команды. Используйте /editrules <текст>")
        return

    result = await edit_rules(args)

    if result:
        await message.answer("Правила обновлены")
    else:
        await message.answer("Правила не обновлены. Произошла ошибка")


async def show_rules_command(message: Message) -> None:
    """
    Команда для просмотра правил.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем правила с помощью функции get_rules().
    2. Если информация не найдена, выводим сообщение об этом.
    3. Если информация найдена, отправляем её в ответе на сообщение пользователя.
    """
    rules = await get_rules()

    if not rules:
        await message.answer("Правила не найдены")
        return

    await message.answer(rules)


async def show_news_command(message: Message) -> None:
    """
    Команда для просмотра новостей.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем список новостей с помощью функции get_news_admin().
    2. Если список новостей не найден, выводим сообщение об этом.
    3. Если список новостей найден, отправляем его в ответе на сообщение пользователя.
    """
    news = await get_news_admin()

    if not news:
        await message.answer("Новости не найдены")
        return

    text = "Новости:\n\n"
    text += "\n".join(f"ID: {new[0]} - {new[1]}" for new in news)

    await message.answer(text)


async def add_news_command(message: Message, command: CommandObject) -> None:
    """
    Команда для добавления новости.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем текст новости.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст непустой, добавляем новость с помощью функции add_news().
    4. Если новость была успешно добавлена, отправляем сообщение об этом.
    5. Если новость не была добавлена, отправляем сообщение об ошибке.
    """
    args = command.args

    if not args:
        await message.answer("Неверный формат команды. Используйте /addnews <текст>")
        return

    result = await add_news(args)

    if result:
        await message.answer("Новость добавлена")
    else:
        await message.answer("Новость не добавлена. Произошла ошибка")


async def edit_news_command(message: Message, command: CommandObject) -> None:
    """
    Команда для редактирования новости.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем текст для редактирования новости.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст непустой, обновляем новость с помощью функции edit_news().
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /editnews <id> <текст>"
        )
        return

    if len(args) < 2 or not args[0].isdigit():
        await message.answer(
            "Неверный формат команды. Используйте /editnews <id> <текст>"
        )
        return

    id = args[0]
    text = " ".join(args[1:])

    result = await edit_news(id, text)

    if result:
        await message.answer("Новость обновлена")
    else:
        await message.answer("Новость не обновлена. Произошла ошибка")


async def delete_news_command(message: Message, command: CommandObject) -> None:
    """
    Команда для удаления новости.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем ID новости из параметров команды.
    2. Если ID новости не найден, выводим сообщение об ошибке.
    3. Если ID новости найден, удаляем новость с помощью функции del_news().
    4. Если новость была успешно удалена, отправляем сообщение об этом.
    5. Если новость не была удалена, отправляем сообщение об ошибке.
    """
    args = command.args

    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /delnews <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /delnews <id>")
        return

    id = args[0]

    result = await del_news(id)

    if result:
        await message.answer("Новость удалена")
    else:
        await message.answer("Новость не удалена. Произошла ошибка")


async def show_quizzes_command(message: Message) -> None:
    """
    Команда для просмотра предстоящих викторин.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем список предстоящих викторин из базы данных.
    2. Если список викторин пуст, выводим сообщение об этом.
    3. Если викторины найдены, формируем текст сообщения с их ID и текстом.
    4. Отправляем сообщение с данными викторин.
    """
    quizzes = await get_quizzes_admin()

    if not quizzes:
        await message.answer("Предстоящие викторины не найдены")
        return

    text = "Предстоящие викторины:\n\n"
    text += "\n".join(f"ID: {quiz[0]} - {quiz[1]}" for quiz in quizzes)

    await message.answer(text)


async def show_quiz_command(message: Message, command: CommandObject) -> None:
    """
    Команда для просмотра предстоящей викторины.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем ID викторины.
    2. Если ID не указан, выводим сообщение об ошибке.
    3. Если ID указан, получаем текст викторины.
    4. Если викторина не найдена, выводим сообщение об этом.
    5. Если викторина найдена, отправляем текст в ответе на сообщение пользователя.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /quiz <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /quiz <id>")
        return

    id = args[0]

    quiz = await get_quiz(id)

    if not quiz:
        await message.answer("Предстоящая викторина не найдена")
        return

    await message.answer(quiz)


async def add_quiz_command(message: Message, command: CommandObject) -> None:
    """
    Команда для добавления предстоящей викторины.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем текст для добавления викторины.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст не пустой, добавляем викторину.
    """
    args = command.args

    if not args:
        await message.answer("Неверный формат команды. Используйте /addquiz <текст>")
        return

    result = await add_quiz(args)

    if result:
        await message.answer("Предстоящая викторина добавлена")
    else:
        await message.answer("Предстоящая викторина не добавлена. Произошла ошибка")


async def edit_quiz_command(message: Message, command: CommandObject) -> None:
    """
    Команда для редактирования викторины.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем ID викторины и текст для редактирования.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст не пустой, обновляем викторину.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /editquiz <id> <текст>"
        )
        return

    if len(args) < 2 or not args[0].isdigit():
        await message.answer(
            "Неверный формат команды. Используйте /editquiz <id> <текст>"
        )
        return

    id = args[0]
    text = " ".join(args[1:])

    result = await edit_quiz(id, text)

    if result:
        await message.answer("Предстоящая викторина обновлена")
    else:
        await message.answer("Предстоящая викторина не обновлена. Произошла ошибка")


async def delete_quiz_command(message: Message, command: CommandObject) -> None:
    """Команда для удаления викторины.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем аргументы команды.
    2. Если аргументы пустые, выводим сообщение об ошибке.
    3. Если аргументы непустые, удаляем викторину.
    """
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /delquiz <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /delquiz <id>")
        return

    id = args[0]

    result = await del_quiz(id)

    if result:
        await message.answer("Предстоящая викторина удалена")
    else:
        await message.answer("Предстоящая викторина не удалена. Произошла ошибка")


async def add_quiz_command(message: Message, command: CommandObject) -> None:
    """
    Команда для добавления новой предстоящей викторины.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param command: Объект CommandObject, представляющий команду.
    :return: None

    Внутренний процесс:
    1. Получаем текст из аргумента команды для добавления викторины.
    2. Если текст пустой, выводим сообщение об ошибке.
    3. Если текст непустой, добавляем новую викторину.
    """
    text = command.args

    if not text:
        await message.answer("Неверный формат команды. Используйте /addquiz <текст>")
        return

    result = await add_quiz(text)

    if result:
        await message.answer("Предстоящая викторина добавлена")
    else:
        await message.answer("Предстоящая викторина не добавлена. Произошла ошибка")


async def echo_message(message: Message) -> None:
    """

    Эта функция обрабатывает любые сообщения, которые не соответствуют
    ни одной из команд администратора.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None
    """
    await message.answer("Чтобы начать, напишите /start")
