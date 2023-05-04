import pytest

from anakonda.anakonda import apiv1_bp
from anakonda.util import uuidgen

API_URL_PREFIX = apiv1_bp.url_prefix
API_REQUEST_HEADERS = {"Content-Type": "application/json"}


@pytest.mark.order(1000)
def test_get_tasks(client):
    response = client.get(f"{API_URL_PREFIX}/tasks", headers=API_REQUEST_HEADERS)
    result = response.get_json()
    assert response.status_code == 200
    assert len(result["result"]) == 1
    assert result["status"]["code"] == 100


@pytest.mark.parametrize(
    ["task_id", "status", "code", "headers"],
    (
        ["random", 404, 107, True],
        ["storage:test", 200, 100, True],
        ["random", 400, 105, False],
    ),
)
@pytest.mark.order(1000)
def test_get_task(storage, app, client, task_id, status, code, headers):
    if task_id == "random":
        task_id = uuidgen()
    if task_id.startswith("storage:") is True:
        task_id = storage.get(task_id.split(":")[1])
    response = client.get(
        f"{API_URL_PREFIX}/tasks/{task_id}",
        headers=API_REQUEST_HEADERS if headers else {},
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code


@pytest.mark.parametrize(
    ["data", "status", "code"],
    (
        ["", 400, 102],
        [{}, 400, 102],
        [{"name": "test", "namespace": "test"}, 400, 102],
        [
            {
                "name": "ANAKONDATESTRESOURCEINVALIDINPUTDATA",
                "namespace": "test",
                "runtime": "docker",
                "image": "alpine:latest",
                "script": "id",
            },
            400,
            104,
        ],
        [
            {
                "name": "test",
                "namespace": "ANAKONDATESTRESOURCEINVALIDINPUTDATA",
                "runtime": "kubernetes",
                "image": "alpine:latest",
                "script": "id",
            },
            400,
            104,
        ],
        [
            {
                "name": "test",
                "namespace": "test",
                "runtime": "invalid",
                "image": "alpine:latest",
                "script": "id",
            },
            400,
            108,
        ],
        [
            {
                "name": "test",
                "namespace": "test",
                "runtime": "kubernetes",
                "image": "alpine:latest",
                "script": "id",
            },
            201,
            100,
        ],
    ),
)
@pytest.mark.order(1000)
def test_create_task(storage, client, data, status, code):
    response = client.post(
        f"{API_URL_PREFIX}/tasks",
        json=data,
        headers=API_REQUEST_HEADERS,
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code
    if response.status_code == 201:
        assert result["result"]["status"] == "new"
        assert result["result"]["last_update_at"] is None
        storage.set("temp", result["result"]["id"])


@pytest.mark.parametrize(
    ["task_id", "data", "status", "code"],
    (
        ["random", "", 400, 102],
        ["random", {}, 404, 107],
        ["storage:test", {}, 400, 109],
        ["storage:temp", {}, 200, 100],
        ["storage:temp", {"runtime": "invalid"}, 400, 108],
        ["storage:temp", {"runtime": "docker"}, 200, 100],
        [
            "random",
            {
                "name": "ANAKONDATESTRESOURCEINVALIDINPUTDATA",
                "namespace": "test",
                "runtime": "docker",
                "image": "alpine:latest",
                "script": "id",
            },
            400,
            104,
        ],
        [
            "random",
            {
                "name": "test",
                "namespace": "ANAKONDATESTRESOURCEINVALIDINPUTDATA",
                "runtime": "kubernetes",
                "image": "alpine:latest",
                "script": "id",
            },
            400,
            104,
        ],
        [
            "random",
            {
                "name": "test",
                "namespace": "test",
                "runtime": "invalid",
                "image": "alpine:latest",
                "script": "id",
            },
            400,
            108,
        ],
    ),
)
@pytest.mark.order(1000)
def test_update_task(storage, client, task_id, data, status, code):
    if task_id == "random":
        task_id = uuidgen()
    if task_id.startswith("storage:") is True:
        task_id = storage.get(task_id.split(":")[1])
    response = client.patch(
        f"{API_URL_PREFIX}/tasks/{task_id}",
        json=data,
        headers=API_REQUEST_HEADERS,
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code


@pytest.mark.parametrize(
    ["task_id", "status", "code"],
    (
        ["random", 404, 107],
        ["storage:temp", 200, 100],
    ),
)
@pytest.mark.order(1000)
def test_delete_task(storage, client, task_id, status, code):
    if task_id == "random":
        task_id = uuidgen()
    if task_id.startswith("storage:") is True:
        task_id = storage.get(task_id.split(":")[1])
    response = client.delete(
        f"{API_URL_PREFIX}/tasks/{task_id}",
        headers=API_REQUEST_HEADERS,
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code
