import pytest

@pytest.mark.db
def test_register_creates_user_in_db(auth_client, unique_user_data, db):
    auth_client.register(**unique_user_data)

    user = db.get_user_by_email(unique_user_data['email'])
    assert user is not None
    assert user["username"] == unique_user_data["username"]

@pytest.mark.db
def test_create_task_appears_in_db(authed_tasks_client, db):
    task = authed_tasks_client.create("Buy milk")
    assert task.status_code == 201

    task_json = task.json()
    id_of_task = task_json["id"]

    assert db.get_task_by_id(id_of_task)
    assert db.get_task_by_id(id_of_task)["title"] == "Buy milk"
    assert db.get_task_by_id(id_of_task)["status"] == "TODO"

@pytest.mark.db
def test_delete_task_removes_from_db(authed_tasks_client, db):
    task = authed_tasks_client.create("Buy milk")
    assert task.status_code == 201

    task_json = task.json()
    id_of_task = task_json["id"]

    authed_tasks_client.delete(id_of_task)
    assert db.get_task_by_id(id_of_task) is None

@pytest.mark.db
def test_update_task_changes_db(authed_tasks_client, db):
    task = authed_tasks_client.create("Buy milk")
    assert task.status_code == 201

    task_json = task.json()
    id_of_task = task_json["id"]

    payload = {"title": "Buy water"}

    update = authed_tasks_client.update(id_of_task, **payload)
    assert update.status_code == 200

    assert db.get_task_by_id(id_of_task)["title"] == "Buy water"

@pytest.mark.db
def test_keys(auth_client, authed_tasks_client, authenticated_user, db):
    user_data, token = authenticated_user

    db_user = db.get_user_by_email(user_data['email'])
    assert db_user is not None
    user_id_from_db = db_user["id"]

    res_task = authed_tasks_client.create("Buy milk")
    assert res_task.status_code == 201

    task_id = res_task.json()["id"]

    db_task = db.get_task_by_id(task_id)
    assert db_task is not None

    assert db_task["user_id"] == user_id_from_db
