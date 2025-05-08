from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
from dotenv import load_dotenv
import os

load_dotenv()

def query_vector_rag(
    question: str,
    vector_index_name: str,
    vector_node_label: str,
    vector_source_property: str,
    vector_embedding_property: str,
    top_k: int = 3
):
    # initialize the Neo4j-backed vector store
    vector_store = Neo4jVector.from_existing_graph(
        embedding=GoogleGenerativeAIEmbeddings(),
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        index_name=vector_index_name,
        node_label=vector_node_label,
        text_node_properties=[vector_source_property],
        embedding_node_property=vector_embedding_property,
    )
    # directly run a similarity search with scores
    docs_and_scores = vector_store.similarity_search_with_score(
        question,
        k=top_k
    )

    return docs_and_scores



# eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InlhZG5pdDAwMzBAZ21haWwuY29tIiwibWl4cGFuZWxJZCI6IiRkZXZpY2U6MTVmOTVhZmEtZjIyYi00NGUzLWFmMzEtOWU0ZGI3OTFkMTNkIiwibWl4cGFuZWxQcm9qZWN0SWQiOiI0YmZiMjQxNGFiOTczYzc0MWI2ZjA2N2JmMDZkNTU3NSIsIm9yZyI6IlRDT0VSIiwicHViIjoibmVvNGouY29tIiwicmVnIjoiWWFkbml0IEthbGUiLCJzdWIiOiJuZW80ai1kZXNrdG9wIiwiZXhwIjoxNzc4MjE5OTE3LCJ2ZXIiOiIqIiwiaXNzIjoibmVvNGouY29tIiwibmJmIjoxNzQ2NjgzOTE3LCJpYXQiOjE3NDY2ODM5MTcsImp0aSI6ImZ4NWVyenBtLSJ9.giurWBuJ3rCXnqjJz4LUZWQCjbgBzoDTD62zfME1mAdLxIH2I-r1wIevXTAvz619WWz-7c-K08tCVIG2hNxn_GeT6H4s8_I27V-1ZOOUX7XTP2BIJknUeBDsAR0RPgb0mk7XWauW3B0sPbvEA1tPLEvTharS1dLi5m7bO0h8Fbfb-CRrTxNaqoQikCPwQmnMPMNcPl9mL8VBXNvfc1tQ_8SuCZ4Y05k9mWw5TqsnfHDyv9eM8YN07S1dWqAbp7si31C03Ms-_-GP0weMpGuT5Ra_FXv69mtLtmxECec9JuSRAkWmvd8lFNv6gL71ieveaLI0BceQo4pRd2_w69ZAng