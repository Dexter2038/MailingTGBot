import re


def validate_email(email: str) -> bool:
    """
    Проверяет, является ли строка корректным email адресом.

    Args:
        email: str - строка, содержащая email адрес для проверки
    Returns:
        bool: - True, если строка является корректным email адресом, False в противном случае
    """
    email_regex = re.compile(
        pattern=r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    )

    return email_regex.match(string=email)
