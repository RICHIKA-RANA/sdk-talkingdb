"""Examples for namespaces, demo documents and suggested queries.

  1. Public discovery - no API key required.
  2. Developer curation - train a document into a namespace with curated metadata.
  3. Authenticated namespace management.
"""

from talkingdb_sdk import TalkingDBClient

HOST = "http://localhost:8090"
API_KEY = "REPLACE_WITH_TDB_API_KEY"


def public_discovery() -> None:
    """A signed-out client discovers and browses public demo content."""
    anon = TalkingDBClient(HOST)  # no api_key needed for /public/*

    for ns in anon.list_public_namespaces():
        print(f"{ns.namespace}: {ns.title} - {ns.description}")
        for doc in anon.list_public_namespace_documents(ns.namespace):
            print(f"  - {doc.title}  (graph={doc.result_graph_id})")
            for q in doc.suggested_queries:
                print(f"      • {q}")


def curate_demo_document() -> None:
    """Developer-only: train a document into the demo-library namespace."""
    client = TalkingDBClient(HOST, api_key=API_KEY)

    accepted = client.submit_document(
        "clinical-overview.pdf",
        namespace="demo-library",
        title="Clinical Trial Overview",
        description="A short summary of a sample clinical trial protocol.",
        suggested_queries=[
            "What is the primary endpoint?",
            "How many participants were enrolled?",
            "What are the inclusion criteria?",
        ],
    )
    print("submitted:", accepted.job_id, accepted.state)


def manage_namespaces() -> None:
    """Authenticated management view over all namespaces and their documents."""
    client = TalkingDBClient(HOST, api_key=API_KEY)

    for ns in client.list_namespaces():
        print(f"{ns.namespace} (public_read={ns.public_read})")
        for doc in client.list_namespace_documents(ns.namespace, completed_only=False):
            print(f"  - [{doc.state}] {doc.title}")


if __name__ == "__main__":
    public_discovery()
