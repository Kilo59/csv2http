import argparse
import pathlib
from typing import Literal, NamedTuple

from httpx import URL

SUPPORTED_METHODS = ["POST", "PATCH", "PUT"]

CONCURRENCY_DEFAULT = 25


class Args(NamedTuple):
    file: pathlib.Path
    url: URL | str
    concurrency: int
    method: Literal["POST", "PATCH", "PUT"]
    # verbose: bool = True


def get_args() -> Args:
    parser = argparse.ArgumentParser(
        description="HTTP request for every row of a CSV file"
    )
    parser.add_argument("file", help="payload csv file", type=pathlib.Path)
    parser.add_argument("url", help="URL destination", type=URL)
    parser.add_argument(
        "-c",
        "--concurrency",
        help=f"Maxinum number of concurrent requests (default: {CONCURRENCY_DEFAULT})",
        default=CONCURRENCY_DEFAULT,
        type=int,
    )
    parser.add_argument(
        "--method",
        help="HTTP method/verb (default: POST)",
        default="POST",
        choices=SUPPORTED_METHODS,
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
        # args.verbose,
    )


if __name__ == "__main__":
    print(get_args())
