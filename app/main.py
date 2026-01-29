from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

load_dotenv()

from .config import get_config

config = get_config()

app = Flask(__name__)
app.config.update(config)


@app.route("/")
def index():
    env = app.config.get("APP_ENV")
    if env == "dev":
        message = app.config.get("GREETING_DEV") or app.config.get("GREETING") or f"Running in {env}"
    else:
        message = app.config.get("GREETING_TEST") or app.config.get("GREETING") or f"Running in {env}"
    return jsonify(environment=env, message=message)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify(error='no file part'), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify(error='empty filename'), 400
    filename = secure_filename(f.filename)
    upload_dir = app.config.get('UPLOAD_DIR') or os.environ.get('UPLOAD_DIR', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    dest = os.path.join(upload_dir, filename)
    f.save(dest)
    url = f"/uploads/{filename}"
    return jsonify(filename=filename, url=url), 201


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    upload_dir = app.config.get('UPLOAD_DIR') or os.environ.get('UPLOAD_DIR', 'uploads')
    return send_from_directory(upload_dir, filename)


def run():
    host = app.config.get("HOST")
    port = app.config.get("PORT")
    app.run(host=host, port=port)


if __name__ == "__main__":
    run()
