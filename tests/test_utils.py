import ast

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
    assert summary

    _, status_codes = summary.split(" - ")
    status_codes_dict = ast.literal_eval(status_codes)
    print(status_codes_dict)

    for r in responses:
        assert getattr(r, "status_code", r.__class__.__name__) in status_codes_dict


if __name__ == "__main__":
    pytest.main(["-vv"])
