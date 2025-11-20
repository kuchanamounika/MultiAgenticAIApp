from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector
from .db import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, index=True)
    content = Column(String)
    embedding = Column(Vector(1536))
