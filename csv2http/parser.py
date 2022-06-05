"""
parser.py
~~~~~~~~~

Parses CSV files and generates JSON payload from row data.

Splits up data in smaller chunks/pages.


TODO: support other input/file formats and generate form data payloads
TODO: async file IO
"""
import csv
import logging
import pathlib
from typing import Generator, Iterable

from .constants import PAGE_SIZE_DEFAULT

LOGGER = logging.getLogger(__file__)


def payload_generator(fp: pathlib.Path) -> Generator[dict, None, None]:
    yield {"foo": "bar"}
    yield {"fizz": "buzz"}
    yield {"thunder": "flash"}


def chunker(
    input_iterator: Iterable[dict], chunk_size: int = PAGE_SIZE_DEFAULT
) -> Generator[list[dict], None, None]:
    """Takes"""
    chunk = []
    for i, data in enumerate(input_iterator):
        LOGGER.warning(f"{i=} {data=}")
        chunk.append(data)
        if len(chunk) == chunk_size:
            yield chunk
            chunk.clear()

    if chunk:  # yield the leftovers
        yield chunk
