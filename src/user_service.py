"""
Модуль сервиса работы с пользователями.

Учебный проект для курса AQA на Python. Содержит:
- класс User — представление пользователя
- класс UserService — операции регистрации, логина, поиска, удаления
- кастомные исключения для разных ситуаций
- хранилище в JSON-файле (путь передаётся в конструктор)
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from validators import validate_registration_data


# ---------- Исключения ----------
# Свои классы исключений — хорошая практика. Сразу видно, что произошло,
# и в тестах можно проверить именно нужный тип ошибки через pytest.raises.

class UserServiceError(Exception):
    """Базовое исключение для всех ошибок сервиса."""
    pass


class UserAlreadyExistsError(UserServiceError):
    """Пользователь с таким email уже зарегистрирован."""
    pass


class UserNotFoundError(UserServiceError):
    """Пользователь с таким email не найден."""
    pass


class InvalidCredentialsError(UserServiceError):
    """Неверный email или пароль при попытке логина."""
    pass


# ---------- Модель пользователя ----------

@dataclass
class User:
    """
    Представление пользователя.

    Пароль хранится в виде хеша, а не в открытом виде.
    Хешируем sha256 — это упрощённый вариант для учебного проекта.
    В реальном проекте используют bcrypt/argon2 с солью.
    """
    email: str
    password_hash: str

    @classmethod
    def create(cls, email: str, password: str) -> "User":
        """Создать пользователя из email и пароля в открытом виде."""
        return cls(email=email, password_hash=cls._hash_password(password))

    def check_password(self, password: str) -> bool:
        """Проверить, что переданный пароль совпадает с сохранённым."""
        return self.password_hash == self._hash_password(password)

    @staticmethod
    def _hash_password(password: str) -> str:
        """Превращает пароль в hex-строку sha256."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------- Сервис ----------

class UserService:
    """
    Сервис работы с пользователями.

    Хранит данные в JSON-файле. Путь к файлу передаётся при создании
    сервиса — это удобно для тестов: в каждом тесте можно дать свой
    временный файл, и тесты не будут мешать друг другу.

    Пример использования:
        service = UserService(storage_path="users.json")
        service.register("alice@example.com", "Password123")
        user = service.login("alice@example.com", "Password123")
    """

    def __init__(self, storage_path: str | Path):
        self.storage_path = Path(storage_path)
        # Если файла нет — создадим пустой
        if not self.storage_path.exists():
            self._save_users({})

    # ---------- Публичные методы ----------

    def register(self, email: str, password: str) -> User:
        """
        Зарегистрировать нового пользователя.

        Бросает:
            ValueError — если email или пароль невалидны
            UserAlreadyExistsError — если такой email уже зарегистрирован
        """
        validate_registration_data(email, password)

        users = self._load_users()
        if email in users:
            raise UserAlreadyExistsError(
                f"Пользователь с email {email!r} уже существует"
            )

        user = User.create(email=email, password=password)
        users[email] = asdict(user)
        self._save_users(users)
        return user

    def login(self, email: str, password: str) -> User:
        """
        Аутентифицировать пользователя.

        Возвращает объект User, если email и пароль верные.

        Бросает:
            InvalidCredentialsError — если email не найден ИЛИ пароль неверный
                (намеренно одно исключение на оба случая — это безопаснее:
                злоумышленник не узнает, существует email в системе или нет).
        """
        user = self.get_user(email)
        if user is None or not user.check_password(password):
            raise InvalidCredentialsError("Неверный email или пароль")
        return user

    def get_user(self, email: str) -> Optional[User]:
        """
        Получить пользователя по email.

        Возвращает User или None, если пользователь не найден.
        В отличие от login, не бросает исключение — это просто запрос.
        """
        users = self._load_users()
        data = users.get(email)
        if data is None:
            return None
        return User(**data)

    def delete_user(self, email: str) -> None:
        """
        Удалить пользователя.

        Бросает:
            UserNotFoundError — если такого пользователя нет
        """
        users = self._load_users()
        if email not in users:
            raise UserNotFoundError(
                f"Пользователь с email {email!r} не найден"
            )
        del users[email]
        self._save_users(users)

    def count_users(self) -> int:
        """Вернуть количество зарегистрированных пользователей."""
        return len(self._load_users())

    # ---------- Внутренние методы ----------

    def _load_users(self) -> dict:
        """Прочитать всех пользователей из JSON-файла."""
        with open(self.storage_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_users(self, users: dict) -> None:
        """Записать пользователей в JSON-файл."""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
