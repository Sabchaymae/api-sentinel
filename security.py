
import ipaddress
import socket
from urllib.parse import urlparse


def validate_public_url(url: str) -> str:
    """Validate an HTTP(S) URL and reject local/private destinations."""
    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise ValueError("Invalid URL") from exc

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed")

    hostname = parsed.hostname.lower().rstrip(".")

    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("Local URLs are not allowed")

    if hostname.endswith(".local"):
        raise ValueError("Local network URLs are not allowed")

    try:
        addresses = {ipaddress.ip_address(hostname)}
    except ValueError:
        try:
            resolved = socket.getaddrinfo(
                hostname,
                parsed.port or (443 if parsed.scheme == "https" else 80),
                type=socket.SOCK_STREAM,
            )
        except (socket.gaierror, OSError):
            raise ValueError("Hostname cannot be resolved")

        addresses = {
            ipaddress.ip_address(item[4][0])
            for item in resolved
        }

    if not addresses:
        raise ValueError("Hostname has no valid IP address")

    for address in addresses:
        if (
            not address.is_global
            or address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_multicast
            or address.is_reserved
            or address.is_unspecified
        ):
            raise ValueError("Private or non-public IP addresses are not allowed")

    return url
