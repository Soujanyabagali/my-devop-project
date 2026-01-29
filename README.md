# My DevOps Project — Flask config & environments

[![CI](https://github.com/Soujanyabagali/my-devop-project/actions/workflows/ci.yml/badge.svg)](https://github.com/Soujanyabagali/my-devop-project/actions/workflows/ci.yml)

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
- The `.github/workflows/ci.yml` pipeline:
  1. Installs dependencies
  2. Runs `pytest` tests
  3. Builds the Docker image
- No secrets required — runs automatically on every push to `main` or `master`

Deploy to Render (free PaaS)
1. Create a free Render.com account at https://render.com
2. Create a new "Web Service" and connect your GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python -m app.main`
5. Under "Environment" add runtime vars:
   - `APP_ENV=prod`
   - `GREETING=Hello from Render`
   - `PORT=5000`
6. Deploy — Render auto-builds and runs the app on each push.

Deploy to Railway (free tier)
1. Go to https://railway.app and sign in with GitHub
2. Create a new project → Deploy from GitHub repo
3. Select your repo and branch
4. Add environment variables under "Variables"
5. Deploy — Railway auto-detects the Flask app and runs it.

Notes
- Configuration values are never hardcoded in application logic — they are read from environment variables.
- Use `.env` for local convenience only; never commit secrets to the repo.
- For production, use strong credentials and store in GitHub Secrets or platform env vars.
