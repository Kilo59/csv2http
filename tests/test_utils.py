import httpx
import pytest
from respx import MockResponse

from csv2http import utils


@pytest.mark.parametrize(
    "responses",
    [
        [
            MockResponse(200),
            MockResponse(201),
            httpx.ConnectTimeout("Ooops"),
            MockResponse(201),
            httpx.ConnectError("Oh no"),
        ]
    ],
)
def test_summarize_responses(responses):
    summary = utils.summarize_responses(responses)
    print(summary)
    assert summary


if __name__ == "__main__":
    pytest.main(["-vv"])
