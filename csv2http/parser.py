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
from typing import Callable, Generator, Optional

LOGGER = logging.getLogger(__file__)


def payload_generator(
    fp: pathlib.Path,
    delimiter: str = ",",
    mutator: Optional[Callable[[dict], dict]] = None,
    **reader_kwargs,
) -> Generator[dict, None, None]:
    with open(fp) as file_in:
        for i, row_dict in enumerate(
            csv.DictReader(file_in, delimiter=delimiter, **reader_kwargs)
        ):
            LOGGER.info(f"{i=} - {row_dict}")
            if mutator:
                row_dict = mutator(row_dict)
            yield row_dict


def tokenize_line(filepath: str | pathlib.Path, line_num: int = 1, split_on: str = ","):
    if isinstance(filepath, pathlib.Path):
        filepath = str(filepath)
    return linecache.getline(filepath, line_num).rstrip().split(split_on)
