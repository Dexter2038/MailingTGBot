from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.actions import create_user, modify_email
from app.states.user import User
from app.keyboards.user import get_back_kb
from app.utils.ask import ask_question
from app.utils.email import validate_email


router = Router(name="user_states")


@router.message(User.change_email)
async def change_email_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение, отправленное пользователем для изменения email.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Проверяем, является ли email корректным.
    2. Если email корректен, изменяем email в базе данных.
    3. Оповещаем пользователя о результате.
    4. Очищаем текущее состояние машины состояний.
    """
    if not validate_email(message.text):
        await message.answer(
            "Некорректная почта. Попробуйте еще раз.", reply_markup=get_back_kb()
        )
        await state.set_state(User.change_email)
        return

    if modify_email(message.from_user.id, message.text):
        await message.answer("Ваша почта изменена", reply_markup=get_back_kb())
    else:
        await message.answer(
            "Ваша почта не изменена. Попробуйте позже", reply_markup=get_back_kb()
        )
    await state.clear()


@router.message(User.ask_question)
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
        await message.answer("Ваш вопрос отправлен", reply_markup=get_back_kb())
    else:
        await message.answer(
            "Ваш вопрос не отправлен. Попробуйте позже", reply_markup=get_back_kb()
        )
    await state.clear()


@router.message(User.register_email)
async def register_email_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение, отправленное пользователем для регистрации email.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Проверяем, является ли email корректным.
    2. Если email корректен, сохраняем его в базе данных.
    3. Оповещаем пользователя о результате.
    4. Очищаем текущее состояние машины состояний.
    """
    if not validate_email(message.text):
        await message.answer("Некорректная почта. Попробуйте еще раз.")
        await state.set_state(User.register_email)
        return

    result = create_user(message.from_user.id, message.text, message.from_user.username)
    if not result:
        await message.answer(
            "Вы не зарегистрировались. Попробуйте ещё раз", reply_markup=get_back_kb()
        )
        return

    await message.answer("Вы успешно зарегистрировались!", reply_markup=get_back_kb())
    await state.clear()
