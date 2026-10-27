def detect_incident(check_result: dict) -> dict | None:
    if check_result["is_available"]:
        return None

    return {
        "url": check_result["url"],
        "status_code": check_result["status_code"],
        "error": check_result["error"],
        "incident_type": "API_UNAVAILABLE",
    }