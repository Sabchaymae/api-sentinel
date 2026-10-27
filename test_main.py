
from datetime import datetime, timezone
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from main import app

client = TestClient(app, raise_server_exceptions=False)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "message": "API Sentinel is running",
    }


@patch("main.SessionLocal")
def test_monitor_history(mock_session_local):
    mock_db = mock_session_local.return_value.__enter__.return_value
    mock_db.scalars.return_value.all.return_value = []

    response = client.get("/monitor/history")

    assert response.status_code == 200
    assert response.json() == {
        "total_checks": 0,
        "history": [],
    }


@patch("main.detect_incident", return_value=None)
@patch("main.check_api")
@patch("main.SessionLocal")
def test_monitor_check_success(
    mock_session_local,
    mock_check_api,
    mock_detect_incident,
):
    mock_check_api.return_value = {
        "url": "https://example.com",
        "status_code": 200,
        "response_time_ms": 120.5,
        "is_available": True,
        "error": None,
    }

    mock_db = mock_session_local.return_value.__enter__.return_value

    def fake_refresh(item):
        item.id = 123
        item.checked_at = datetime.now(timezone.utc)

    mock_db.refresh.side_effect = fake_refresh

    response = client.get(
        "/monitor/check",
        params={"url": "https://example.com"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 123
    assert data["url"] == "https://example.com"
    assert data["status_code"] == 200
    assert data["is_available"] is True
    assert data["error"] is None

    mock_db.add.assert_called_once()
    mock_db.flush.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_detect_incident.assert_called_once()


@patch(
    "main.detect_incident",
    return_value={
        "url": "https://example.com",
        "status_code": 500,
        "error": "HTTP error: 500",
        "incident_type": "API_UNAVAILABLE",
    },
)
@patch("main.check_api")
@patch("main.SessionLocal")
def test_monitor_check_server_error(
    mock_session_local,
    mock_check_api,
    mock_detect_incident,
):
    mock_check_api.return_value = {
        "url": "https://example.com",
        "status_code": 500,
        "response_time_ms": 90.0,
        "is_available": False,
        "error": "HTTP error: 500",
    }

    mock_db = mock_session_local.return_value.__enter__.return_value

    def fake_refresh(item):
        item.id = 124
        item.checked_at = datetime.now(timezone.utc)

    mock_db.refresh.side_effect = fake_refresh

    response = client.get(
        "/monitor/check",
        params={"url": "https://example.com"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 124
    assert data["status_code"] == 500
    assert data["is_available"] is False
    assert data["error"] == "HTTP error: 500"

    assert mock_db.add.call_count == 2
    mock_db.flush.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_detect_incident.assert_called_once()


def test_monitor_check_missing_url():
    response = client.get("/monitor/check")

    assert response.status_code == 422


@patch("main.detect_incident", return_value=None)
@patch("main.check_api")
@patch("main.SessionLocal")
def test_monitor_check_database_error(
    mock_session_local,
    mock_check_api,
    mock_detect_incident,
):
    mock_check_api.return_value = {
        "url": "https://example.com",
        "status_code": 200,
        "response_time_ms": 100.0,
        "is_available": True,
        "error": None,
    }

    mock_db = mock_session_local.return_value.__enter__.return_value
    mock_db.flush.side_effect = SQLAlchemyError("Database unavailable")

    response = client.get(
        "/monitor/check",
        params={"url": "https://example.com"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Failed to save monitoring result to database"
    }


@patch("main.SessionLocal")
def test_get_incidents_empty(mock_session_local):
    mock_db = mock_session_local.return_value.__enter__.return_value
    mock_db.scalars.return_value.all.return_value = []

    response = client.get("/incidents")

    assert response.status_code == 200
    assert response.json() == {
        "total_incidents": 0,
        "incidents": [],
    }


@patch("main.SessionLocal")
def test_get_incidents_with_data(mock_session_local):
    mock_db = mock_session_local.return_value.__enter__.return_value

    incident = type("FakeIncident", (), {})()
    incident.id = 7
    incident.url = "https://example.com"
    incident.status_code = 500
    incident.error = "HTTP error: 500"
    incident.incident_type = "API_UNAVAILABLE"
    incident.detected_at = datetime(
        2026, 10, 27, 12, 0, tzinfo=timezone.utc
    )

    mock_db.scalars.return_value.all.return_value = [incident]

    response = client.get("/incidents")

    assert response.status_code == 200
    data = response.json()

    assert data["total_incidents"] == 1
    assert data["incidents"][0]["id"] == 7
    assert data["incidents"][0]["url"] == "https://example.com"
    assert data["incidents"][0]["status_code"] == 500
    assert data["incidents"][0]["incident_type"] == "API_UNAVAILABLE"


@patch("main.SessionLocal")
def test_get_incidents_database_error(mock_session_local):
    mock_db = mock_session_local.return_value.__enter__.return_value
    mock_db.scalars.side_effect = SQLAlchemyError("Database unavailable")

    response = client.get("/incidents")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Failed to retrieve incidents"
    }


@patch("main.SessionLocal")
def test_monitor_history_database_error(mock_session_local):
    mock_db = mock_session_local.return_value.__enter__.return_value
    mock_db.scalars.side_effect = SQLAlchemyError("Database unavailable")

    response = client.get("/monitor/history")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Failed to retrieve monitoring history"
    }
