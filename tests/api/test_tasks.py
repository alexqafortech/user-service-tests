import pytest
import allure
from models.task import TaskResponse, TaskListResponse

@allure.title("Создание задачи")
@allure.epic("Task Management API")
@allure.feature("Tasks")
@allure.story("Создание задачи, проверка статус кода ответа, проверка что название задачи совпадает с "
                "переданным, проверка что статус задач совпадает с ожидаемым")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "smoke", "regression", "tasks")
@pytest.mark.tasks
def test_create_task(authed_tasks_client):
    res_create_task = authed_tasks_client.create("Buy milk")
    assert res_create_task.status_code == 201
    task = TaskResponse.model_validate(res_create_task.json())
    assert task.title == "Buy milk"
    assert task.status == "TODO"

@allure.title("Получение существующей задачи по id")
@allure.epic("Task Management API")
@allure.feature("Tasks")
@allure.story("Получение задачи по id, проверка совпадения названия задачи, и статуса задачи")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "smoke", "regression", "tasks")
@pytest.mark.tasks
def test_get_task_by_id(authed_tasks_client):
    res_create_task = authed_tasks_client.create("Buy milk")
    task_id = res_create_task.json()['id']

    res_get_task = authed_tasks_client.get_by_id(task_id)
    assert res_get_task.status_code == 200
    task = TaskResponse.model_validate(res_get_task.json())
    assert task.title == "Buy milk"
    assert task.status == "TODO"

@pytest.mark.tasks
def test_get_tasks_list(authed_tasks_client):
    res_create_first_task = authed_tasks_client.create("test1")
    res_create_second_task = authed_tasks_client.create("test2")

    res_list = authed_tasks_client.get_list()
    assert res_list.status_code == 200

    task_list = TaskListResponse.model_validate(res_list.json())

    assert task_list.total >= 2
    assert len(task_list.items) <= task_list.page_size

@pytest.mark.tasks
def test_delete_task(authed_tasks_client):
    res_create_task = authed_tasks_client.create("test1")
    task_id = res_create_task.json()['id']

    res_delete_task = authed_tasks_client.delete(task_id)

    res_get_task = authed_tasks_client.get_by_id(task_id)
    assert res_get_task.status_code == 404




