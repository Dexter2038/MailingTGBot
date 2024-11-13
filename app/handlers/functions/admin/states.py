from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.actions import add_confirm, end_confirm

from app.states.admin import Admin
from app.utils.ask import ask_question
from app.utils.info import (
    add_news,
    add_quiz,
    edit_about_quiz,
    edit_faq,
    edit_news,
    edit_quiz,
    edit_rules,
)
from app.utils.mailing import make_mailing
from app.utils.ranks import add_moder, add_subadmin, del_moder
from app.keyboards.admin import get_back_kb, get_back_user_kb


async def ask_question_state(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обрабатывает сообщение пользователя с вопросом и отправляет его в чат поддержки.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :param bot: Объект Bot, представляющий бота, который отправляет сообщение.
    :return: None

    Внутренний процесс:
    1. Вызываем функцию ask_question(), передавая необходимые параметры, для отправки вопроса в чат поддержки.
    2. Анализируем результат выполнения функции ask_question().
    3. Если вопрос успешно отправлен, уведомляем пользователя об успешной отправке.
    4. Если отправка не удалась, уведомляем пользователя о неудаче и предлагаем попробовать позже.
    5. Очищаем текущее состояние машины состояний.
    """
    result = await ask_question(
        message.from_user.id,
        message.message_id,
        message.from_user.username,
        bot,
        message.text,
    )

    if result:
        await message.answer("Ваш вопрос отправлен", reply_markup=get_back_user_kb())
    else:
        await message.answer(
            "Ваш вопрос не отправлен. Попробуйте позже", reply_markup=get_back_user_kb()
        )
    await state.clear()


async def add_moder_state(message: Message, state: FSMContext) -> None:
    """
    Функция, которая обрабатывает сообщение, отправленное администратором,
    для добавления модератора. Она очищает текущее состояние, получает
    информацию о пользователе, пытается добавить модератора, используя
    функцию add_moder(), и отправляет сообщение с результатом.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем аргументы сообщения.
    3. Если аргументы неправильны, отправляем сообщение с инструкциями.
    4. Если аргументы правильны, пытаемся добавить модератора.
    5. Если модератор успешно добавлен, отправляем сообщение об успешном
    добавлении.
    6. Если пользователь уже является модератором, отправляем соответствующее
    сообщение.
    7. Если возникла ошибка, отправляем сообщение об ошибке.
    """
    args = message.text.split(" ")

    if len(args) != 1:
        await message.answer(
            "Неверный формат. Введите <username> пользователя, которого хотите назначить модератором. Пример: @username или username",
            reply_markup=get_back_kb(),
        )
        return

    username = args[0]

    username = username.replace("@", "")

    try:
        result = await add_moder(username)

        if result:
            await message.answer(
                "Пользователь назначен модератором", reply_markup=get_back_kb()
            )
        else:
            if result == -1:
                await message.answer(
                    "Пользователь уже является модератором",
                    reply_markup=get_back_kb(),
                )
            if result == -2:
                await message.answer(
                    "Пользователь с таким никнеймом не наиден",
                    reply_markup=get_back_kb(),
                )

    except Exception:
        await message.answer(
            "Пользователь не назначен модератором. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


async def add_subadmin_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение, отправленное администратором,
    для добавления субадмина. Она получает текст сообщения,
    пытается добавить субадмина, используя функцию add_subadmin(),
    и отправляет сообщение с результатом.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Получаем аргументы сообщения.
    2. Если аргументы неправильны, отправляем сообщение с инструкциями.
    3. Если аргументы правильны, пытаемся добавить субадмина.
    4. Если субадмин успешно добавлен, отправляем сообщение об успешном
    добавлении.
    5. Если пользователь уже является субадмином, отправляем соответствующее
    сообщение.
    6. Если возникла ошибка, отправляем сообщение об ошибке.
    """
    args = message.text.split(" ")

    if len(args) != 1:
        await message.answer(
            "Неверный формат. Введите <username> пользователя, которого хотите назначить субадминистратором. Пример: @username или username",
            reply_markup=get_back_kb(),
        )
        return

    username = args[0]

    username = username.replace("@", "")

    try:
        result = await add_subadmin(username)

        if result:
            await message.answer(
                "Пользователь назначен субадмином", reply_markup=get_back_kb()
            )
        else:
            if result == -1:
                await message.answer(
                    "Пользователь уже является субадмином",
                    reply_markup=get_back_kb(),
                )
            if result == -2:
                await message.answer(
                    "Пользователь с таким никнеймом не наиден",
                    reply_markup=get_back_kb(),
                )

    except Exception:
        await message.answer(
            "Пользователь не назначен субадмином. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


async def make_mailing_state(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Эта функция обрабатывает сообщение, отправленное администратором,
    для запуска рассылки. Она получает текст сообщения, передает его
    на функцию make_mailing() для отправки и оповещает пользователя
    о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :param bot: Объект Bot, представляющий бота, который отправляет сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся отправить рассылку, используя функцию make_mailing().
    3. Если рассылка успешно отправлена, отправляем сообщение об успешной
    отправке.
    4. Если рассылка не отправлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await make_mailing(text, bot)

        if result:
            await message.answer("Рассылка запущена", reply_markup=get_back_kb())
        else:
            await message.answer("Рассылка не запущена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Рассылка не запущена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


async def add_news_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение, отправленное администратором,
    для добавления новостей. Она получает текст сообщения,
    передает его на функцию add_news() для добавления
    и оповещает пользователя о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся добавить новость, используя функцию add_news().
    3. Если новость была успешно добавлена, отправляем сообщение об успешном
    добавлении.
    4. Если новость не была добавлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await add_news(text)

        if result:
            await message.answer("Новости добавлены", reply_markup=get_back_kb())
        else:
            await message.answer("Новости не добавлены", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Новости не добавлены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


async def add_quiz_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение, отправленное администратором,
    для добавления викторины. Она получает текст сообщения,
    передает его на функцию add_quiz() для добавления
    и оповещает пользователя о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся добавить викторину, используя функцию add_quiz().
    3. Если викторина была успешно добавлена, отправляем сообщение об успешном
    добавлении.
    4. Если викторина не была добавлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await add_quiz(text)

        if result:
            await message.answer("Викторина добавлена", reply_markup=get_back_kb())
        else:
            await message.answer("Викторина не добавлена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Викторина не добавлена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


async def add_confirm_state(message: Message, state: FSMContext) -> None:
    """
    Эта функция обрабатывает сообщение, отправленное администратором,
    для добавления рассылки с подтверждением. Она получает текст сообщения,
    передает его на функцию add_confirm() для добавления и оповещает
    пользователя о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся добавить рассылку с подтверждением, используя функцию add_confirm().
    3. Если рассылка успешно добавлена, отправляем сообщение об успешном
       добавлении.
    4. Если рассылка не была добавлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = add_confirm(text)

        if result:
            await message.answer(
                "Рассылка с подтверждением выполнена", reply_markup=get_back_kb()
            )
        else:
            await message.answer(
                "Рассылка с подтверждением не выполнена", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Рассылка с подтверждением не выполнена. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


async def edit_about_quiz_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение для редактирования информации о викторине.
    Получает текст сообщения от пользователя и пытается обновить
    информацию в базе данных.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст из сообщения пользователя.
    2. Вызываем функцию edit_about_quiz() для обновления текста в базе данных.
    3. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    4. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    5. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await edit_about_quiz(text)

        if result:
            await message.answer("О викторине изменено", reply_markup=get_back_kb())
        else:
            await message.answer("О викторине не изменено", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "О викторине не изменено. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


async def edit_faq_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение для редактирования информации о часто задаваемых вопросах (FAQ).
    Получает текст сообщения от пользователя и пытается обновить информацию в базе данных.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст из сообщения пользователя.
    2. Вызываем функцию edit_faq() для обновления текста в базе данных.
    3. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    4. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    5. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await edit_faq(text)

        if result:
            await message.answer("Частые вопросы изменены", reply_markup=get_back_kb())
        else:
            await message.answer(
                "Частые вопросы не изменены", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Частые вопросы не изменены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


async def edit_news_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение для редактирования новости.
    Функция извлекает текст новости из сообщения пользователя и обновляет
    соответствующую запись в базе данных.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст новости из сообщения пользователя.
    2. Получаем данные состояния, чтобы извлечь ID новости для редактирования.
    3. Пытаемся обновить новость в базе данных, вызывая функцию edit_news().
    4. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    5. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    data = await state.get_data()

    id = data.get("id", None)

    try:
        result = await edit_news(id, text)

        if result:
            await message.answer("Новости изменены", reply_markup=get_back_kb())
        else:
            await message.answer("Новости не изменены", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Новости не изменены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


async def edit_quiz_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает текст, отправленный администратором, и обновляет
    текст викторины с соответствующим ID.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст викторины из сообщения администратора.
    2. Получаем данные состояния, чтобы извлечь ID викторины для редактирования.
    3. Пытаемся обновить викторину в базе данных, вызывая функцию edit_quiz().
    4. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    5. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    data = await state.get_data()

    id = data.get("id", None)

    try:
        result = await edit_quiz(id, text)

        if result:
            await message.answer("Викторина изменена", reply_markup=get_back_kb())
        else:
            await message.answer("Викторина не изменена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Викторина не изменена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


async def edit_rules_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает текст, отправленный администратором, и обновляет
    текст правил.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст правил из сообщения администратора.
    2. Пытаемся обновить текст правил в базе данных, вызывая функцию edit_rules().
    3. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    4. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    5. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await edit_rules(text)

        if result:
            await message.answer("Правила изменены", reply_markup=get_back_kb())
        else:
            await message.answer("Правила не изменены", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Правила не изменены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()
