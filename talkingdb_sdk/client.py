import threading
import time
from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict, List, Optional, Union

import requests
from requests.exceptions import RequestException
from tenacity import (
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from .exceptions import (
    HTTPError,
    JobFailedError,
    NotFoundError,
    QueueFullError,
    SpoolExhaustedError,
    TalkingDBError,
    UnauthorizedError,
    UnsupportedTypeError,
    ValidationError,
    FileTooLargeError,
)
from .types import JobAccepted, JobState, JobStatus


FilePathOrHandle = Union[str, Path, BinaryIO]


def _is_retryable_exception(exc: Exception) -> bool:
    """Retry network errors, timeouts, and 5xx; never 4xx."""
    if isinstance(exc, RequestException):
        if isinstance(exc, requests.HTTPError) and exc.response is not None:
            return 500 <= exc.response.status_code < 600
        return True
    return False


def _retry_after_seconds(res: requests.Response) -> Optional[int]:
    raw = res.headers.get("Retry-After")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _body(res: requests.Response) -> Dict[str, Any]:
    try:
        return res.json()
    except ValueError:
        return {"raw": res.text}


def _to_typed_exception(http_err: requests.HTTPError) -> TalkingDBError:
    """Map a raw requests.HTTPError into the SDK's typed hierarchy."""
    res = http_err.response
    if res is None:
        return HTTPError(0, {"raw": str(http_err)})

    status = res.status_code
    body = _body(res)
    url = res.url
    retry_after = _retry_after_seconds(res)

    if status == 401:
        return UnauthorizedError(status, body, url)
    if status == 404:
        return NotFoundError(status, body, url)
    if status == 413:
        return FileTooLargeError(status, body, url)
    if status == 415:
        return UnsupportedTypeError(status, body, url)
    if status == 422:
        return ValidationError(status, body, url)
    if status == 429:
        return QueueFullError(status, body, url, retry_after_seconds=retry_after)
    if status == 503:
        return SpoolExhaustedError(status, body, url, retry_after_seconds=retry_after)
    return HTTPError(status, body, url)


class TalkingDBClient:
    """HTTP client for the TalkingDB service.

    Pass ``api_key=`` to build the ``Authorization: Bearer <key>`` header
    automatically. Custom headers via ``headers=`` are merged on top.
    """

    def __init__(
        self,
        host: str,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
        api_key: Optional[str] = None,
    ):
        self.host = host.rstrip("/")
        self.timeout = timeout
        self.default_headers: Dict[str, str] = {}
        if api_key:
            self.default_headers["Authorization"] = f"Bearer {api_key}"
        if headers:
            self.default_headers.update(headers)
        self._local = threading.local()

    # ----------------------------------------------------------- session
    def _get_session(self) -> requests.Session:
        if not hasattr(self._local, "session"):
            session = requests.Session()
            session.headers.update(self.default_headers)
            self._local.session = session
        return self._local.session

    # ----------------------------------------------------------- request
    def _do_request(
        self,
        method: str,
        url: str,
        *,
        json: Optional[dict] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> requests.Response:
        res = self._get_session().request(
            method,
            url,
            json=json,
            files=files,
            data=data,
            params=params,
            timeout=timeout if timeout is not None else self.timeout,
        )
        res.raise_for_status()
        return res

    def _request(
        self,
        method: str,
        url: str,
        *,
        json: Optional[dict] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        retry_attempts: int = 5,
        retry_max_wait: float = 10.0,
    ) -> requests.Response:
        """Unified request with retry + typed-exception mapping."""
        retryer = Retrying(
            retry=retry_if_exception(_is_retryable_exception),
            stop=stop_after_attempt(retry_attempts),
            wait=wait_exponential_jitter(initial=1, max=retry_max_wait),
            reraise=True,
        )
        try:
            return retryer(
                self._do_request,
                method,
                url,
                json=json,
                files=files,
                data=data,
                params=params,
                timeout=timeout,
            )
        except requests.HTTPError as exc:
            raise _to_typed_exception(exc) from exc
        except RequestException as exc:
            raise TalkingDBError(str(exc)) from exc

    def _post(self, url: str, payload: dict) -> requests.Response:
        return self._request("POST", url, json=payload)

    def _get(self, url: str) -> requests.Response:
        # Shorter retry policy for polling - next poll is seconds away.
        return self._request(
            "GET", url, retry_attempts=3, retry_max_wait=5.0, timeout=5.0
        )

    # ------------------------------------------------------- existing API
    def index_document(
        self,
        document: dict,
        metadata: dict,
    ) -> Optional[str]:
        url = f"{self.host}/index/document/elements"
        payload = {"metadata": metadata, "document": document}
        res = self._post(url, payload)
        return res.json().get("graph_id")

    def match_node(
        self,
        graph_ids: List[str],
        query: str,
        max_results: int = 20,
        metadata: dict | None = None,
    ) -> list:
        url = f"{self.host}/v1/queries"
        payload: Dict[str, Any] = {
            "graph_ids": graph_ids,
            "text": query,
            "max_results": max_results,
        }
        if metadata is not None:
            payload["metadata"] = metadata
        res = self._post(url, payload)
        return res.json().get("elements", [])

    # --------------------------------------------------- document management
    def list_documents(
        self, session_id: Optional[str] = None
    ) -> List[JobStatus]:
        url = f"{self.host}/v1/documents"
        params = {"session_id": session_id} if session_id else None
        res = self._request(
            "GET", url, params=params,
            retry_attempts=3, retry_max_wait=5.0, timeout=5.0,
        )
        return [JobStatus.from_dict(item) for item in res.json()]

    def remove_document(self, job_id: str) -> JobStatus:
        url = f"{self.host}/v1/documents/{job_id}"
        res = self._request("DELETE", url)
        return JobStatus.from_dict(res.json())

    # ------------------------------------------------------- async ingest
    def submit_document(
        self,
        file: FilePathOrHandle,
        metadata: Optional[dict] = None,
        filename: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> JobAccepted:
        url = f"{self.host}/v1/documents"

        handle, resolved_name, opened_here = _open_file(file, filename)
        try:
            multipart: Dict[str, Any] = {
                "file": (
                    resolved_name,
                    handle,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
            }
            form: Dict[str, Any] = {}
            if metadata is not None:
                import json as _json
                form["metadata"] = _json.dumps(metadata)
            if session_id is not None:
                form["session_id"] = session_id

            res = self._request(
                "POST", url, files=multipart, data=form or None, timeout=self.timeout
            )
        finally:
            if opened_here:
                handle.close()

        return JobAccepted.from_dict(res.json())

    def get_job_status(self, job_id: str) -> JobStatus:
        """Fetch the current lifecycle state of ``job_id``."""
        url = f"{self.host}/v1/jobs/{job_id}"
        res = self._get(url)
        return JobStatus.from_dict(res.json())

    def cancel_job(self, job_id: str) -> JobStatus:
        url = f"{self.host}/v1/jobs/{job_id}/cancel"
        res = self._request("POST", url)
        return JobStatus.from_dict(res.json())

    def wait_for_terminal(
        self,
        job_id: str,
        *,
        poll_interval: float = 1.0,
        timeout: Optional[float] = None,
        on_progress: Optional[Callable[[JobStatus], None]] = None,
    ) -> JobStatus:
        started = time.monotonic()
        while True:
            status = self.get_job_status(job_id)
            if on_progress is not None:
                on_progress(status)
            if status.is_terminal():
                return status
            if timeout is not None and time.monotonic() - started > timeout:
                raise TimeoutError(
                    f"job {job_id} did not terminate within {timeout}s "
                    f"(last state={status.state.value})"
                )
            time.sleep(poll_interval)

    def ingest_document(
        self,
        file: FilePathOrHandle,
        metadata: Optional[dict] = None,
        filename: Optional[str] = None,
        session_id: Optional[str] = None,
        *,
        poll_interval: float = 1.0,
        timeout: Optional[float] = None,
        on_progress: Optional[Callable[[JobStatus], None]] = None,
    ) -> JobStatus:
        accepted = self.submit_document(file, metadata, filename, session_id)
        terminal = self.wait_for_terminal(
            accepted.job_id,
            poll_interval=poll_interval,
            timeout=timeout,
            on_progress=on_progress,
        )
        if terminal.state == JobState.FAILED:
            raise JobFailedError(
                terminal.job_id,
                terminal.error_code.value if terminal.error_code else None,
                terminal.error_message,
            )
        return terminal


# --------------------------------------------------------- file helpers
def _open_file(
    file: FilePathOrHandle, filename: Optional[str]
) -> tuple[BinaryIO, str, bool]:
    """Return (handle, resolved_filename, opened_here)."""
    if isinstance(file, (str, Path)):
        path = Path(file)
        handle = path.open("rb")
        return handle, filename or path.name, True

    name = filename or getattr(file, "name", None)
    if not name:
        raise ValueError(
            "filename= is required when passing a file handle without .name"
        )
    return file, Path(name).name, False
