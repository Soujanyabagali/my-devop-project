import io
import importlib
import os


def reload_app():
    import app.main as main
    importlib.reload(main)
    return main.app


def test_upload_and_serve(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    monkeypatch.setenv("UPLOAD_DIR", str(upload_dir))
    app = reload_app()
    client = app.test_client()

    data = {
        'file': (io.BytesIO(b'fake-image-bytes'), 'test.png')
    }
    resp = client.post('/upload', data=data, content_type='multipart/form-data')
    assert resp.status_code == 201
    body = resp.get_json()
    assert body['filename'] == 'test.png'

    # file saved to UPLOAD_DIR
    saved = upload_dir / 'test.png'
    assert saved.exists()

    # can retrieve via /uploads/<filename>
    get_resp = client.get(f"/uploads/test.png")
    assert get_resp.status_code == 200
    assert get_resp.data == b'fake-image-bytes'
