import pytest
from models.health import HealthResponse

@pytest.mark.smoke
def test_health_status_code(api_session, config):
    res = api_session.get(f"{config.API_BASE_URL}/health")
    assert res.status_code == 200

@pytest.mark.smoke
def test_health_response_body(api_session, config):
    res = api_session.get(f"{config.API_BASE_URL}/health")
    res_json = res.json()
    assert "status" in res_json
    status = res_json["status"]
    assert isinstance(status, str)

@pytest.mark.smoke
def test_health_response_headers(api_session, config):
    res = api_session.get(f"{config.API_BASE_URL}/health")
    assert "application/json" in res.headers["content-type"]

@pytest.mark.smoke
def test_health_response_time(api_session, config):
    res = api_session.get(f"{config.API_BASE_URL}/health")
    assert res.elapsed.total_seconds() < 1

@pytest.mark.smoke
def test_health_response_schema(api_session, config):
    response = api_session.get(f"{config.API_BASE_URL}/health")
    health = HealthResponse.model_validate(response.json())
    assert health.status == "healthy"

