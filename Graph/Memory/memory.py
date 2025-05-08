# Graph/Memory/memory.py
import json
from types import SimpleNamespace
from typing import List, Dict, Tuple
import time
from langchain_core.messages import HumanMessage, SystemMessage
from Graph.Prompt.prompts import Agent_prompt
from Config.neo4j import load_neo4j_graph
from langgraph.checkpoint.memory import MemorySaver
from Graph.Memory.db import Neo4jMemoryStore

# 1. Short-term memory (thread-scoped)
short_term_memory_store = MemorySaver()

# 2. Long-term memory (Neo4j-backed)
kg = load_neo4j_graph()
long_term_memory_store = Neo4jMemoryStore(kg_client=kg)

# 3) User / app identifiers
user_id = "user-6"
default_app_ctx = "history"

def load_and_save_long_term(state: dict) -> list:
    """
    state_modifier for your agent:
     - saves the latest user msg into Neo4j under (user_id, thread_id)
     - retrieves the last 5 memories
     - prepends [System prompt] + [Memory snippets] + existing chat history
    """
    # pull the thread_id out of the state (passed via app.py)
    thread_id = state.get("thread_id", default_app_ctx)
    namespace = (user_id, thread_id)

    # a) grab and store the last user message
    last_msg = state["messages"][-1].content
    key = f"msg-{int(time.time())}"
    long_term_memory_store.put_memory(namespace, key, {"text": last_msg})

    # b) fetch the most recent 5 memories
    records = long_term_memory_store.search_memory(namespace, limit=5)
    mem_msgs = [
        HumanMessage(content=f"[Memory] {r.key}: {r.value['text']}")
        for r in records
    ]

    # c) system prompt
    sys_msg = (
        Agent_prompt
        if isinstance(Agent_prompt, SystemMessage)
        else SystemMessage(content=Agent_prompt)
    )

    # d) rebuild the list the LLM sees
    return [sys_msg] + mem_msgs + state["messages"]