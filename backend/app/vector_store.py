from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import DocumentChunk

def upsert_chunk(db: Session, doc_id: str, content: str, embedding):
    chunk = DocumentChunk(doc_id=doc_id, content=content, embedding=embedding)
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return chunk

def search_chunks(db: Session, query_embedding, top_k: int = 5):
    # This uses pgvector's distance helpers if available
    try:
        stmt = select(DocumentChunk).order_by(DocumentChunk.embedding.cosine_distance(query_embedding)).limit(top_k)
        return db.execute(stmt).scalars().all()
    except Exception:
        # Fallback: return empty list
        return []
