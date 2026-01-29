import importlib


def reload_app():
    import app.main as main
    importlib.reload(main)
    return main.app


def test_dev_message(monkeypatch):
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("GREETING_DEV", "Hello Dev")
    app = reload_app()
    client = app.test_client()
    resp = client.get("/")
    data = resp.get_json()
    assert data["environment"] == "dev"
    assert data["message"] == "Hello Dev"


def test_test_message(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("GREETING_TEST", "Hello Test")
    app = reload_app()
    client = app.test_client()
    resp = client.get("/")
    data = resp.get_json()
    assert data["environment"] == "test"
    assert data["message"] == "Hello Test"
