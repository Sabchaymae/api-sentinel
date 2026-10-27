
from unittest.mock import Mock, patch

import httpx

from monitor import check_api


@patch("monitor.httpx.get")
def test_check_api_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.is_success = True
    mock_get.return_value = mock_response

    result = check_api("https://example.com")

    assert result["status_code"] == 200
    assert result["is_available"] is True
    assert result["error"] is None


@patch("monitor.httpx.get")
def test_check_api_server_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.is_success = False
    mock_get.return_value = mock_response

    result = check_api("https://example.com")

    assert result["status_code"] == 500
    assert result["is_available"] is False
    assert result["error"] == "HTTP error: 500"


@patch("monitor.httpx.get")
def test_check_api_timeout(mock_get):
    mock_get.side_effect = httpx.TimeoutException("Timeout")

    result = check_api("https://example.com")

    assert result["status_code"] is None
    assert result["is_available"] is False
    assert result["error"] == "Request timed out"

@patch("monitor.httpx.get")
def test_check_api_network_error(mock_get):
    mock_get.side_effect = httpx.ConnectError(
        "Connection failed"
    )

    result = check_api("https://example.com")

    assert result["status_code"] is None
    assert result["is_available"] is False
    assert result["error"] == "Connection failed"
