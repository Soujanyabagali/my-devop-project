# My DevOps Project — Flask config & environments

Overview
- Simple Flask app that reads configuration from environment variables.
- Local development uses a `.env` file (with `python-dotenv`).
- Docker containers receive configuration via environment variables at runtime.
- CI is implemented with GitHub Actions (build → test → docker build).

Files
- `app/main.py` — Flask app entry that reads configuration at startup.
- `app/config.py` — Helper that reads environment variables.
- `.env.example` — Example local environment values.
- `Dockerfile` — Build container image. Pass environment variables when running.
- `.github/workflows/ci.yml` — CI pipeline that installs, tests and builds Docker image.

Local setup
1. Copy `.env.example` to `.env` and edit values for local development.

   Example `.env`:

   APP_ENV=dev
   GREETING_DEV=Hello Developer
   GREETING_TEST=Hello Tester
   PORT=5000

2. Create virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the app locally (dotenv will be loaded automatically):

```powershell
python -m app.main
```

Upload images
- Upload a file with `curl`:

```powershell
curl -F "file=@./local-image.png" http://127.0.0.1:5000/upload
```

- The response includes a `url` you can GET to retrieve the file, for example `http://127.0.0.1:5000/uploads/local-image.png`.

- To change where files are stored, set `UPLOAD_DIR` environment variable (or in `.env`).

Docker
1. Build image:

```powershell
docker build -t my-devops-project:latest .
```

2. Run container in `dev` mode (pass env vars at runtime):

```powershell
docker run -p 5000:5000 -e APP_ENV=dev -e GREETING_DEV="Hello Docker Dev" my-devops-project:latest
```

3. Run container in `test` mode:

```powershell
docker run -p 5000:5000 -e APP_ENV=test -e GREETING_TEST="Hello Docker Test" my-devops-project:latest
```

CI (GitHub Actions)
- The `.github/workflows/ci.yml` pipeline installs dependencies, runs `pytest`, and builds the Docker image.

Notes
- Configuration values are never hardcoded in application logic — they are read from environment variables.
- Use `.env` for local convenience only; never commit secrets to the repo.
