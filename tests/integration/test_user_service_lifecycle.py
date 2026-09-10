import pytest
from user_service import InvalidCredentialsError

@pytest.mark.smoke
@pytest.mark.storage
def test_user_service_starts_empty(user_service):
    assert user_service.count_users() == 0

@pytest.mark.smoke
@pytest.mark.auth
def test_user_service_count_increases_after_register(user_service):
    user_service.register("test@example.com", "Password1")
    assert user_service.count_users() == 1

@pytest.mark.regression
@pytest.mark.auth
def test_user_service_count_increases_for_multiple_users(user_service):
    user_service.register("test1@example.com", "Password1")
    user_service.register("test2@example.com", "Password2")
    user_service.register("test3@example.com", "Password3")
    assert user_service.count_users() == 3

@pytest.mark.smoke
@pytest.mark.auth
def test_login_with_correct_credentials_returns_user(user_service, registered_user):
    data = user_service.login(**registered_user)
    assert data.email == "alice@example.com"

@pytest.mark.regression
@pytest.mark.auth
def test_login_with_wrong_password_raises(user_service, registered_user):
    email = registered_user["email"]
    with pytest.raises(InvalidCredentialsError):
        user_service.login(email, "WrongPass1")

@pytest.mark.regression
@pytest.mark.auth
def test_login_with_nonexistent_email_raises(user_service):
    with pytest.raises(InvalidCredentialsError):
        user_service.login("ghost@example.com", "Password123")

@pytest.mark.smoke
@pytest.mark.storage
def test_get_user_returns_registered_user(user_service, registered_user):
    email = registered_user["email"]
    data = user_service.get_user(email)
    assert data.email == email

@pytest.mark.regression
@pytest.mark.storage
def test_get_user_returns_none_for_unknown_email(user_service, registered_user):
    assert user_service.get_user("ghost@example.com") is None