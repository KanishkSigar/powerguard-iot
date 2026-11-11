"""PowerGuard IoT — API Versioning & Semver Negotiation Tests"""
import re
import pytest

def parse_semver(version_str: str) -> tuple:
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", version_str.strip())
    if not match:
        raise ValueError(f"Invalid semver: {version_str}")
    return tuple(int(x) for x in match.groups())

def is_compatible_api_version(client_version: str, server_version: str = "1.4.0") -> bool:
    client_major, client_minor, _ = parse_semver(client_version)
    server_major, server_minor, _ = parse_semver(server_version)
    return client_major == server_major and client_minor <= server_minor

def test_semver_parsing():
    assert parse_semver("v1.4.0") == (1, 4, 0)
    assert parse_semver("2.0.1") == (2, 0, 1)
    with pytest.raises(ValueError):
        parse_semver("invalid.version")

def test_api_compatibility():
    assert is_compatible_api_version("1.2.0", "1.4.0") is True
    assert is_compatible_api_version("1.4.0", "1.4.0") is True
    assert is_compatible_api_version("2.0.0", "1.4.0") is False
    assert is_compatible_api_version("1.5.0", "1.4.0") is False