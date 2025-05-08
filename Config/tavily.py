from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv
load_dotenv()



api_key = os.getenv("TAVILY_API_KEY")


search_engine = TavilySearch(
    api_key=api_key,
    max_results=10,
    search_depth="advanced",
    time_range="year",
    semantic_configuration="default",
    reranker="cross-encoder/ms-marco-MiniLM-L-6-v2",
    filters={"language": "en"},
)