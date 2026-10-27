
import pytest

from security import validate_public_url


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "https://httpbin.org/status/500",
    ],
)
def test_validate_public_url_accepts_public_urls(url, monkeypatch):
    import socket

    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443))
        ],
    )

    assert validate_public_url(url) == url


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://example.com",
        "http://localhost",
        "http://127.0.0.1",
        "http://192.168.1.1",
        "http://10.0.0.1",
        "http://169.254.169.254",
        "http://router.local",
        "http://user:password@example.com",
    ],
)
def test_validate_public_url_rejects_unsafe_urls(url):
    with pytest.raises(ValueError):
        validate_public_url(url)


def test_validate_public_url_rejects_unresolvable_hostname(monkeypatch):
    import socket

    def fail_resolution(*args, **kwargs):
        raise socket.gaierror("Hostname not found")

    monkeypatch.setattr(socket, "getaddrinfo", fail_resolution)

    with pytest.raises(ValueError, match="cannot be resolved"):
        validate_public_url("https://unknown.invalid")
