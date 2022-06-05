import pathlib

import pytest

from csv2http import parser

CWD = pathlib.Path.cwd()
TESTS_ROOT = pathlib.Path(__file__).parent
DATA_DIR = TESTS_ROOT / "data"

# relative path strings for all test CSV files
TEST_CSVS = [str(path.relative_to(CWD)) for path in DATA_DIR.glob("*.csv")]


@pytest.mark.parametrize("filepath", TEST_CSVS)
def test_tokenize_line(filepath):
    result = parser.tokenize_line(filepath, line_num=1, split_on=",")
    print(result)
    assert len(result) > 1
    assert open(filepath).readline().rstrip().split(",") == result


@pytest.mark.parametrize("filepath", TEST_CSVS)
def test_payload_generator(filepath):
    index = 0
    for index, result in enumerate(parser.payload_generator(filepath), start=1):
        assert isinstance(result, dict)
    assert index > 0


if __name__ == "__main__":
    pytest.main(["-vv"])
