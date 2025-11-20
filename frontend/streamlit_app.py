import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("MultiAgentic AI Dashboard")

# Finance
st.header("Finance")
symbol = st.text_input("Symbol", "AAPL")
if st.button("Get Price"):
    r = requests.get(f"{API_URL}/finance/price", params={"symbol": symbol})
    st.json(r.json())

# Search
st.header("Web Search")
q = st.text_input("Query", "latest AI news")
if st.button("Search"):
    r = requests.get(f"{API_URL}/search", params={"q": q, "max_results": 5})
    st.json(r.json())

# Document upload
st.header("Upload PDF")
pdf = st.file_uploader("Choose a PDF", type=["pdf"]) 
if st.button("Upload") and pdf:
    files = {"file": (pdf.name, pdf.getvalue(), "application/pdf")}
    r = requests.post(f"{API_URL}/docs/upload", files={"file": (pdf.name, pdf.getvalue())})
    st.json(r.json())

# Chat
st.header("Chat over documents")
question = st.text_input("Your question", "Summarize the document contents")
provider = st.selectbox("Model provider", ["openai", "groq", "google"]) 
if st.button("Ask"):
    r = requests.post(f"{API_URL}/chat/ask", json={"question": question, "model_provider": provider})
    st.json(r.json())
