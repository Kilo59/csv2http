import asyncio
import logging
from typing import Generator, Iterable, Literal

import httpx

from .constants import PAGE_SIZE_DEFAULT

LOGGER = logging.getLogger(__file__)


def chunker(
    input_iterator: Iterable[dict], chunk_size: int = PAGE_SIZE_DEFAULT
) -> Generator[list[dict], None, None]:
    """Works through an iterator in chunks."""
    chunk = []
    for i, data in enumerate(input_iterator):
        LOGGER.warning(f"{i=} {data=}")
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


# supported http methods
Methods = Literal["POST", "PUT", "PATCH"]


async def parrelelize_requests(
    method: Methods,
    path: str,
    request_kwarg_list: list[dict],
    client_session: httpx.AsyncClient,
) -> list[httpx.Response]:

    tasks = []
    for request_kwargs in request_kwarg_list:
        tasks.append(client_session.request(method, path, **request_kwargs))

    LOGGER.info(f"parrelelizing {len(request_kwarg_list)} requests")

    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses
