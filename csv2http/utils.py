"""
utils.py
~~~~~~~~
Homeless utilities.
"""
import datetime as dt
import pathlib
import traceback
from typing import Counter, Union

from typing import Counter

from httpx import Response

# pylint: disable=fixme

UTF8 = "utf-8"


def format_traceback(ex: Union[Exception, BaseException]) -> str:
    """Generate a full exception traceback string from an exception."""
    tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    return "".join(tb_lines)


def dump_crash_log(
    file_stem: str, exc: Union[Exception, BaseException]
) -> pathlib.Path:
    """Write a crash log with a timestamp to a `.crash.log` file."""
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    file_path = pathlib.Path(f"{file_stem}_{timestamp}.crash.log")
    with open(file_path, mode="w+", encoding=UTF8) as file_out:
        file_out.write(format_traceback(exc))
    return file_path


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
