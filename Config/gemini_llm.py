from neo4j_graphrag.llm.base import LLMInterface
from google.generativeai import GenerativeModel
import os
from dotenv import load_dotenv
load_dotenv()

class GeminiLLM(LLMInterface):
    def __init__(self, api_key: str = os.getenv("GoogleGeminiKey"), model: str = "gemini-1.5-flash"):
        self.model = GenerativeModel(model)
        self.api_key = api_key

    def call(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
