import os
import pytest

def get_max_password_length():
    """Читает максимальную длину пароля из переменной окружения."""
    return int(os.environ.get("MAX_PASSWORD_LENGHT", "64"))

def test_default_max_password_length():
    assert get_max_password_length() == 64

def test_max_password_length_from_env(monkeypatch):
    monkeypatch.setenv("MAX_PASSWORD_LENGHT", "128")
    assert get_max_password_length() == 128

def test_max_password_length_isolated_between_tests():
    assert get_max_password_length() == 64