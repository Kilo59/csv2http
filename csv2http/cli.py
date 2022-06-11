"""
cli.py
~~~~~~
"""
import argparse
import pathlib
import re
from typing import Literal, NamedTuple, Optional, Union

from httpx import URL, Headers

from csv2http._version import __version__

SUPPORTED_METHODS = ["POST", "PATCH", "PUT"]
CONCURRENCY_DEFAULT = 25
TIMEOUT_DEFAULT = 5

_SPLIT_REGEX = r"[:=]"


def _get_input(prompt: str):
    return input(prompt)


def _normalize_url(value: Union[str, URL]) -> URL:
    """Add scheme to url string if it's missing."""
    url = URL(value)
    if not url.scheme:
        url = URL(f"https://{url}")
    return url


def _resolve_auth(value: str) -> Union[tuple[str, str], tuple[None, None]]:
    """
    Parse username & password. Prompt for password if not provided.
    """
    username, *extras = re.split(_SPLIT_REGEX, value, maxsplit=1)
    password = " ".join(extras) if extras else _get_input("password:")
    return username, password


def _parse_header(value: str) -> tuple[str, str]:
    """Splits string on `:` or `=` and returns a tuple of key, value."""
    key, value = re.split(_SPLIT_REGEX, value, maxsplit=1)
    return key, value


def _bootstrap_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"HTTP request for every row of a CSV file - v{__version__}"
    )
    parser.add_argument("file", help="payload csv file", type=pathlib.Path)
    parser.add_argument(
        "url",
        help="URL destination - called with `http` if scheme is absent",
        type=_normalize_url,
    )
    parser.add_argument(
        "-c",
        "--concurrency",
        help=f"Maximum number of concurrent requests (default: {CONCURRENCY_DEFAULT})",
        default=CONCURRENCY_DEFAULT,
        type=int,
    )
    parser.add_argument(
        "--method",
        help="HTTP method/verb (default: POST)",
        default="POST",
        choices=SUPPORTED_METHODS,
    )
    parser.add_argument(
        "-a",
        "--auth",
        help="Basic Authentication enter <USERNAME>:<PASSWORD>."
        " If password is blank you will be prompted for input",
        type=_resolve_auth,
    )
    parser.add_argument(
        "-H", "--header", help="Header `key:value` pairs", nargs="*", type=_parse_header
    )
    parser.add_argument(
        "-d",
        "--form-data",
        help="Send payload as form encoded data instead of JSON (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--no-save",
        help="Do not save results to log file (default: false)",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help=f"Connection timeout of each request in seconds (default: {TIMEOUT_DEFAULT})",
        default=TIMEOUT_DEFAULT,
        type=int,
    )
    # parser.add_argument(
    #     "-v",
    #     "--verbose",
    #     help="verbose stdout logging",
    #     action="store_true",
    # )
    return parser


class Args(NamedTuple):
    """Expected user Args."""

    file: pathlib.Path
    url: Union[URL, str]
    concurrency: int
    method: Literal["POST", "PATCH", "PUT"]
    auth: Optional[tuple[str, str]] = None
    headers: Optional[Headers] = None
    form_data: bool = False
    save_log: bool = True
    timeout: int = TIMEOUT_DEFAULT
    # verbose: bool = False


_PARSER = _bootstrap_parser()


def get_args() -> Args:
    """Get user args from the command line."""
    args = _PARSER.parse_args()
    return Args(
        args.file,
        args.url,
        args.concurrency,
        args.method,
        args.auth,
        Headers(args.header),
        args.form_data,
        not args.no_save,
        args.timeout,
        # args.verbose,
    )


if __name__ == "__main__":
    print(get_args())
