from user_service import User

def test_user_create_sets_email():
    user = User.create("a@b.io", "Password1")
    assert user.email == "a@b.io"

def test_user_create_hashes_password():
    user = User.create("a@b.io", "Password1")
    assert user.password_hash != "Password1"

def test_user_create_hash_is_not_empty():
    user = User.create("a@b.io", "Password1")
    assert len(user.password_hash) > 0

def test_user_check_password_correct():
    user = User.create("a@b.io", "Password1")
    assert user.check_password("Password1") is True

def test_user_check_password_wrong():
    user = User.create("a@b.io", "Password1")
    assert user.check_password("WrongPass1") is False