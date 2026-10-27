import pytest
from tests.conftest import unique_user_data
from models.auth import TokenResponse, RegisterPayload
from models.error import ErrorResponse
from models.user import UserResponse

@pytest.fixture
def url_register():
    return "/api/v1/auth/register"

@pytest.fixture
def url_login():
    return "/api/v1/auth/login"

@pytest.mark.auth
def test_register_new_user(auth_client, unique_user_data):
    res = auth_client.register(**unique_user_data)
    assert res.status_code == 201
    res_data = UserResponse.model_validate(res.json()["user"])
    assert res_data.email == unique_user_data['email']

@pytest.mark.auth
def test_login_success(auth_client, unique_user_data):
    res_register = auth_client.register(**unique_user_data)
    assert res_register.status_code == 201

    res_login = auth_client.login(unique_user_data['username'], unique_user_data['password'])

    token = TokenResponse.model_validate(res_login.json())
    assert token.token_type == "bearer"

@pytest.mark.negative
def test_login_nonexistent_user(auth_client, unique_user_data):
    res_login = auth_client.login(unique_user_data['username'], unique_user_data['password'])
    assert res_login.status_code == 401

@pytest.mark.negative
@pytest.mark.parametrize("user, expected_status_code",[
    pytest.param(
      {
          "email": "",
          "password": "TestPass123!",
          "username": "TestUser"
      },
      422,
      id = "empty_email"
    ),
    pytest.param(
        {
          "email": "not-an-email",
          "password": "TestPass123!",
          "username": "TestUser"
        },
        422,
        id = "invalid_email"
    ),
    pytest.param(
        {
          "email": "test@example.com",
          "password": "TestPass123!",
        },
        422,
        id = "missing_username"
    ),
    pytest.param(
        {
            "email": "test@example.com",
            "username": "TestUser"
        },
        422,
        id = "missing_password"
    ),
    pytest.param(
        {},
        422,
        id = "empty_body"
    )
])
def test_register_validation(user, expected_status_code, auth_client):
    res = auth_client.register(**user)
    assert res.status_code == expected_status_code, f"Payload: {user}, получили {res.status_code}"

    error = ErrorResponse.model_validate(res.json())
    assert error.detail

@pytest.mark.auth
def test_register_with_model(auth_client, unique_user_data):
    payload = RegisterPayload(
        email = unique_user_data['email'],
        username = unique_user_data['username'],
        password = "ValidPass123!"
    )
    response = auth_client.register(**payload.model_dump())
    assert response.status_code in (200, 201)
