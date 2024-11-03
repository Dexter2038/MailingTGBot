from app.database.models import init_db
from app.utils.mailing import gmail_authenticate
from app.utils.ranks import init_rank_files


def initialize_app() -> None:
    """
    Инициализация приложения.

    Эта функция инициализирует базу данных, почтовый сервис и систему рангов.
    """
    # Инициализация системы рангов
    init_rank_files()

    # Инициализация базы данных
    init_db()

    # Инициализация почтового сервиса
    gmail_authenticate()
