"""
utils.py
~~~~~~~~
Homeless utilities.
"""

from typing import Counter

from httpx import Response

# pylint: disable=fixme


def response_details(response: Response, verbose: bool = False) -> str:
    """Returns a string details of the response and the original request."""
    # TODO: prettyprint json
    result = f"{response.request.method} {response.request.url} -> {response}"
    if verbose:
        result += (
            f"\n  headers - {dict(response.headers)}"
            + f"\n  content - {response.content.decode()}"
        )
    return result


def summarize_responses(responses: list[Response]) -> str:
    """Returns count of all response status codes sorted by status code"""
    # TODO: make this pretty, display as table with running tally of previous responses
    counter = Counter([r.status_code for r in responses])
    # TODO: maybe don't bother sorting this
    sorted_dict = dict(sorted(counter.items(), key=lambda item: item[0]))
    return f"status codes - {sorted_dict}"
