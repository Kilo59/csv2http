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
    "auth_input,expected",
    [
        ("foo bar", ("foo", "bar")),
        # this probably invalid auth but not responsiblity of _resolve_auth
        ("foo bar bazz", ("foo", "bar bazz")),
        ("fizz", ("fizz", "fake_input")),
    ],
)
def test_resolve_auth(monkeypatch, auth_input, expected):
    monkeypatch.setattr(cli, "_get_input", lambda x: "fake_input", raising=True)

    assert expected == cli._resolve_auth(auth_input)


if __name__ == "__main__":
    pytest.main(["-vv"])
