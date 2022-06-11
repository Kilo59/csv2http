import pytest
from httpx import URL

from csv2http import cli


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://example.com", "https://example.com"),
        ("example.com", "https://example.com"),
        ("example.com/foo/bar", "https://example.com/foo/bar"),
    ],
)
def test_normalize_ulr(url, expected):
    assert URL(expected) == cli._normalize_url(url)


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://example.com", "https://example.com"),
        ("example.com", "https://example.com"),
        ("example.com/foo/bar", "https://example.com/foo/bar"),
    ],
)
def test_resolve_auth(url, expected):
    assert URL(expected) == cli._normalize_url(url)


if __name__ == "__main__":
    pytest.main(["-vv"])
