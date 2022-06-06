"""
Global test fixtures
"""
import pathlib
import random

import httpx
import pytest
import respx

from csv2http import parser

from .constants import TEST_CSVS


@pytest.fixture(scope="module", params=TEST_CSVS)
def csv_payload_generator_param_fxt(request):
    """Parametrized fixture of csv_payload_generators, one per CSV in tests/data."""
    payload_gen = parser.csv_payload_generator(request.param)
    yield payload_gen


@pytest.fixture(scope="module")
def sample_csv() -> pathlib.Path:
    return pathlib.Path(TEST_CSVS[1])


def _reflect_request(request: httpx.Request) -> respx.MockResponse:
    reflect_headers = {"content-type", "content-length"}
    headers = {k: v for (k, v) in request.headers.items() if k in reflect_headers}
    return respx.MockResponse(200, content=request.content, headers=headers)


def _reflect_request_random_status(request: httpx.Request) -> respx.MockResponse:
    response = _reflect_request(request)
    response.status_code = random.choice((200, 200, 201, 202, 401, 403, 404, 422, 500))
    return response


@pytest.fixture
def http_reflect():
    """Return all outgoing http POST | PUT | PATCH request's payload as a response."""
    # TODO: make http_reflect_airgap
    # pylint: disable=not-context-manager
    with respx.mock(assert_all_called=False, assert_all_mocked=True) as respx_mock:

        respx_mock.route(method__in=["POST", "PUT", "PATCH"]).mock(
            side_effect=_reflect_request
        )

        yield respx_mock


@pytest.fixture
def http_reflect_random_status():
    """Randomize status codes. Return all outgoing http request's payload as a response."""
    # pylint: disable=not-context-manager
    with respx.mock(assert_all_called=False, assert_all_mocked=True) as respx_mock:

        respx_mock.route(method__in=["POST", "PUT", "PATCH"]).mock(
            side_effect=_reflect_request_random_status
        )

        yield respx_mock
