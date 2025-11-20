import openai
from groq import Groq
import google.generativeai as genai
from .config import OPENAI_API_KEY, GROQ_API_KEY, GOOGLE_API_KEY


def get_openai_client():
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
    return openai


def get_groq_client():
    if GROQ_API_KEY:
        return Groq(api_key=GROQ_API_KEY)
    return Groq()


def get_google_client():
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
    return genai
