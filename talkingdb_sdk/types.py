from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class JobType(str, Enum):
    DOCUMENT = "document"


class JobState(str, Enum):
    QUEUED = "QUEUED"
    ONGOING = "ONGOING"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    @classmethod
    def terminal(cls) -> set["JobState"]:
        return {cls.CANCELLED, cls.COMPLETED, cls.FAILED}

    def is_terminal(self) -> bool:
        return self in self.terminal()


class JobStage(str, Enum):
    VALIDATING = "VALIDATING"
    PARSING = "PARSING"
    ELEMENT_EXTRACTION = "ELEMENT_EXTRACTION"
    TREE_GENERATION = "TREE_GENERATION"
    INDEXING = "INDEXING"
    PERSISTING = "PERSISTING"


class JobErrorCode(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    PARSE_ERROR = "PARSE_ERROR"
    INDEX_ERROR = "INDEX_ERROR"
    PERSIST_ERROR = "PERSIST_ERROR"
    TIMEOUT = "TIMEOUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


@dataclass(frozen=True)
class JobAccepted:
    """Response from ``POST /v1/documents``."""

    job_id: str
    job_type: JobType
    state: JobState
    session_id: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "JobAccepted":
        return cls(
            job_id=payload["job_id"],
            job_type=JobType(payload["job_type"]),
            state=JobState(payload["state"]),
            session_id=payload.get("session_id"),
        )


@dataclass(frozen=True)
class JobStatus:
    """Response from ``GET /v1/jobs/{job_id}`` and the cancel endpoint."""

    job_id: str
    job_type: JobType
    state: JobState
    stage: Optional[JobStage]
    percent: Optional[int]
    status_message: Optional[str]
    result_graph_id: Optional[str]
    result_summary: Optional[Dict[str, Any]]
    error_code: Optional[JobErrorCode]
    error_message: Optional[str]
    session_id: Optional[str] = None

    def is_terminal(self) -> bool:
        return self.state.is_terminal()

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "JobStatus":
        return cls(
            job_id=payload["job_id"],
            job_type=JobType(payload["job_type"]),
            state=JobState(payload["state"]),
            stage=JobStage(payload["stage"]) if payload.get("stage") else None,
            percent=payload.get("progress", payload.get("percent")),
            status_message=payload.get("status_message"),
            result_graph_id=payload.get("result_graph_id"),
            result_summary=payload.get("result_summary"),
            error_code=(
                JobErrorCode(payload["error_code"])
                if payload.get("error_code")
                else None
            ),
            error_message=payload.get("error_message"),
            session_id=payload.get("session_id"),
        )


@dataclass(frozen=True)
class Namespace:
    namespace: str
    public_read: bool
    title: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Namespace":
        return cls(
            namespace=payload["namespace"],
            public_read=bool(payload.get("public_read", False)),
            title=payload.get("title"),
            description=payload.get("description"),
        )


@dataclass(frozen=True)
class NamespaceDocument:
    id: str
    state: str
    title: Optional[str] = None
    description: Optional[str] = None
    suggested_queries: List[str] = field(default_factory=list)
    result_graph_id: Optional[str] = None
    namespace: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "NamespaceDocument":
        return cls(
            id=payload["id"],
            state=payload.get("state", ""),
            title=payload.get("title"),
            description=payload.get("description"),
            suggested_queries=list(payload.get("suggested_queries") or []),
            result_graph_id=payload.get("result_graph_id"),
            namespace=payload.get("namespace"),
        )
