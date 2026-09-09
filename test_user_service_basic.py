import pytest
from user_service import UserService

@pytest.fixture
def user_service(tmp_path):
    storage = tmp_path / "users.json"
    storage.write_text("{}")
    return UserService(storage_path = storage)

def test_register_with_invalid_email_raises_value_error(user_service):
    with pytest.raises(ValueError):
        user_service.register("not-an-email", "Password123")

def test_register_with_short_password_raises_value_error(user_service):
    with pytest.raises(ValueError):
        user_service.register("alice@example.com", "abc")