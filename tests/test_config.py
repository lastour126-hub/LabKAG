from app.config import Settings


def test_neo4j_settings_are_loaded_from_primary_names():
    settings = Settings(
        neo4j_uri="bolt://new-host:7687",
        neo4j_user="new-user",
        neo4j_password="new-password",
        neo4j_database="new-db",
    )

    assert settings.neo4j_uri == "bolt://new-host:7687"
    assert settings.neo4j_user == "new-user"
    assert settings.neo4j_password == "new-password"
    assert settings.neo4j_database == "new-db"


def test_neo4j_settings_have_local_defaults_except_password():
    settings = Settings(_env_file=None)

    assert settings.graph_backend == "neo4j"
    assert settings.neo4j_uri == "bolt://127.0.0.1:7687"
    assert settings.neo4j_user == "neo4j"
    assert settings.neo4j_password is None
    assert settings.neo4j_database == "neo4j"
