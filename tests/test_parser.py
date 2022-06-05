import pathlib

import pytest

from csv2http import parser

TEST_ROOT = pathlib.Path(__file__, "..")
DATA_DIR = TEST_ROOT / "data"


@pytest.mark.parametrize("filepath", ["/data/simple.csv", "/data/simple1K.csv"])
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
    pytest.main(["--vv"])
