import sys
import pytest

@pytest.mark.skip(reason = "Функционал ещё не реализован: восстановление пароля")
def test_password_reset_sends_email():
    """Заглушка для будущего теста - когда появится сброс пароля."""
    assert False

@pytest.mark.skipif(sys.platform == "win32", reason = "Не работает на Windows из-за path separator")
def test_unix_storage_path():
    """Пример теста, который актуален только для Unix-систем"""
    storage_path = "/tmp/users.json"
    assert "/" in storage_path

@pytest.mark.skipif(sys.version_info < (3, 10), reason = "Match-case появился в Python 3.10")
def test_python_3_10_feature():
    """Эмулируем тест на фичу новой версии Python."""
    value = "hello"
    match value:
        case "hello":
            result = True
        case _:
            result = False
    assert result is True

@pytest.mark.xfail(reason = "QA-5678: функция greet_user ещё не реализована")
def test_greet_user_returns_greeting():
    """Тест на функцию, которой ещё нет"""
    from user_service import greet_user
    assert greet_user("Alice") == "Hello, Alice!"

@pytest.mark.xfail(raises = ValueError, reason = "QA0-9012: ожидаем ValueError при пустом email")
def test_register_empty_email_raises_value_error_specifically(tmp_path):
    """Используем raises= для ожидаения конкретного исключения"""
    from user_service import UserService
    storage = tmp_path / "users.json"
    storage.write_text("{}")
    service = UserService(storage_path = storage)
    service.register("", "Password123")