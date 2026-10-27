
import time

import httpx


def check_api(url: str) -> dict:
    start_time = time.perf_counter()

    try:
        response = httpx.get(url, timeout=5.0)

        response_time = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        is_available = response.is_success

        if not is_available:
            error = f"HTTP error: {response.status_code}"
        else:
            error = None

        return {
            "url": url,
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "is_available": is_available,
            "error": error,
        }

    except httpx.TimeoutException:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": round(
                (time.perf_counter() - start_time) * 1000, 2
            ),
            "is_available": False,
            "error": "Request timed out",
        }

    except httpx.RequestError as exc:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": round(
                (time.perf_counter() - start_time) * 1000, 2
            ),
            "is_available": False,
            "error": str(exc),
        }
