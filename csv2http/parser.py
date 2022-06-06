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
from typing import Callable, Generator, Optional, Union

LOGGER = logging.getLogger(__file__)


def csv_payload_generator(
    filepath: pathlib.Path,
    delimiter: str = ",",
    mutator: Optional[Callable[[dict], dict]] = None,
    **reader_kwargs,
) -> Generator[dict, None, None]:
    """
    Yields rows from a CSV as dictionaries.
    Optionaly mutate the row first by providing a `Callable` (function).
    """

    with open(filepath, encoding="utf-8") as file_in:
        for i, row_dict in enumerate(
            csv.DictReader(file_in, delimiter=delimiter, **reader_kwargs)
        ):
            LOGGER.debug(f"{i=} - {row_dict}")
            if mutator:
                row_dict = mutator(row_dict)
            yield row_dict


def tokenize_line(
    filepath: Union[str, pathlib.Path], line_num: int = 1, split_on: str = ","
):
    """Split strings on a given line number."""
    if isinstance(filepath, pathlib.Path):
        filepath = str(filepath)
    return linecache.getline(filepath, line_num).rstrip().split(split_on)
