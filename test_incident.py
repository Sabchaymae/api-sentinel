from incident import detect_incident


def test_detect_incident_when_api_is_available():
    check_result = {
        "url": "https://example.com",
        "status_code": 200,
        "response_time_ms": 120.0,
        "is_available": True,
        "error": None,
    }

    result = detect_incident(check_result)

    assert result is None


def test_detect_incident_when_api_is_unavailable():
    check_result = {
        "url": "https://example.com",
        "status_code": 500,
        "response_time_ms": 100.0,
        "is_available": False,
        "error": "HTTP error: 500",
    }

    result = detect_incident(check_result)

    assert result == {
        "url": "https://example.com",
        "status_code": 500,
        "error": "HTTP error: 500",
        "incident_type": "API_UNAVAILABLE",
    }