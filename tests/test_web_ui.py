"""
Automated Verification Suite for Web UI Dashboard and Documentation Endpoints.
"""

import pytest
from src.app import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_web_ui_dashboard_index(client):
    """Verify that root / serves the interactive HTML Web UI."""
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.content_type
    html = res.get_data(as_text=True)
    assert "LabManager" in html
    assert "My Academic Classes" in html
    assert "Deadline Calendar" in html
    assert "System Audit Log" in html

def test_system_logs_endpoint(client):
    """Verify that /api/v1/system/logs returns recent log records."""
    res = client.get("/api/v1/system/logs")
    assert res.status_code == 200
    data = res.get_json()
    assert "lines" in data
    assert isinstance(data["lines"], list)

def test_openapi_spec_endpoint(client):
    """Verify that /api/v1/spec serves the active OpenAPI JSON contract."""
    res = client.get("/api/v1/spec")
    assert res.status_code == 200
    assert "application/json" in res.content_type
    spec = res.get_json()
    assert "openapi" in spec
    assert "paths" in spec
    assert "/classes" in spec["paths"]
