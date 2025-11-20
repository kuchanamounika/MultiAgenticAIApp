# MultiAgenticAIApp

Full-stack AI scaffold combining FastAPI backend, Streamlit frontend and simple agents.

Structure
- `backend/app/` — FastAPI backend with routers for finance, search, docs (PDF upload + embeddings), and chat.
- `frontend/` — Streamlit app that interacts with the backend.
- `agents/` — small agent example using `phidata`-style tools.
- `.env.example` — example environment variables.

This scaffold is a starting point. Some features (Postgres + pgvector, external model APIs) require provisioning and credentials.
MultiAgenticAIApp
## Deployment Guide (Windows & Linux)

This section shows step-by-step instructions to run the project locally on Windows (PowerShell) or Linux (bash). It includes two alternatives for Postgres with `pgvector`: native installation and Docker.

Prerequisites
- Python 3.10+ installed
- Git (optional)
- Docker & Docker Compose (optional, recommended for DB via container)

Files to review before running
- Copy `.env.example` -> `.env` and fill keys:
	- `OPENAI_API_KEY`, `GROQ_API_KEY`, `GOOGLE_API_KEY` (if used)
	- `DATABASE_URL` (Postgres)
	- `API_URL` for frontend

### Option A — Use Docker Compose (recommended)
This is the simplest cross-platform approach: run Postgres with pgvector in Docker.

1. Create `docker-compose.yml` alongside `MultiAgenticAIApp/` with this content:

```yaml
version: '3.8'
services:
	db:
		image: ankane/pgvector:postgres-15
		environment:
			POSTGRES_USER: aiuser
			POSTGRES_PASSWORD: aipass
			POSTGRES_DB: aiapp
		ports:
			- "5432:5432"
		volumes:
			- db_data:/var/lib/postgresql/data

volumes:
	db_data:
```

2. Start DB (PowerShell or bash):

```powershell
docker compose up -d
```

3. Set `DATABASE_URL` in `.env`:

```text
DATABASE_URL=postgresql+psycopg://aiuser:aipass@localhost:5432/aiapp
```

4. The code calls `init_pgvector()` on startup which will try to create the extension. If the image includes pgvector (the `ankane/pgvector` image does), no extra step is needed.

### Option B — Native Postgres installation (Linux example)
On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
# Install pgvector (Debian/Ubuntu might provide pgvector or use pgxn/extension install)
sudo apt install -y postgresql-15-pgvector || echo "Install pgvector via your distro or compile from source"
# Start DB
sudo systemctl enable --now postgresql
# Create DB and user
sudo -u postgres psql -c "CREATE USER aiuser WITH PASSWORD 'aipass';"
sudo -u postgres psql -c "CREATE DATABASE aiapp OWNER aiuser;"
```

Set `.env` DATABASE_URL accordingly.

## Python virtual environment & dependencies

Windows (PowerShell)
```powershell
cd D:/ML/MultiAgenticAIApp/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux (bash)
```bash
cd /path/to/MultiAgenticAIApp/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the backend (FastAPI)

Windows (PowerShell)
```powershell
# Ensure .env is present at project root or backend/app/config.py loads it
cd D:/ML/MultiAgenticAIApp/backend
$env:DATABASE_URL = "postgresql+psycopg://aiuser:aipass@localhost:5432/aiapp"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Linux (bash)
```bash
export DATABASE_URL="postgresql+psycopg://aiuser:aipass@localhost:5432/aiapp"
cd /path/to/MultiAgenticAIApp/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run the frontend (Streamlit)

Windows (PowerShell)
```powershell
cd D:/ML/MultiAgenticAIApp/frontend
$env:API_URL = "http://localhost:8000"
streamlit run streamlit_app.py
```

Linux (bash)
```bash
cd /path/to/MultiAgenticAIApp/frontend
export API_URL=http://localhost:8000
streamlit run streamlit_app.py
```

## Run the example agent

Windows (PowerShell)
```powershell
cd D:/ML/MultiAgenticAIApp/agents
python agent.py
```

Linux (bash)
```bash
cd /path/to/MultiAgenticAIApp/agents
python agent.py
```

## Notes & Troubleshooting
- Windows temp path: The `docs` upload router writes temporary files to `/tmp`. On Windows that may not exist; change `docs.py` to use `tempfile.NamedTemporaryFile(delete=False)` for a portable temp path.
- If embeddings/LLM calls fail due to missing API keys, either set the keys in `.env` or run with mock configurations.
- If Postgres reports missing `vector` extension, ensure you used a Postgres build with `pgvector` installed (Docker image above or install pgvector for your platform).

## Optional: Run everything with Docker Compose
You can extend the `docker-compose.yml` above to include services for the backend and optionally the Streamlit frontend. Example (very minimal):

```yaml
version: '3.8'
services:
	db:
		image: ankane/pgvector:postgres-15
		environment:
			POSTGRES_USER: aiuser
			POSTGRES_PASSWORD: aipass
			POSTGRES_DB: aiapp
		ports:
			- "5432:5432"

	backend:
		build: ./backend
		volumes:
			- ./backend:/app
		environment:
			DATABASE_URL: postgresql+psycopg://aiuser:aipass@db:5432/aiapp
		depends_on:
			- db
		ports:
			- "8000:8000"

	frontend:
		image: python:3.11-slim
		command: bash -c "pip install streamlit && streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"
		volumes:
			- ./:/app
		ports:
			- "8501:8501"

```

Save the compose file and run:

```bash
docker compose up --build
```

## Final tips
- Keep secrets out of version control — use `.env` and a secret manager in production.
- Use a managed Postgres service with pgvector in production, or a Docker image that includes the extension.
- If you want, I can add a `docker-compose.yml` file to the repo, convert `docs.py` to use `tempfile`, and add a systemd unit or Windows service example for production-run instructions.

