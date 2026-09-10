import pytest
from user_service import UserService

@pytest.fixture
def user_service(tmp_path):
    storage = tmp_path / "users.json"
    storage.write_text("{}")
    return UserService(storage_path = storage)

@pytest.mark.parametrize("email", [
    pytest.param("alice@example.com", id = "valid_email_1"),
    pytest.param("bob@test.org", id = "valid_email_2"),
    pytest.param("carol@domain.io", id = "valid_email_3"),
])
@pytest.mark.parametrize("password", [
    pytest.param("Password1", id = "valid_password_1"),
    pytest.param("Strong2A", id = "valid_password_2"),
    pytest.param("Valid3Pw", id = "valid_password_3"),
])
def test_all_email_password_combinations(user_service, email, password):
    user_service.register(email, password)
    assert user_service.count_users() == 1