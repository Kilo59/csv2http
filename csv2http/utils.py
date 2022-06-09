"""
utils.py
~~~~~~~~
Homeless utilities.
"""
import datetime as dt
import pathlib
import traceback
from typing import Counter, Union

from httpx import Request, Response

# pylint: disable=fixme

UTF8 = "utf-8"

# TODO: refactor `_add_timestamp_and_suffix` and its use.
# bad coupling and seperation of concerns here
# `dump_crash_log` & `append_responses` shouldn't need to know anything about a CSV file


def _add_timestamp_and_suffix(
    file_path: pathlib.Path, suffix: str = "log"
) -> pathlib.Path:
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    return pathlib.Path(f"{file_path.stem}_{timestamp}.{suffix}")


def format_traceback(ex: Union[Exception, BaseException]) -> str:
    """Generate a full exception traceback string from an exception."""
    tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    return "".join(tb_lines)


def dump_crash_log(
    csv_source_file_name: pathlib.Path, exc: Union[Exception, BaseException]
) -> pathlib.Path:
    """Write a crash log with a timestamp to a `.crash.log` file."""
    crash_log = _add_timestamp_and_suffix(csv_source_file_name, "crash.log")
    with open(crash_log, mode="w", encoding=UTF8) as file_out:
        file_out.write(format_traceback(exc))
    return crash_log


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


def _get_request_identifiers(request: Request) -> str:
    """
    Extract identiying details from the request payload
    TODO: only pull out `id` and or `name` values if they exist
    """
    return f"{request.content.decode(UTF8)}"


def _extract_log(response: Response) -> str:
    return f"{response} - {_get_request_identifiers(response.request)}"


def append_responses(
    csv_source_file_name: pathlib.Path,
    responses: list[Response],
) -> pathlib.Path:
    """
    Append response results to a file.
    TODO: write to a logger and define a file handler logger
    """
    log_path = _add_timestamp_and_suffix(csv_source_file_name, "log")
    with open(log_path, mode="a", encoding=UTF8) as file_out:
        file_out.writelines([_extract_log(r) + "\n" for r in responses])
    return log_path
