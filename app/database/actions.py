from typing import List, Tuple
from mysql.connector import connect, Error
from os import environ


def create_user(id: int, email: str, username: str) -> bool:
    """
    Создает пользователя с id и email

    Args:
        id: int - id пользователя
        email: str - email
    Returns:
        bool: True, если пользователь успешно создан, False - в противном случае
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                INSERT INTO users (id, email, username) VALUES (%s, %s, %s);
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (id, email, username))
            connection.commit()
            return True
    except Error as e:
        print(e)
        print("Не получилось добавить пользователя с id =", id, "email =", email)
        return False


def modify_email(id: int, new_email: str) -> bool:
    """
    Изменяет email пользователя с id

    Args:
        id (int): id пользователя.
        new_email (str): новый email.

    Returns:
        bool: True, если email успешно изменен, False - в противном случае.
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                UPDATE users SET email = %s WHERE id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (new_email, id))
            connection.commit()
            return True
    except Error as e:
        print(e)
        print(
            "Не получилось изменить email пользователя с id =", id, "email =", new_email
        )
        return False


def get_email_by_id(id: int) -> str:
    """
    Возвращает email пользователя с id

    Args:
        id: int - id пользователя
    Returns:
        str: email пользователя
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT email FROM users WHERE id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                return cursor.fetchone()[0]
    except Error as e:
        print(e)
        print("Не получилось получить email пользователя с id =", id)
        return ""


def get_all_emails_and_ids() -> List[Tuple[str, int]]:
    """
    Возвращает список email-ов всех пользователей
    или пустый список в случае ошибки

    Пример:
    [(email1, id1), (email2, id2), ...]

    Returns:
        List[Tuple[str, int]]: - список email-ов всех пользователей
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT email, id FROM users;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Error as e:
        print(e)
        print("Не получилось получить email всех пользователей")
        return []


def is_user_registered(id: int) -> bool:
    """
    Проверяет, зарегистрирован ли пользователь

    Args:
        id: int - id пользователя
    Returns:
        bool: True, если пользователь зарегистрирован, False - в противном случае
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT id FROM users WHERE id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                return cursor.fetchone() is not None
    except Error as e:
        print(e)
        print("Не получилось проверить наличие пользователя с id =", id)
        return False


def add_confirm(text: str) -> int:
    """
    Добавляет рассылку с подтверждением

    Args:
        text: str - текст рассылки

    Returns:
        int: id добавленной рассылки или 0 в случае ошибки
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                INSERT INTO confirms (text) VALUES (%s);
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (text[:125] + "...",))
                connection.commit()
                return cursor.lastrowid
    except Error as e:
        print(e)
        print("Не получилось добавить рассылку с подтверждением")
        return 0


def get_all_confirms() -> List[Tuple[int, str]]:
    """
    Возвращает все рассылки

    Returns:
        List[str]: все рассылки
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT id, text FROM confirms;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Error as e:
        print(e)
        print("Не получилось получить рассылки с подтверждением")
        return []


def add_confirm_user_mailing(user_id, mailing_id):
    """
    Добавляет подтверждение рассылки пользователю

    Args:
        user_id: int - id пользователя
        mailing_id: int - id рассылки
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                INSERT INTO users_confirms (user_id, confirm_id) VALUES (%s, %s);
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, mailing_id))
                connection.commit()
    except Error as e:
        print(e)
        print("Не получилось добавить подтверждение рассылки пользователю")


def end_confirm(id: int) -> bool:
    """
    Завершает рассылку с подтверждением

    Args:
        id: int - id рассылки
    Returns:
        bool: True, если рассылка завершена, False - в противном случае
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                DELETE FROM confirms WHERE id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                connection.commit()
                return True
    except Error as e:
        print(e)
        print("Не получилось завершить рассылку с подтверждением")
        return False


def get_confirm_users(id: int) -> List[Tuple[int, str]]:
    """
    Возвращает информацию о подтвержденных пользователях

    Args:
        id: int - id рассылки
    Returns:
        List[Tuple[int, str]]: тг id и username каждого пользователя, подтвердившего id конкурса
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT user.id, user.username 
                FROM users_confirms AS confirmation 
                JOIN users AS user ON user.id = confirmation.user_id
                WHERE confirmation.confirm_id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                return cursor.fetchall()
    except Error as e:
        print(e)
        print("Не получилось получить подтвержденных пользователей")
        return []
