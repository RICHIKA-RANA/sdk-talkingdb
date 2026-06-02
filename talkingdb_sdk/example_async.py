from talkingdb_sdk import (
    JobState,
    TalkingDBClient,
    JobFailedError,
)


def main() -> None:
    client = TalkingDBClient(
        host="http://localhost:8090",
        api_key="REPLACE_WITH_TDB_API_KEY",
        timeout=30,
    )

    metadata = {"scope": "org", "event_group_id": "", "trigger_event_id": ""}

    # 1. Submit - returns immediately with a job_id.
    accepted = client.submit_document(
        "sample.docx",
        metadata=metadata,
    )
    print(
        f"queued: job_id={accepted.job_id} "
        f"job_type={accepted.job_type.value} state={accepted.state.value}"
    )

    # 2. Wait for terminal - polls GET /v1/jobs/{id} every second.
    def on_progress(status):
        print(
            f"  poll: state={status.state.value} "
            f"stage={status.stage.value if status.stage else '-'} "
            f"percent={status.percent}"
        )

    try:
        terminal = client.wait_for_terminal(
            accepted.job_id, poll_interval=1.0, on_progress=on_progress
        )
    except TimeoutError as exc:
        print(f"gave up waiting: {exc}")
        return

    # 3. Inspect the terminal payload.
    if terminal.state == JobState.COMPLETED:
        print(
            f"done: graph_id={terminal.result_graph_id} "
            f"summary={terminal.result_summary}"
        )
    elif terminal.state == JobState.CANCELLED:
        print("cancelled by user / daemon")
    elif terminal.state == JobState.FAILED:
        print(
            f"failed: {terminal.error_code.value if terminal.error_code else None} "
            f"- {terminal.error_message}"
        )


def main_oneshot() -> None:
    """Same flow via the ingest_document convenience helper.

    JobFailedError is raised on terminal FAILED so the caller does not
    have to introspect the status payload.
    """
    client = TalkingDBClient(
        host="http://localhost:8090",
        api_key="REPLACE_WITH_TDB_API_KEY",
        timeout=30,
    )

    try:
        terminal = client.ingest_document(
            "sample.docx",
            metadata={"scope": "org", "event_group_id": "", "trigger_event_id": ""},
            poll_interval=1.0,
            timeout=600,
        )
    except JobFailedError as exc:
        print(f"failed: {exc.error_code} - {exc.error_message}")
        return

    print(f"graph_id={terminal.result_graph_id}")


if __name__ == "__main__":
    main()
