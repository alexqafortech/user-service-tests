import pytest
from validators import is_valid_email, is_valid_password

@pytest.mark.smoke
@pytest.mark.validators
@pytest.mark.parametrize(
    "email, expected",
    [
    # Валидные
    pytest.param("alice@example.com", True, id = "valid_simple"),
    pytest.param("user.name@example.co.uk", True, id = "valid_with_dots"),
    pytest.param("a+tag@b.io", True, id = "valid_with_plus_tag"),

    # Невалидные - формат
    pytest.param("no-at-sign.com", False, id = "invalid_no_at_sign"),
    pytest.param("@example.com", False, id = "invalid_no_local_part"),
    pytest.param("alice@", False, id = "invalid_no_domain"),
    pytest.param("alice@domain", False, id = "invalid_no_tld"),

    # Невалидные - типы и пустота
    pytest.param("", False, id = "invalid_empty_string"),
    pytest.param(None, False, id = "invalid_none"),
    pytest.param(12345, False, id = "invalid_not_a_string"),
    pytest.param(
        "user@domain..com",
        False,
                id = "invalid_double_dot_in_domain_QA1234",
                marks = pytest.mark.xfail(reason = "QA-1234: двойная точка в домене не должна проходить")),
    ],
)
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected

@pytest.mark.smoke
@pytest.mark.validators
@pytest.mark.parametrize(
    "password, expected",[
    # Валидные - включая границы длины
    pytest.param("Password123", True, id = "valid_standard"),
    pytest.param("Abcdefg1", True, id = "valid_min_length_8"),
    pytest.param("A"+ "a" * 62 + "1", True, id = "valid_max_length_64"),

    # Невалидные - длина (границы с другой стороны)
    pytest.param("Abcdef1", False, id = "invalid_too_short_7"),
    pytest.param("A"+ "a" * 63 + "1", False, id = "invalid_too_long_65"),

    # Невалидные - отсутствие нужных символов
    pytest.param("NoDigitsHere", False, id = "invalid_no_digit"),
    pytest.param("nouppercase1", False, id = "invalid_no_uppercase"),
    pytest.param("NOLOWERCASE1", False, id = "invalid_no_lowercase")
    ],
)
def test_is_valid_password(password, expected):
    assert is_valid_password(password) == expected