from fastapi import APIRouter, Query
from duckduckgo_search import DDGS

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
def web_search(q: str = Query(...), max_results: int = 5):
    with DDGS() as ddgs:
        results = ddgs.text(q, max_results=max_results)
    return {"query": q, "results": results}
