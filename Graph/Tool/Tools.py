from langchain_core.tools import tool
from KG.VectorRAG import query_vector_rag
from Config.tavily import search_engine
from Config.neo4j import load_neo4j_graph
import json

@tool
def get_vector_response(question,top_k=5):
    """Use this to get vector response from database."""
    Vector_RAG = query_vector_rag(
        question=question, 
        vector_index_name = 'Chunk',
        vector_node_label = 'Chunk',
        vector_source_property= 'text',
        vector_embedding_property = 'textEmbeddingOpenAI',
        top_k= top_k
        )
    return Vector_RAG


@tool
def add_data_to_kg(search_result):
    """
    Use this to add a Search node in Neo4j with the given input directly as text.

    Args:
        search_result: a string, dict, or any object. If dict, 'summary' or 'text' field is used; otherwise, serialized as JSON or string.
    """
    graph = load_neo4j_graph()

    # Extract text
    if isinstance(search_result, dict):
        text = search_result.get('summary') or search_result.get('text') or json.dumps(search_result)
    else:
        text = str(search_result)

    # Create the Search node
    cypher = "CREATE (s:Search {text: $text})"
    graph.query(cypher, params={"text": text})

    return "Added 1 Search node to Neo4j."

@tool
def SearchEngine(query: str, max_results: int = 10) -> str:
    """
    Fetches top search results via Tavily’s Search API.
    """
    if max_results is not None:
        search_engine.max_results = max_results

    # either of the following two will work:
    return search_engine.run(query)             