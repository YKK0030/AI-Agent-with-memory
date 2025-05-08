import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from neo4j.debug import watch
load_dotenv()

def load_neo4j_graph() -> Neo4jGraph:
    uri      = os.getenv("NEO4J_URI")       
    user     = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    graph = Neo4jGraph(
        url=uri,
        username=user,
        password=password,
        database=database,
    )
    return graph