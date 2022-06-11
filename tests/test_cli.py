import base64
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
        ("foo:bar", ("foo", "bar")),
        ("foo=bar", ("foo", "bar")),
        ("fizz", ("fizz", "fake_input")),
        ("nopassword:", ("nopassword", "")),
        ("nopassword=", ("nopassword", "")),
        # also not valid
        ("", ("", "fake_input")),
    ],
)
def test_resolve_auth(monkeypatch, auth_input, expected):
    monkeypatch.setattr(cli, "_get_input", lambda x: "fake_input", raising=True)

    assert expected == cli._resolve_auth(auth_input)


@pytest.mark.parametrize(
    "headers_input,expected",
    [
        ("foo:bar", ("foo", "bar")),
        ("foo=bar", ("foo", "bar")),
        (
            # ensure base64 padding is not removed
            f"foo={base64.standard_b64encode(b'bar64').decode('utf-8')}",
            ("foo", base64.standard_b64encode(b"bar64").decode("utf-8")),
        ),
    ],
)
def test_pase_header(headers_input, expected):
    assert expected == cli._parse_header(headers_input)


@pytest.mark.parametrize(
    "args,expected",
    [
        # minimal example
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
        ),
        (
            [
                "myfile.csv",
                "example.com",
                "-H",
                "x-foo:bar",
                "fizz=buzz",
                "-c",
                "23",
                "--auth",
                "bigetti:password",
            ],
            {
                "auth": ("bigetti", "password"),
                "concurrency": 23,
                "file": pathlib.Path("myfile.csv"),
                "form_data": False,
                "header": [("x-foo", "bar"), ("fizz", "buzz")],
                "method": "POST",
                "no_save": False,
                "url": URL("https://example.com"),
            },
        ),
    ],
)
def test_get_args(args, expected):
    parser = cli._bootstrap_parser()

    assert expected == vars(parser.parse_args(args))


if __name__ == "__main__":
    pytest.main(["-vv"])
