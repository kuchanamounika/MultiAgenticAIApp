from fastapi import FastAPI
from .db import Base, engine, init_pgvector
from .models import DocumentChunk
from .routers.finance import router as finance_router
from .routers.search import router as search_router
from .routers.docs import router as docs_router
from .routers.chat import router as chat_router

app = FastAPI(title="AI App")


@app.on_event("startup")
def on_startup():
    init_pgvector()
    Base.metadata.create_all(bind=engine)


app.include_router(finance_router)
app.include_router(search_router)
app.include_router(docs_router)
app.include_router(chat_router)
