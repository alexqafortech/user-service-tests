import pytest
from tests.conftest import unique_user_data
from models.category import CategoryStatsResponse
from models.user import UserResponse
from models.auth import TokenResponse
from models.health import HealthResponse
from models.task import TaskResponse
from pydantic import ValidationError
from pydantic import ConfigDict

class StrictUserResponse(UserResponse):
    model_config = ConfigDict(extra="forbid")

@pytest.mark.contracts
def test_register_response_contract(auth_client, unique_user_data):
    res = auth_client.register(**unique_user_data)
    assert res.status_code == 201
    user_data = res.json()["user"]
    user = UserResponse.model_validate(user_data)

@pytest.mark.contracts
def test_login_response_contract(auth_client, unique_user_data):
    res_reg = auth_client.register(**unique_user_data)
    assert res_reg.status_code == 201
    res_login = auth_client.login(unique_user_data["username"], unique_user_data["password"])
    token = TokenResponse.model_validate(res_login.json())

@pytest.mark.contracts
def test_health_response_contract(api_session, config):
    res = api_session.get(f"{config.API_BASE_URL}/health")
    health = HealthResponse.model_validate(res.json())

@pytest.mark.contracts
def test_create_task_response_contract(authed_tasks_client, tasks_client):
    res_create_task = authed_tasks_client.create("Buy milk")
    assert res_create_task.status_code == 201

    task = TaskResponse.model_validate(res_create_task.json())
    assert task.title == "Buy milk"
    assert task.status == "TODO"

@pytest.mark.contracts
def test_task_with_invalid_status_fails_validation():
    """Модель не принимает невалидный статус."""
    with pytest.raises(ValidationError):
        TaskResponse.model_validate({
            "id": "1",
            "title": "Test",
            "status": "INVALID_STATUS",
            "priority": "HIGH",
            "user_id": "u1"
        })

@pytest.mark.contracts
def test_category_stat(authed_categories_client, category):
    payload = {"color": "#784554", "name": "Work"}
    res_create_category = authed_categories_client.create(payload)
    assert res_create_category.status_code == 201

    category_id = res_create_category.json()['id']

    res_get_category = authed_categories_client.get_stats(category_id)
    assert res_get_category.status_code == 200

    res_get_category = CategoryStatsResponse.model_validate(res_get_category.json())

@pytest.mark.contracts
def test_register_no_extra_fields(auth_client, unique_user_data):
    res = auth_client.register(**unique_user_data)
    assert res.status_code == 201
    user_json = res.json()["user"]
    StrictUserResponse.model_validate(user_json)