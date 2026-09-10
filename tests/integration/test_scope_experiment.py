import pytest
from user_service import UserService

@pytest.fixture(scope="function")
def user_service_shared(tmp_path):
    """ОПАСНЫЙ ПРИМЕР: session-scope для изменяемой фикстуры."""
    storage = tmp_path / "users.json"
    storage.write_text("{}")
    return UserService(storage_path = storage)

def test_a_starts_empty(user_service_shared):
    assert user_service_shared.count_users() == 0

def test_b_registers_alcie(user_service_shared):
    user_service_shared.register("alice@example.com", "Password123")
    assert user_service_shared.count_users() == 1

def test_c_storage_is_empty_again(user_service_shared):
    assert user_service_shared.count_users() == 0