"""
Global test fixtures
"""
import httpx
import pytest
import respx

from csv2http import parser

from .constants import TEST_CSVS


@pytest.fixture(scope="module", params=TEST_CSVS)
def payload_generator_param_fxt(request):
    """Parametrized fixture of payload_generators, one per CSV in tests/data."""
    payload_gen = parser.payload_generator(request.param)
    yield payload_gen


def _reflect_request(request: httpx.Request):
    reflect_headers = {"content-type", "content-length"}
    headers = {k: v for (k, v) in request.headers.items() if k in reflect_headers}
    return respx.MockResponse(200, content=request.content, headers=headers)


@pytest.fixture
def http_reflect():
    """Return all outgoing http request's payload as a response."""
    # TODO: make http_reflect_airgap
    with respx.mock(assert_all_called=False, assert_all_mocked=True) as respx_mock:

        respx_mock.route(method__in=["POST", "PUT", "PATCH"]).mock(
            side_effect=_reflect_request
        )

        yield respx_mock
