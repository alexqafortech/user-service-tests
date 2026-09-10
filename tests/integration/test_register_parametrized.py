import pytest

@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.parametrize(
    "email, password",
    [
        pytest.param("alice@example.com", "Password123", id = "standard"),
        pytest.param("user.name@b.co.uk", "ValidPass1", id = "with_dots"),
        pytest.param("a+tag@b.io", "MinLength1", id = "with_plus_tag"),
        pytest.param("a@b.cc", "Abcdefg1", id = "short_email_min_pass"),
    ],
)
def test_register_with_valid_data_creates_user(user_service, email, password):
    user_service.register(email, password)
    assert user_service.count_users() == 1

@pytest.mark.regression
@pytest.mark.auth
@pytest.mark.parametrize(
    "email, password",
    [
        pytest.param("not-an-email", "Password123", id = "invalid_email"),
        pytest.param("alice@example.com", "short", id = "too_short_password"),
        pytest.param("alice@example.com", "nouppercase1", id = "no_uppercase"),
        pytest.param("alice@example.com", "NOLOWERCASE1", id = "no_lowercase"),
        pytest.param("alice@example.com", "NoDigitsHere", id = "no_digit"),
        pytest.param("", "Password123", id = "empty_email"),
    ],
)
def test_register_with_invalid_data_raises(user_service, email, password):
    with pytest.raises(ValueError):
        user_service.register(email, password)