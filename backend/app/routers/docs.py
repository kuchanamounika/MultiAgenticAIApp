import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..utils.pdf import extract_text_from_pdf
from ..vector_store import upsert_chunk
from ..llm_clients import get_openai_client

router = APIRouter(prefix="/docs", tags=["docs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save temp
    doc_id = str(uuid.uuid4())
    tmp_path = f"/tmp/{doc_id}.pdf"
    with open(tmp_path, "wb") as f:
        f.write(file.file.read())

    text = extract_text_from_pdf(tmp_path)
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    # Simple chunking
    chunks = [text[i:i+1500] for i in range(0, len(text), 1500)]
    openai = get_openai_client()
    # Get embeddings using OpenAI (replace with model you prefer)
    try:
        resp = openai.Embedding.create(model="text-embedding-3-small", input=chunks)
        embeddings = [item["embedding"] for item in resp["data"]]
    except Exception:
        embeddings = [None] * len(chunks)

    for content, emb in zip(chunks, embeddings):
        upsert_chunk(db, doc_id=doc_id, content=content, embedding=emb)

    return {"doc_id": doc_id, "chunks": len(chunks)}
