"""
Модуль валидации пользовательских данных.

Содержит чистые функции валидации email и пароля.
Чистые — значит без побочных эффектов: ничего не пишут, не читают,
не печатают. Только принимают вход и возвращают True/False
или бросают понятное исключение.
"""

import re


# Регулярка для email: что-то@что-то.что-то
# Не идеальная (идеальная регулярка для email — это легенда),
# но покрывает 99% реальных кейсов.
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 64


def is_valid_email(email: str) -> bool:
    """
    Проверяет, что email соответствует формату.

    Возвращает True, если формат корректный, иначе False.
    Не бросает исключений — только возвращает булево.
    """
    if not isinstance(email, str):
        return False
    if not email:
        return False
    return bool(EMAIL_PATTERN.match(email))


def is_valid_password(password: str) -> bool:
    """
    Проверяет, что пароль соответствует требованиям:
    - длина от 8 до 64 символов
    - есть хотя бы одна цифра
    - есть хотя бы одна заглавная буква
    - есть хотя бы одна строчная буква

    Спецсимволы не требуем — это упрощённая версия для учебного проекта.
    """
    if not isinstance(password, str):
        return False
    if not (MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH):
        return False
    if not any(ch.isdigit() for ch in password):
        return False
    if not any(ch.isupper() for ch in password):
        return False
    if not any(ch.islower() for ch in password):
        return False
    return True


def validate_registration_data(email: str, password: str) -> None:
    """
    Валидирует данные при регистрации.

    В отличие от is_valid_*, эта функция бросает исключение,
    если данные невалидны — потому что регистрация без валидных
    данных просто не должна состояться.

    Бросает:
        ValueError — если email или пароль невалидны.
    """
    if not is_valid_email(email):
        raise ValueError(f"Невалидный email: {email!r}")
    if not is_valid_password(password):
        raise ValueError(
            "Пароль должен быть от 8 до 64 символов, "
            "содержать цифру, заглавную и строчную буквы"
        )
