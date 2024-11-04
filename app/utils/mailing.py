from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from os import environ
import os.path
from typing import Any, Dict, List, Tuple

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from google.auth.external_account_authorized_user import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.database.actions import add_confirm, get_all_emails_and_ids
from app.keyboards.user import get_confirm_mailing_kb

# При изменении удалить файл token.json.
SCOPES: List[str] = ["https://mail.google.com/"]


def init_mailing() -> None:
    """
    Инициализирует credentials.json и token.json.
    """
    gmail_authenticate()


def gmail_authenticate() -> Any:
    """
    Авторизирует пользователя по OAuth 2.0.

    Returns:
      Service: Авторизированный сервис Gmail API.

    Raises:
      HttpError: Если произошла ошибка при подключении к сервису Gmail API.
    """
    creds = None
    # Файл token.json содержит доступные ключи доступа и обновления,
    # и создается автоматически при первом запуске авторизационного цикла.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Если нет доступных учетных данных, попросите пользователя войти.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(request=Request())
        else:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file="credentials.json", scopes=SCOPES
            )
            creds: Credentials = flow.run_local_server(port=0)
        # Сохраняем данные для следующего запуска
        with open(file="token.json", mode="w") as token:
            token.write(creds.to_json())

    try:
        # Получаем клиент Gmail API
        service = build(serviceName="gmail", version="v1", credentials=creds)
        return service

    except HttpError as e:
        print(e)
        print("Не получилось авторизовать GMAIL API клиент")
        exit(code=403)


def build_message(destination, title, body) -> Dict[str, str]:
    """
    Функция создает сообщение электронной почты на основе
    переданных destination, title, body.

    Args:
        destination (str or List[str]): адрес(а) электронной почты
            получателя(-ей).
        title (str): тема сообщения.
        body (str): текст сообщения.

    Returns:
        dict: словарь с полем raw, содержащим закодированное в base64
        сообщение.
    """
    message = MIMEText(body)
    message["to"] = (
        ", ".join(destination) if isinstance(destination, list) else destination
    )
    message["from"] = environ["MAIL_USERNAME"]
    message["subject"] = title
    return {"raw": urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(destination, title, body) -> Any:
    """
    Отправляет сообщение на адрес(а) destination
    с темой title и текстом body.

    Args:
        service (Any): авторизированный сервис Gmail API.
        destination (str or List[str]): адрес(а) электронной почты
            получателя(-ей).
        title (str): тема сообщения.
        body (str): текст сообщения.

    Returns:
        dict: словарь с информацией о отправленном сообщении.
    """

    service = gmail_authenticate()
    return (
        service.users()
        .messages()
        .send(userId="me", body=build_message(destination, title, body))
        .execute()
    )


async def make_mailing(text: str, bot: Bot) -> bool:
    """
    Отправляет сообщение с текстом text
    всем пользователям, у которых есть email.

    Args:
        text (str): текст сообщения.
        bot (Bot): объект бота, который отправляет сообщение.

    Returns:
        bool: флаг успешности отправки.
    """
    try:
        data: List[Tuple[str, int]] = get_all_emails_and_ids()

        emails, ids = zip(*data)

        emails = list(emails)

        for id in ids:
            await bot.send_message(id, text)

        if len(text) > 125:
            title = text[:125]
        else:
            title = text

        send_message(emails, title, text)

        return True

    except Exception as e:
        print("Не получилось отправить сообщение всем пользователям")
        return False


async def make_confirm_mailing(text: str, bot: Bot) -> bool:
    """
    Отправляет сообщение с текстом text
    всем пользователям, у которых есть email.

    Args:
        text (str): текст сообщения.
        bot (Bot): объект бота, который отправляет сообщение.

    Returns:
        bool: флаг успешности отправки.
    """
    try:
        data: List[Tuple[str, int]] = get_all_emails_and_ids()

        emails, ids = zip(*data)

        emails = list(emails)

        mailing_id: int = add_confirm(text)

        kb: InlineKeyboardMarkup = get_confirm_mailing_kb(mailing_id)

        for id in ids:
            await bot.send_message(id, text, reply_markup=kb)

        if len(text) > 125:
            title: str = text[:122] + "..."
        else:
            title: str = text

        send_message(emails, title, text)

        return True

    except Exception as e:
        print("Не получилось отправить сообщение всем пользователям")
        return False
