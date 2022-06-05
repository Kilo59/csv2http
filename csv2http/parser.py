import pathlib
import csv
from typing import Generator


def payload_generator(fp: pathlib.Path) -> Generator[dict, None, None]:
    yield {"foo": "bar"}
