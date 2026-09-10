import pytest

@pytest.mark.regression
@pytest.mark.auth
def test_register_with_invalid_email_raises_value_error(user_service):
    with pytest.raises(ValueError):
        user_service.register("not-an-email", "Password123")

@pytest.mark.regression
@pytest.mark.auth
def test_register_with_short_password_raises_value_error(user_service):
    with pytest.raises(ValueError):
        user_service.register("alice@example.com", "abc")