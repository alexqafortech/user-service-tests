import pytest
import requests
import time
import uuid
import psycopg2
from src.clients.categories_client import CategoriesClient
from config import Config
from src.clients.auth_client import AuthClient
from src.clients.tasks_client import TasksClient

@pytest.fixture(scope = "session")
def config():
    return Config()

@pytest.fixture(scope='session')
def api_session():
    """HTTP-сессия, используемая между тестами"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })

    yield session

    session.close()

@pytest.fixture(scope='session', autouse=True)
def check_api_available(config):
    url = f"{config.API_BASE_URL.rstrip('/')}/health"
    attempts = 20

    print(f"\nПроверяем доступность API: {url}")

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                print(f"API доступен: {url}")
                return

            print(
                f"Попытка {attempt}/{attempts}: "
                f"HTTP {response.status_code}"
            )

        except requests.exceptions.RequestException as exc:
            print(
                f"Попытка {attempt}/{attempts}: "
                f"{type(exc).__name__}: {exc}"
            )

        if attempt < attempts:
            time.sleep(3)

    pytest.exit(
        f"API недоступен после {attempts} попыток. "
        f"Проверенный URL: {url}",
        returncode=2,
    )

@pytest.fixture(scope='function')
def unique_user_data():
    """Создание уникальных данных для пользователей"""
    unique_user = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{unique_user}@example.com",
        "username": f"user_{unique_user}",
        "password": "TestPass123!"
    }

@pytest.fixture(scope = "session")
def auth_client(api_session, config):
    client_auth = AuthClient(base_url = config.API_BASE_URL, session = api_session, timeout = config.API_TIMEOUT)
    return client_auth

@pytest.fixture(scope = "session")
def tasks_client(api_session, config):
    task = TasksClient(base_url = config.API_BASE_URL, session = api_session, timeout = config.API_TIMEOUT)
    return task

@pytest.fixture(scope = "session")
def category(api_session, config):
    category = CategoriesClient(base_url = config.API_BASE_URL, session = api_session, timeout = config.API_TIMEOUT)
    return category

@pytest.fixture(scope = "session")
def user_token(auth_client, unique_user_data):
    # Получение токена пользователя для дальнейшего использования  тестах
    unique_id = uuid.uuid4().hex[:8]
    user_data = {
        "email": f"session_{unique_id}@example.com",
        "username": f"session_{unique_id}",
        "password": "TestPass123!"
    }

    res_register = auth_client.register(**user_data)
    assert res_register.status_code == 201

    res_login = auth_client.login(email=user_data["email"], password=user_data["password"])
    assert res_login.status_code == 200
    return res_login.json()["access_token"]

@pytest.fixture(scope = "function")
def authenticated_user(auth_client, unique_user_data):
    res_reg = auth_client.register(**unique_user_data)
    assert res_reg.status_code in (200, 201), f"Register failed: {res_reg.text}"

    res_log = auth_client.login(unique_user_data["username"], unique_user_data["password"])
    assert res_log.status_code == 200, f"Login failed: {res_log.text}"

    token = res_log.json()["access_token"]
    return unique_user_data, token

@pytest.fixture(scope = "function")
def authed_session(authenticated_user):
    user_data, token = authenticated_user
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    })

    yield session
    session.close()

@pytest.fixture(scope="function")
def authed_tasks_client(config, authed_session):
    return TasksClient(config.API_BASE_URL, authed_session, config.API_TIMEOUT)

@pytest.fixture(scope="function")
def authed_categories_client(config, authed_session):
    return CategoriesClient(config.API_BASE_URL, authed_session, config.API_TIMEOUT)

@pytest.fixture(scope="session")
def db_connection(config):
    """Подключение к тестовой БД. Одно на весь прогон."""
    conn = psycopg2.connect(
        host = config.DB_HOST,
        port = config.DB_PORT,
        dbname = config.DB_NAME,
        user = config.DB_USER,
        password = config.DB_PASSWORD
    )

    yield conn
    conn.close()