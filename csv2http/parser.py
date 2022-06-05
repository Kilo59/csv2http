"""
parser.py
~~~~~~~~~

Parses CSV files and generates JSON payload from row data.

Splits up data in smaller chunks/pages.


TODO: support other input/file formats and generate form data payloads
TODO: async file IO
"""
import linecache
import csv
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


def tokenize_line(filepath: str | pathlib.Path, split_on: str = ","):
    filepath = pathlib.Path(filepath)
    with open(filepath, mode="r") as file_in:
        return file_in.readline().rstrip().split(split_on)
