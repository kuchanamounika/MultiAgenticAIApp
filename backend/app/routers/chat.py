from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..vector_store import search_chunks
from ..llm_clients import get_openai_client, get_groq_client, get_google_client

router = APIRouter(prefix="/chat", tags=["chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ask")
def ask(
    question: str = Body(...),
    model_provider: str = Body("openai"),
    db: Session = Depends(get_db),
):
    # Embed question (using OpenAI for simplicity)
    openai = get_openai_client()
    try:
        q_emb = openai.Embedding.create(model="text-embedding-3-small", input=[question])["data"][0]["embedding"]
    except Exception:
        q_emb = None

    ctx_chunks = search_chunks(db, q_emb, top_k=5) if q_emb is not None else []
    context = "\n\n".join([c.content for c in ctx_chunks])

    prompt = f"Answer the question using the context below.\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"

    if model_provider == "openai":
        resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
        answer = resp["choices"][0]["message"]["content"]
    elif model_provider == "groq":
        groq = get_groq_client()
        resp = groq.chat.completions.create(model="llama3-70b-8192", messages=[{"role": "user", "content": prompt}])
        answer = resp.choices[0].message.content
    elif model_provider == "google":
        genai = get_google_client()
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        answer = getattr(resp, "text", str(resp))
    else:
        answer = "Unsupported provider"

    return {"answer": answer, "sources": [c.id for c in ctx_chunks]}
