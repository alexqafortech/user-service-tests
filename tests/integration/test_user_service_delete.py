import pytest
from user_service import UserNotFoundError

@pytest.mark.smoke
@pytest.mark.storage
def test_delete_existing_user_removes_from_storage(user_service, registered_user):
    user_service.delete_user(registered_user["email"])
    assert user_service.count_users() == 0

@pytest.mark.regression
@pytest.mark.storage
def test_delete_existing_user_makes_get_return_none(user_service, registered_user):
    user_service.delete_user(registered_user["email"])
    assert user_service.get_user(registered_user["email"]) == None

@pytest.mark.regression
@pytest.mark.storage
def test_delete_nonexistent_user_rises(user_service):
    with pytest.raises(UserNotFoundError):
        user_service.delete_user("ghost@example.com")

@pytest.mark.regression
@pytest.mark.storage
def test_delete_one_user_keeps_other(user_service, registered_user):
    user_service.register("user2@example.com", "Password123")
    user_service.register("user3@example.com", "Password123")
    user_service.delete_user("user2@example.com")
    assert user_service.count_users() == 2