"""
parser.py
~~~~~~~~~

Parses CSV files and generates JSON payload from row data.

Splits up data in smaller chunks/pages.


TODO: support other input/file formats and generate form data payloads
TODO: async file IO
TODO: remove/update debugging logs
"""
import csv
import linecache
import logging
import pathlib
from typing import Generator, Iterable

from .constants import PAGE_SIZE_DEFAULT

LOGGER = logging.getLogger(__file__)


def payload_generator(
    fp: pathlib.Path, delimiter: str = ",", **reader_kwargs
) -> Generator[dict, None, None]:
    with open(fp) as file_in:
        for i, row_dict in enumerate(
            csv.DictReader(file_in, delimiter=delimiter, **reader_kwargs)
        ):
            LOGGER.info(f"{i=} - {row_dict}")
            yield row_dict


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


def tokenize_line(filepath: str | pathlib.Path, line_num: int = 1, split_on: str = ","):
    if isinstance(filepath, pathlib.Path):
        filepath = str(filepath)
    return linecache.getline(filepath, line_num).rstrip().split(split_on)
