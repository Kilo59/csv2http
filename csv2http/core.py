import logging
from typing import Generator, Iterable

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
