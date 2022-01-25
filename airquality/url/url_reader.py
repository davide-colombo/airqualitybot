# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 19:42
# ======================================
import logging
import requests
import requests.exceptions
from airquality.url import HTTP_ERROR_MESSAGES, DEFAULT_ERROR_MESSAGE


MAX_SERVER_RESPONSE_TIMEOUT = 10.0              # how many seconds to wait for a server response.


class URLReadError(Exception):
    """
    A subclass of Exception that signal an error while reading the content at a given URL.
    """
    pass


def _fmt_url_read_error_msg(
    err_url: str,                       # The URL that causes the error.
    status_code: int,                   # The HTTP response status code.
    code_explain: str,                  # The HTTP status code text explanation.
    http_jresp: str                     # The HTTP response json representation.
):
    return f"[HTTP STATUS CODE]: {status_code} - " \
           f"[HTTP CODE EXPLANATION]: {code_explain} - " \
           f"[HTTP JSON RESPONSE]: {http_jresp} - " \
           f"[ERROR URL]: {err_url}"


class URLReader(object):
    """
    A class that defines the business rules for reading the content of the given URL using HTTP(S) protocol.
    """

    def __init__(self, timeout_in_seconds=MAX_SERVER_RESPONSE_TIMEOUT):
        self._timeout_in_seconds = timeout_in_seconds
        self._logger = logging.getLogger(__name__)

    def json(self, url: str):
        return self._safe_get(url).json()

    def _safe_get(self, url: str):
        http_response = requests.get(
            url=url,
            timeout=self._timeout_in_seconds,
            headers={'Connection': 'close'}
        )
        if 400 <= http_response.status_code < 600:
            cause = _fmt_url_read_error_msg(
                err_url=url,
                status_code=http_response.status_code,
                code_explain=HTTP_ERROR_MESSAGES.get(http_response.status_code, DEFAULT_ERROR_MESSAGE),
                http_jresp=http_response.json()
            )
            self._raise(cause=cause)
        return http_response

    def _raise(self, cause: str):
        self._logger.exception(cause)
        raise URLReadError(cause)

    def __repr__(self):
        return f"{type(self).__name__}(timeout={self._timeout_in_seconds})"
