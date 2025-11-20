from fastapi import APIRouter
import yfinance as yf

router = APIRouter(prefix="/finance", tags=["finance"])

@router.get("/price")
def get_price(symbol: str):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")
    last_close = float(hist["Close"].iloc[-1]) if not hist.empty else None
    return {"symbol": symbol, "last_close": last_close}
