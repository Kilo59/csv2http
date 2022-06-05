import httpx


def response_details(response: httpx.Response, verbose: bool = False) -> str:
    """Returns a string details of the response and the original request."""
    # TODO: response json/content
    result = f"{response.request.method} {response.request.url} -> {response}"
    if verbose:
        result += (
            f"\n  headers - {dict(response.headers)}"
            + f"\n  content - {response.content.decode()}"
        )
    return result
