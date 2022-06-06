"""
core.py
~~~~~~~
"""
import asyncio
import logging
import pathlib
from typing import Counter, Generator, Iterable, Literal

import httpx

from csv2http import cli, parser
from csv2http.constants import PAGE_SIZE_DEFAULT

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


def response_details(response: httpx.Response, verbose: bool = False) -> str:
    """Returns a string details of the response and the original request."""
    # TODO: prettyprint json
    result = f"{response.request.method} {response.request.url} -> {response}"
    if verbose:
        result += (
            f"\n  headers - {dict(response.headers)}"
            + f"\n  content - {response.content.decode()}"
        )
    return result


def summarize_responses(responses: list[httpx.Response]) -> str:
    """Returns count of all response status codes sorted by status code"""
    # TODO: make this pretty, display as table with running tally of previous responses
    counter = Counter([r.status_code for r in responses])
    # TODO: maybe don't bother sorting this
    sorted_dict = dict(sorted(counter.items(), key=lambda item: item[0]))
    return f"status codes - {sorted_dict}"


# supported http methods
Methods = Literal["POST", "PUT", "PATCH"]


async def parrelelize_requests(
    method: Methods,
    path: str | httpx.URL,
    request_kwarg_list: list[dict],
    client_session: httpx.AsyncClient,
) -> list[httpx.Response]:
    """Parreleize multiple HTTP requests with asyncio.gather."""

    tasks = []
    for request_kwargs in request_kwarg_list:
        tasks.append(client_session.request(method, path, **request_kwargs))

    LOGGER.debug(f"{method} {path} - parrelelizing {len(request_kwarg_list)} requests")

    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses


async def execute(args: cli.Args) -> int:
    """Make http requests given a CSV file and user arguments."""
    file_input = pathlib.Path(args.file)
    assert file_input.exists(), f"could not find {file_input.absolute()}"

    total_requests = 0

    async with httpx.AsyncClient() as client_session:

        print(f" {args.method} {args.url}")

        for paylod_batch in chunker(
            parser.csv_payload_generator(file_input), chunk_size=args.concurrency
        ):

            responses = await parrelelize_requests(
                args.method,
                args.url,
                [{"json": p} for p in paylod_batch],
                client_session,
            )
            total_requests += len(responses)
            print(f"  {summarize_responses(responses)}")

    return total_requests


def main():
    """csv2http script entrypoint."""
    user_args = cli.get_args()
    asyncio.run(execute(user_args))


if __name__ == "__main__":
    main()
