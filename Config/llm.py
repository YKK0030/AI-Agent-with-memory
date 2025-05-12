import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.getenv("GoogleGeminiKey"), temperature=0, max_tokens=150)