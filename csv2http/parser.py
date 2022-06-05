import csv
import pathlib
from typing import Generator


def payload_generator(fp: pathlib.Path) -> Generator[dict, None, None]:
    yield {"foo": "bar"}
