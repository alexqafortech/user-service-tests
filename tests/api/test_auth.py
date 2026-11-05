import pytest
import allure
from tests.conftest import unique_user_data
from models.auth import TokenResponse, RegisterPayload
from models.error import ErrorResponse
from models.user import UserResponse
# Коммент для проверки PR
@pytest.fixture
def url_register():
    return "/api/v1/auth/register"

@pytest.fixture
def url_login():
    return "/api/v1/auth/login"

@allure.title("Регистрация нового пользователя")
@allure.epic("Task Management API")
@allure.feature("Authentication")
@allure.story("Валидная регистрация с уникальными данными, проверяется статус код ответа и совпадение"
              " входного email и email созданного аккаунта")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "regression", "auth")
@pytest.mark.auth
def test_register_new_user(auth_client, unique_user_data):
    with allure.step("Зарегистрировать пользователя"):
        res = auth_client.register(**unique_user_data)

    with allure.step("Проверка статус кода ответа на запрос на регистрацию"):
        assert res.status_code == 201

    with allure.step("Получение тела ответа"):
        res_data = UserResponse.model_validate(res.json()["user"])

    with allure.step("Проверка, что полученный email совпадает с посылаемым"):
        assert res_data.email == unique_user_data['email']

@allure.title("Логин в существующий аккаунт")
@allure.epic("Task Management API")
@allure.feature("Authentication")
@allure.story("Регистрируется пользователь с уникальными данными, выполняется вход в аккаунт, "
              "проверка, что используется именно bearer токен")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "regression", "auth")
@pytest.mark.auth
def test_login_success(auth_client, unique_user_data):
    with allure.step("Регистрация пользователя"):
        res_register = auth_client.register(**unique_user_data)
        assert res_register.status_code == 201

    with allure.step("Вход в аккаунт"):
        res_login = auth_client.login(unique_user_data['username'], unique_user_data['password'])

    with allure.step("Получение токена из ответа на запрос на логин"):
        token = TokenResponse.model_validate(res_login.json())

    with allure.step("Проверка типа токена"):
        assert token.token_type == "bearer"

@allure.title("Вход в несуществующий аккаунт")
@allure.epic("Task Management API")
@allure.feature("Authentication")
@allure.story("Выполняется вход в аккаунт с случайными username и password")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("api", "smoke", "regression", "auth")
@pytest.mark.negative
def test_login_nonexistent_user(auth_client, unique_user_data):
    res_login = auth_client.login(unique_user_data['username'], unique_user_data['password'])
    assert res_login.status_code == 401

@allure.title("Разные виды ошибок в формате запроса на регистрацию")
@allure.epic("Task Management API")
@allure.feature("Authentication")
@allure.story("Проверка ошибок в формате запроса на регистрацию: пустое значение email, "
              "ошибка в формате email, нет поля username, нет поля password, пустой запрос")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "regression", "auth")
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
    with allure.step("Регистрация пользователя"):
        res = auth_client.register(**user)
    with allure.step("Проверка совпадения ожидаемого статус кода и фактического"):
        assert res.status_code == expected_status_code, f"Payload: {user}, получили {res.status_code}"

    with allure.step("Получение тела ответа"):
        error = ErrorResponse.model_validate(res.json())
    with allure.step("Проверка, что ошибка в ответе не пустая"):
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
