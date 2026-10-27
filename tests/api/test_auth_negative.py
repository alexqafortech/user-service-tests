import pytest
import requests
from clients.tasks_client import TasksClient
import uuid


@pytest.mark.auth
@pytest.mark.negative
def test_tasks_without_auth(tasks_client):
    res = tasks_client.get_list()
    assert res.status_code == 403 # В задании прописано 401, но API возвращает 403, в Swagger так же, без токен => 403

@pytest.mark.auth
@pytest.mark.negative
def test_tasks_with_invalid_token(tasks_client, config):
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer fake_token"})

    tasks_client = TasksClient(config.API_BASE_URL, session)

    response = tasks_client.get_list()

    assert response.status_code == 401

@pytest.mark.auth
@pytest.mark.negative
def test_register_duplicate_email(auth_client, unique_user_data):
    original_data = {
        "email": unique_user_data['email'],
        "password": unique_user_data['password'],
        "username": unique_user_data['username']
    }
    duplicate_email = {
        "email": original_data['email'],
        "password": original_data['password'],
        "username": "second_name"
    }
    first_response = auth_client.register(**original_data)
    assert first_response.status_code == 201
    second_response = auth_client.register(**duplicate_email)
    assert second_response.status_code == 409

@pytest.mark.auth
@pytest.mark.negative
def test_login_wrong_password(auth_client, unique_user_data):
    user_register = {
        "email": unique_user_data['email'],
        "password": "TestPass123!",
        "username": unique_user_data['username']
    }
    user_login = {
        "email": user_register['email'],
        "password": "WrongPass1!",
        "username": user_register['username']
    }
    res_register = auth_client.register(**user_register)
    assert res_register.status_code == 201
    res_login = auth_client.login(user_login['username'], user_login['password'])
    assert res_login.status_code == 401

@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize("headers, expected", [
    pytest.param({}, (401, 403), id = "Empty header"),
    pytest.param({"Authorization": ""}, (401, 403), id = "Empty value of Authorization"),
    pytest.param({"Authorization": "Bearer"}, (401, 403), id = "Without token"),
    pytest.param({"Authorization": "Basic 2131mlaskdc"}, (401, 403), id = "Basic auth")
])
def test_auth_edge_cases(tasks_client, headers, expected):
    res = tasks_client.post(tasks_client.PREFIX + "/", json = {"title": "Edge cases"}, headers = headers)

    assert res.status_code in expected


@pytest.mark.tasks
def test_cannot_access_other_users_task(authed_tasks_client, auth_client, config, unique_user_data):
    res_create_task = authed_tasks_client.create("Buy milk")
    assert res_create_task.status_code == 201

    task_id = res_create_task.json()['id']

    uid = uuid.uuid4().hex[:8]
    data_second_user = {"email": f"user{uid}@test.com", "username": f"user{uid}", "password": "TestPass123!"}
    auth_client.register(**data_second_user)
    res_login = auth_client.login(data_second_user["username"], data_second_user["password"])
    second_token = res_login.json()["access_token"]

    second_session = requests.Session()
    second_session.headers.update({"Authorization": f"Bearer {second_token}"})
    second_user = TasksClient(config.API_BASE_URL, second_session)

    response = second_user.get_by_id(task_id)
    assert response.status_code in (403, 404)