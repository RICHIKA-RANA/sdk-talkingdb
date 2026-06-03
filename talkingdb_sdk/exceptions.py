from typing import Any, Dict, Optional


class TalkingDBError(Exception):
    """Base class for every SDK-raised error."""


class HTTPError(TalkingDBError):
    """A non-2xx response that survived retries."""

    def __init__(
        self,
        status_code: int,
        body: Optional[Dict[str, Any]] = None,
        url: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.body = body or {}
        self.url = url
        super().__init__(
            f"HTTP {status_code} from {url!r}: {self.body}"
        )


class UnauthorizedError(HTTPError):
    """401 from the API."""


class NotFoundError(HTTPError):
    """404 - unknown resource (e.g. unknown job_id)."""


class FileTooLargeError(HTTPError):
    """413 - uploaded file exceeds the server's size cap."""


class UnsupportedTypeError(HTTPError):
    """415 - uploaded file type is not supported."""


class ValidationError(HTTPError):
    """422 - request body failed validation."""


class _RetryableHTTPError(HTTPError):
    """Mixin: 429 / 503 carry a ``retry_after_seconds`` hint."""

    def __init__(
        self,
        status_code: int,
        body: Optional[Dict[str, Any]] = None,
        url: Optional[str] = None,
        retry_after_seconds: Optional[int] = None,
    ) -> None:
        super().__init__(status_code, body, url)
        self.retry_after_seconds = retry_after_seconds


class QueueFullError(_RetryableHTTPError):
    """429 - worker pool at capacity."""


class SpoolExhaustedError(_RetryableHTTPError):
    """503 - spool directory has no room."""


class JobFailedError(TalkingDBError):
    """``wait_for_terminal`` saw the job land in state ``FAILED``."""

    def __init__(
        self,
        job_id: str,
        error_code: Optional[str],
        error_message: Optional[str],
    ) -> None:
        self.job_id = job_id
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(
            f"job {job_id} failed: {error_code}: {error_message}"
        )
