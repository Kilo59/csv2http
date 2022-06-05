import pathlib

import httpx
import pytest

from csv2http.http import response_details

TESTS_ROOT = pathlib.Path(__file__).parent
DATA_DIR = TESTS_ROOT / "data"


def test_file_to_wire(http_reflect):
    response = httpx.post("http://example.com/foobar", json={"foo": "bar"})
    print(response_details(response, verbose=True))

    assert False
