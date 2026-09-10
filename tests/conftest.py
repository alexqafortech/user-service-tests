"""
Корневой conftest для всех тестов.

Добавляет директорию src/ в sys.path, чтобы тесты могли
импортировать модули как 'from user_service import ...'
без указания полного пути.
"""

import sys
from pathlib import Path



# Добавляем src/ в sys.path
SRC_DIR = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

import pytest

@pytest.fixture
def valid_credentials():
    """Эталонные валидные данные для регистрации."""
    return {"email": "alice@example.com", "password": "Password123"}