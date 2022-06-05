import httpx
import pytest

from csv2http import core, http


def test_chunker_chunk_size():
    input_iterator = [{"a": "alpha"}, {"b": "bravo"}, {"c": "charlie"}]

    chunk_size = 2
    chunker_gen = core.chunker(input_iterator, chunk_size=chunk_size)

    first_result = next(chunker_gen)
    print(f"{first_result=}")
    assert len(first_result) == chunk_size

    last_result = next(chunker_gen)
    print(f"{last_result=}")
    assert len(last_result) == len(input_iterator) - chunk_size


def test_file_to_wire(http_reflect, payload_generator_param_fxt):
    payload = next(payload_generator_param_fxt)

    response = httpx.post("http://example.com/foobar", json=payload)
    print(http.response_details(response, verbose=True))

    assert http_reflect.calls.call_count == 1
    assert payload == response.json()


if __name__ == "__main__":
    pytest.main(["-vv"])
