import pytest
from user_service import UserService, UserNotFoundError

@pytest.fixture
def user_service(tmp_path):
    storage = tmp_path / "users.json"
    storage.write_text("{}")
    service = UserService(storage_path = storage)

    yield service

    if storage.exists():
        storage.write_text("{}")

@pytest.fixture
def registered_user(user_service):
    email = "alice@example.com"
    password = "Password123"
    user_service.register(email, password)
    return {"email": email, "password": password}

def test_delete_existing_user_removes_from_storage(user_service, registered_user):
    user_service.delete_user(registered_user["email"])
    assert user_service.count_users() == 0

def test_delete_existing_user_makes_get_return_none(user_service, registered_user):
    user_service.delete_user(registered_user["email"])
    assert user_service.get_user(registered_user["email"]) == None

def test_delete_nonexistent_user_rises(user_service):
    with pytest.raises(UserNotFoundError):
        user_service.delete_user("ghost@example.com")

def test_delete_one_user_keeps_other(user_service, registered_user):
    user_service.register("user2@example.com", "Password123")
    user_service.register("user3@example.com", "Password123")
    user_service.delete_user("user2@example.com")
    assert user_service.count_users() == 2