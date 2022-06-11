import pathlib

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
        # also not valid
        ("", ("", "fake_input")),
    ],
)
def test_resolve_auth(monkeypatch, auth_input, expected):
    monkeypatch.setattr(cli, "_get_input", lambda x: "fake_input", raising=True)

    assert expected == cli._resolve_auth(auth_input)


@pytest.mark.parametrize(
    "headers_input",
    [
        "foo:bar",
        "foo=bar",
        "foo bar",
    ],
)
def test_pase_header(headers_input):

    assert ("foo", "bar") == cli._parse_header(headers_input)


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            ["myfile.csv", "example.com"],
            {
                "auth": None,
                "concurrency": cli.CONCURRENCY_DEFAULT,
                "file": pathlib.Path("myfile.csv"),
                "form_data": False,
                "header": None,
                "method": "POST",
                "no_save": False,
                "url": URL("https://example.com"),
            },
        )
    ],
)
def test_get_args(args, expected):
    parser = cli._bootstrap_parser()

    assert expected == vars(parser.parse_args(args))


if __name__ == "__main__":
    pytest.main(["-vv"])
