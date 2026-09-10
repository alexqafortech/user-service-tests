from validators import is_valid_email, is_valid_password

def test_email_valid_simple():
    assert is_valid_email("alice@example.com") is True

def test_email_valid_with_dots():
    assert is_valid_email("user.name@example.co.uk") is True

def test_email_valid_with_plus():
    assert is_valid_email("a+tag@b.io") is True

def test_email_invalid_no_at_sign():
    assert is_valid_email("no-at-sign.com") is False

def test_email_invalid_no_local_part():
    assert is_valid_email("@example.com") is False

def test_email_invalid_no_domain():
    assert is_valid_email("alice@") is False

def test_email_invalid_no_tld():
    assert is_valid_email("alice@domain") is False

def test_email_invalid_empty_string():
    assert is_valid_email("") is False

def test_email_invalid_none():
    assert is_valid_email(None) is False

def test_email_invalid_not_a_string():
    assert is_valid_email(12345) is False

def test_password_valid_standard():
    assert is_valid_password("Password123") is True

def test_password_valid_minimum_length():
    assert is_valid_password("Abcdefg1") is True

def test_password_invalid_too_short():
    assert is_valid_password("Abc123") is False

def test_password_invalid_too_long():
    assert is_valid_password("A"*65) is False

def test_password_invalid_no_digit():
    assert is_valid_password("NoDigitsHere") is False

def test_password_invalid_no_uppercase():
    assert is_valid_password("nouppercase1") is False

def test_password_invalid_no_lowercase():
    assert is_valid_password("NOLOWERCASE1") is False

def test_password_invalid_empty():
    assert is_valid_password("") is False