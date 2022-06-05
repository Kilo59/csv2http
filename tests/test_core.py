import pathlib

import httpx
import pytest

from csv2http import http, parser

CWD = pathlib.Path.cwd()
TESTS_ROOT = pathlib.Path(__file__).parent
DATA_DIR = TESTS_ROOT / "data"

# relative path strings for all test CSV files
TEST_CSVS = [str(path.relative_to(CWD)) for path in DATA_DIR.glob("*.csv")]


@pytest.mark.parametrize("filepath", TEST_CSVS)
def test_file_to_wire(http_reflect, filepath):
    payload = next(parser.payload_generator(filepath))

    response = httpx.post("http://example.com/foobar", json=payload)
    print(http.response_details(response, verbose=True))

    assert payload == response.json()
