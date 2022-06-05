import pathlib

import pytest

from csv2http import parser

CWD = pathlib.Path.cwd()
TESTS_ROOT = pathlib.Path(__file__).parent
DATA_DIR = TESTS_ROOT / "data"

# relative path strings for all test CSV files
TEST_CSVS = [str(path.relative_to(CWD)) for path in DATA_DIR.glob("*.csv")]


@pytest.mark.parametrize("filepath", TEST_CSVS)
def test_payload_generator(filepath):
    index = 0
    for index, result in enumerate(parser.payload_generator(filepath), start=1):
        assert isinstance(result, dict)
    assert index > 0


def test_chunker_chunk_size():
    input_iterator = [{"a": "alpha"}, {"b": "bravo"}, {"c": "charlie"}]

    chunk_size = 2
    chunker_gen = parser.chunker(input_iterator, chunk_size=chunk_size)

    first_result = next(chunker_gen)
    print(f"{first_result=}")
    assert len(first_result) == chunk_size

    last_result = next(chunker_gen)
    print(f"{last_result=}")
    assert len(last_result) == len(input_iterator) - chunk_size


if __name__ == "__main__":
    pytest.main(["-vv"])
