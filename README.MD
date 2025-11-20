# MultiAgenticAIApp

Full-stack AI scaffold combining FastAPI backend, Streamlit frontend and simple agents.

Structure
- `backend/app/` — FastAPI backend with routers for finance, search, docs (PDF upload + embeddings), and chat.
- `frontend/` — Streamlit app that interacts with the backend.
- `agents/` — small agent example using `phidata`-style tools.
- `.env.example` — example environment variables.

This scaffold is a starting point. Some features (Postgres + pgvector, external model APIs) require provisioning and credentials.
MultiAgenticAIApp
