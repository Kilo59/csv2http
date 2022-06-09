"""
cli.py
~~~~~~
"""
import argparse
import pathlib
from typing import Literal, NamedTuple, Union

from httpx import URL

from csv2http._version import __version__

SUPPORTED_METHODS = ["POST", "PATCH", "PUT"]

CONCURRENCY_DEFAULT = 25


def _normalize_url(value: Union[str, URL]) -> URL:
    """Add scheme to url string if it's missing."""
    url = URL(value)
    if not url.scheme:
        url = URL(f"https://{url}")
    return url


class Args(NamedTuple):
    """Expected user Args."""

    file: pathlib.Path
    url: Union[URL, str]
    concurrency: int
    method: Literal["POST", "PATCH", "PUT"]
    form_data: bool = False
    save_log: bool = True
    # verbose: bool = True


def get_args() -> Args:
    """Get user args from the command line."""
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
    # parser.add_argument(
    #     "-v", "--verbose", help="verbose stdout logging", default=False, type=bool
    # )

    args = parser.parse_args()
    return Args(
        args.file,
        args.url,
        args.concurrency,
        args.method,
        args.form_data,
        not args.no_save
        # args.verbose,
    )


if __name__ == "__main__":
    print(get_args())
