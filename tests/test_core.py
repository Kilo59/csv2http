import httpx
import pytest

from csv2http import cli, core


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


def test_file_to_wire(http_reflect, csv_payload_generator_param_fxt):
    payload = next(csv_payload_generator_param_fxt)

    response = httpx.post("http://example.com/foobar", json=payload)
    print(core.response_details(response, verbose=True))

    assert http_reflect.calls.call_count == 1
    assert payload == response.json()


@pytest.mark.asyncio
async def test_parrelelize_requests(http_reflect, csv_payload_generator_param_fxt):
    payload_1 = next(csv_payload_generator_param_fxt)
    payload_2 = next(csv_payload_generator_param_fxt)
    payload_3 = next(csv_payload_generator_param_fxt)
    payloads = [payload_1, payload_2, payload_3]

    async with httpx.AsyncClient() as client:
        responses = await core.parrelelize_requests(
            "POST", "http://example.com/foo", [{"json": p} for p in payloads], client
        )

    assert http_reflect.calls.call_count == len(payloads)
    assert len(responses) == len(payloads)

    for payload, response in zip(payloads, responses):
        assert payload == response.json()


@pytest.mark.asyncio
async def test_main(http_reflect_random_status, sample_csv):

    total = await core.main(
        cli.Args(
            sample_csv,
            "http://example.com",
            concurrency=50,
            method="PATCH",
            # verbose=True,
        )
    )

    assert http_reflect_random_status.calls.call_count == total
    assert False


if __name__ == "__main__":
    pytest.main(["-vv"])
