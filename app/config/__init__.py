from dotenv import load_dotenv
from app.database.models import init_db


def init_config() -> None:
    """
    Проверяет все необходимые для работы бота настройки:

    • База данных

    • Email сервер

    Args:
        None
    Returns:
        None
    """
    try:
        load_dotenv()
        init_db()
    except Exception as e:
        print(e)
        print("Произошла ошибка при конфигурации")
        exit(code=403)
