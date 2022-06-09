"""
core.py
~~~~~~~
"""
import asyncio
import logging
import pathlib
from typing import Generator, Iterable, Literal, Union

import httpx

from csv2http import cli, parser
from csv2http.constants import PAGE_SIZE_DEFAULT
from csv2http.utils import (
    _add_timestamp_and_suffix,
    append_responses,
    dump_crash_log,
    summarize_responses,
)

LOGGER = logging.getLogger(__file__)

# pylint: disable=fixme


def chunker(
    input_iterator: Iterable[dict], chunk_size: int = PAGE_SIZE_DEFAULT
) -> Generator[list[dict], None, None]:
    """Works through an iterator and returns batches based on `chunk_size`."""
    chunk = []
    for data in input_iterator:
        chunk.append(data)

        if len(chunk) == chunk_size:
            yield chunk
            chunk.clear()

    if chunk:  # yield the leftovers
        yield chunk


# supported http methods
Methods = Literal["POST", "PUT", "PATCH"]


async def parrelelize_requests(
    method: Methods,
    path: Union[str, httpx.URL],
    # TODO: create type for request_kwargs
    request_kwarg_list: list[dict],
    client_session: httpx.AsyncClient,
) -> list[httpx.Response]:
    """
    Parreleize multiple HTTP requests with asyncio.gather.

    Parameters
    ----------
    method
        HTTP verb to use POST, PUT, PATCH.
    path
        Absolute or relative URL path.
    request_kwarg_list
        List of keyword arguments to pass to `httpx.request()`. Each object becomes an
        independent request and async task.
    client_session
        Active AsyncClient instance session.

    Returns
    -------
    list[httpx.Response]
        List of HTTP response objects.
    """

    tasks = [
        client_session.request(method, path, **request_kwargs)
        for request_kwargs in request_kwarg_list
    ]

    LOGGER.debug(f"{method} {path} - parrelelizing {len(request_kwarg_list)} requests")

    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses


async def execute(args: cli.Args) -> int:
    """Make http requests given a CSV file and user arguments."""
    file_input = pathlib.Path(args.file)
    assert file_input.exists(), f"could not find {file_input.absolute()}"

    total_requests = 0

    content = "data" if args.form_data else "json"
    log_file = _add_timestamp_and_suffix(file_input, "log")

    async with httpx.AsyncClient() as client_session:

        print(f" {args.method} {args.url}")

        for paylod_batch in chunker(
            parser.csv_payload_generator(file_input), chunk_size=args.concurrency
        ):

            responses = await parrelelize_requests(
                args.method,
                args.url,
                [{content: p} for p in paylod_batch],
                client_session,
            )
            total_requests += len(responses)
            print(f"  {summarize_responses(responses)}")
            if args.save_log:
                append_responses(log_file, responses)

    if args.save_log:
        print(f"log file -> {log_file.absolute()}")

    return total_requests


def main():
    """csv2http script entrypoint."""
    user_args = cli.get_args()
    try:
        asyncio.run(execute(user_args))
    except KeyboardInterrupt:
        print("KeyboardInterrupt stopping...")
    except Exception as exc:  # pylint: disable=broad-except
        crash_log_path = _add_timestamp_and_suffix(user_args.file, "crash.log")
        print(
            exc.__class__.__name__
            + f" check crash log - {dump_crash_log(crash_log_path, exc)}",
        )


if __name__ == "__main__":
    main()
