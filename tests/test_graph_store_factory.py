import pytest

from app.adapters.graph_store_factory import GraphStoreFactoryError, build_graph_store
from app.adapters.neo4j_graph_store import Neo4jGraphStore
from app.config import Settings


def test_build_graph_store_returns_neo4j_store_from_primary_settings():
    settings = Settings(
        graph_backend="neo4j",
        neo4j_uri="bolt://new-host:7687",
        neo4j_user="new-user",
        neo4j_password="new-password",
        neo4j_database="new-db",
    )

    store = build_graph_store(settings)

    assert isinstance(store, Neo4jGraphStore)
    assert store.uri == "bolt://new-host:7687"
    assert store.user == "new-user"
    assert store.password == "new-password"
    assert store.database == "new-db"


def test_build_graph_store_requires_neo4j_password():
    settings = Settings(graph_backend="neo4j", neo4j_password=None)

    with pytest.raises(GraphStoreFactoryError, match="NEO4J_PASSWORD is required"):
        build_graph_store(settings)


def test_build_graph_store_rejects_unknown_backend():
    settings = Settings(graph_backend="unknown")

    with pytest.raises(GraphStoreFactoryError, match="Unsupported GRAPH_BACKEND"):
        build_graph_store(settings)
